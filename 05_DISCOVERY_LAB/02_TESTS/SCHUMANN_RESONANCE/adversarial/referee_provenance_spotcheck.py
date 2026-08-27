#!/usr/bin/env python3
"""
Independent re-download spot-check (referee task, written from scratch,
without reading analysis/range_zip.py). Fetches the ZIP central directory
via one HTTP Range request for the last bytes of the 2014.zip Zenodo
archive, locates one specific entry, downloads just that entry via a
second Range request, and compares its bytes/CRC32/SHA256 against the
locally cached copy under data/raw/.
"""
import hashlib
import io
import zipfile
import zlib

import requests

URL = "https://zenodo.org/api/records/6348691/files/2014.zip/content"
TARGET_ENTRY = "2014/1407/smplGRTU1_sensor_1_1407151257"
LOCAL_FILE = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/SCHUMANN_RESONANCE/data/raw/2014-07-15/EW/smplGRTU1_sensor_1_1407151257"


class RangeFile(io.RawIOBase):
    """Minimal seekable file-like object over HTTP Range requests, with an
    in-memory cache of already-fetched byte spans. Written independently
    for this referee check."""

    def __init__(self, url, total_size):
        self.url = url
        self.total_size = total_size
        self.pos = 0
        self.cache = {}  # (start,end) -> bytes, simple linear scan cache
        self.requests_made = 0
        self.bytes_fetched = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        if whence == 0:
            self.pos = offset
        elif whence == 1:
            self.pos += offset
        elif whence == 2:
            self.pos = self.total_size + offset
        return self.pos

    def tell(self):
        return self.pos

    def _fetch_range(self, start, end):
        # end inclusive
        for (s, e), data in self.cache.items():
            if s <= start and end <= e:
                return data[start - s : end - s + 1]
        headers = {"Range": f"bytes={start}-{end}"}
        r = requests.get(self.url, headers=headers, timeout=60)
        r.raise_for_status()
        assert r.status_code == 206, f"expected 206, got {r.status_code}"
        data = r.content
        self.cache[(start, end)] = data
        self.requests_made += 1
        self.bytes_fetched += len(data)
        return data

    def readinto(self, b):
        n = len(b)
        start = self.pos
        end = min(self.pos + n, self.total_size) - 1
        if end < start:
            return 0
        data = self._fetch_range(start, end)
        b[: len(data)] = data
        self.pos += len(data)
        return len(data)


def main():
    head = requests.head(URL, timeout=30)
    total_size = int(head.headers["Content-Length"])
    print(f"Total zip size (Content-Length header, this session's own HEAD request): {total_size}")
    assert total_size == 26697876825, "size mismatch vs PROVENANCE.md claim"

    rf = RangeFile(URL, total_size)
    # Fetch just enough of the tail for EOCD + Zip64 EOCD locator + central directory.
    # Central directory for the full 2014.zip is documented as ~last ~12MB in
    # PROVENANCE.md; use the same generous margin here, fetched independently.
    tail_size = 12 * 1024 * 1024
    tail_start = total_size - tail_size
    rf.seek(tail_start)
    _ = rf._fetch_range(tail_start, total_size - 1)  # warm cache with one big range read

    zf = zipfile.ZipFile(rf)
    names = zf.namelist()
    print(f"Central directory entries found: {len(names)}")
    assert TARGET_ENTRY in names, "target entry not found in central directory"

    info = zf.getinfo(TARGET_ENTRY)
    print(f"Target entry: {TARGET_ENTRY}")
    print(f"  compress_size={info.compress_size} file_size={info.file_size} CRC32(hex)={info.CRC:08x}")

    remote_bytes = zf.read(TARGET_ENTRY)
    print(f"Downloaded {len(remote_bytes)} bytes for target entry")
    print(f"HTTP requests made this check: {rf.requests_made}, bytes over network: {rf.bytes_fetched}")

    remote_crc32 = zlib.crc32(remote_bytes) & 0xFFFFFFFF
    remote_sha256 = hashlib.sha256(remote_bytes).hexdigest()
    print(f"Remote (freshly downloaded) CRC32: {remote_crc32:08x}")
    print(f"Remote (freshly downloaded) SHA256: {remote_sha256}")

    local_bytes = open(LOCAL_FILE, "rb").read()
    local_crc32 = zlib.crc32(local_bytes) & 0xFFFFFFFF
    local_sha256 = hashlib.sha256(local_bytes).hexdigest()
    print(f"Local cached copy CRC32: {local_crc32:08x}")
    print(f"Local cached copy SHA256: {local_sha256}")

    print()
    print("BYTES IDENTICAL:", remote_bytes == local_bytes)
    print("SHA256 MATCH:", remote_sha256 == local_sha256)


if __name__ == "__main__":
    main()
