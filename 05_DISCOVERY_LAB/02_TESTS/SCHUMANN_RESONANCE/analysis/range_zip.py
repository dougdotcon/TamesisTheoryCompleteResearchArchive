"""
A minimal seekable file-like object over HTTP Range requests, for use with
Python's zipfile module against a large remote ZIP without downloading it
in full. Caches fetched byte ranges in memory (not on disk) and coalesces
reads into whole blocks to keep the number of HTTP requests low (Zenodo
enforces a per-minute rate limit reported via X-RateLimit-* headers).
"""
import io
import bisect
import requests

CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


class RangeHTTPFile(io.RawIOBase):
    def __init__(self, url, size=None, session=None, verbose=True):
        self.url = url
        self.session = session or requests.Session()
        self.verbose = verbose
        self.request_count = 0
        self.bytes_fetched = 0
        if size is None:
            r = self.session.head(url, verify=CA_BUNDLE, timeout=60)
            r.raise_for_status()
            size = int(r.headers["Content-Length"])
        self.size = size
        self.pos = 0
        # sorted list of (start, end_exclusive, bytes) cached ranges
        self._blocks = []  # list of (start, data)

    def readable(self):
        return True

    def seekable(self):
        return True

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_END:
            self.pos = self.size + offset
        return self.pos

    def tell(self):
        return self.pos

    def _fetch_range(self, start, end_inclusive):
        """Fetch [start, end_inclusive] over HTTP and cache it."""
        headers = {"Range": f"bytes={start}-{end_inclusive}"}
        r = self.session.get(self.url, headers=headers, verify=CA_BUNDLE, timeout=120)
        r.raise_for_status()
        if r.status_code != 206:
            raise RuntimeError(f"Expected 206 Partial Content, got {r.status_code}")
        data = r.content
        self.request_count += 1
        self.bytes_fetched += len(data)
        if self.verbose:
            print(f"  [HTTP range fetch #{self.request_count}] bytes={start}-{end_inclusive} "
                  f"({len(data)} bytes, {self.bytes_fetched/1e6:.2f} MB total so far)")
        self._blocks.append((start, data))
        self._blocks.sort(key=lambda b: b[0])
        return data

    def _covered(self, start, end_exclusive):
        """Return True if [start, end_exclusive) is fully covered by cache."""
        pos = start
        for bstart, bdata in self._blocks:
            bend = bstart + len(bdata)
            if bstart <= pos < bend:
                pos = bend
                if pos >= end_exclusive:
                    return True
        return pos >= end_exclusive

    def _read_from_cache(self, start, length):
        out = bytearray(length)
        remaining = [(start, length)]
        for bstart, bdata in self._blocks:
            bend = bstart + len(bdata)
            new_remaining = []
            for (s, l) in remaining:
                e = s + l
                # overlap [max(s,bstart), min(e,bend))
                os_ = max(s, bstart)
                oe = min(e, bend)
                if os_ < oe:
                    out[os_ - start: oe - start] = bdata[os_ - bstart: oe - bstart]
                    if s < os_:
                        new_remaining.append((s, os_ - s))
                    if oe < e:
                        new_remaining.append((oe, e - oe))
                else:
                    new_remaining.append((s, l))
            remaining = new_remaining
        return bytes(out)

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        n = max(0, min(n, self.size - self.pos))
        if n == 0:
            return b""
        start = self.pos
        end_exclusive = start + n
        if not self._covered(start, end_exclusive):
            self._fetch_range(start, end_exclusive - 1)
        data = self._read_from_cache(start, n)
        self.pos += n
        return data

    def readinto(self, b):
        data = self.read(len(b))
        b[: len(data)] = data
        return len(data)

    def prefetch(self, start, end_inclusive):
        """Force-fetch a range now (used to batch central-directory reads)."""
        if not self._covered(start, end_inclusive + 1):
            self._fetch_range(start, end_inclusive)
