"""
Independent, from-scratch EDF(+) reader written for the adversarial
reproduction of DISC-COGNITIVE-EEG-SPECTRAL-001 (depression arm).

Implements the plain EDF binary format directly from the public spec
(Kemp et al. 1992; EDF+ extensions Kemp & Roessen 2003) WITHOUT using
mne or pyedflib, so that channel labels, sample rate, and physical-value
scaling are verified independently rather than trusted from a library
that the primary analysis may also depend on.

Header layout (fixed ASCII, byte offsets):
  8   version
  80  patient id
  80  recording id
  8   startdate (dd.mm.yy)
  8   starttime (hh.mm.ss)
  8   number of bytes in header record
  44  reserved
  8   number of data records ("-1" if unknown)
  8   duration of a data record, in seconds
  4   number of signals (ns) in data record

Then, ns times each, in parallel blocks (all labels, then all
transducer types, etc.):
  16  label
  80  transducer type
  8   physical dimension
  8   physical minimum
  8   physical maximum
  8   digital minimum
  8   digital maximum
  80  prefiltering
  8   number of samples in each data record
  32  reserved

Data records follow immediately: nr_data_records times, each containing,
for each signal i in order, nr_samples[i] samples of 2-byte little-endian
signed integers.
"""
import numpy as np


class EDFSignal:
    __slots__ = ("label", "transducer", "phys_dim", "phys_min", "phys_max",
                 "dig_min", "dig_max", "prefiltering", "n_samples_per_record")


class EDFFile:
    def __init__(self, path):
        with open(path, "rb") as f:
            raw = f.read()
        self.raw = raw
        self._parse_header()
        self._parse_data()

    def _parse_header(self):
        raw = self.raw

        def s(offset, length):
            return raw[offset:offset + length].decode("ascii", errors="strict").strip()

        self.version = s(0, 8)
        self.patient_id = s(8, 80)
        self.recording_id = s(88, 80)
        self.startdate = s(168, 8)
        self.starttime = s(176, 8)
        self.n_header_bytes = int(s(184, 8))
        self.reserved = s(192, 44)
        self.is_edf_plus = "EDF+" in self.reserved
        n_records_str = s(236, 8)
        self.n_data_records = int(n_records_str)
        self.record_duration = float(s(244, 8))
        self.n_signals = int(s(252, 4))

        ns = self.n_signals
        off = 256
        labels = [raw[off + 16 * i: off + 16 * (i + 1)].decode("ascii").strip() for i in range(ns)]
        off += 16 * ns
        transducers = [raw[off + 80 * i: off + 80 * (i + 1)].decode("ascii").strip() for i in range(ns)]
        off += 80 * ns
        phys_dims = [raw[off + 8 * i: off + 8 * (i + 1)].decode("ascii").strip() for i in range(ns)]
        off += 8 * ns
        phys_mins = [float(raw[off + 8 * i: off + 8 * (i + 1)].decode("ascii").strip()) for i in range(ns)]
        off += 8 * ns
        phys_maxs = [float(raw[off + 8 * i: off + 8 * (i + 1)].decode("ascii").strip()) for i in range(ns)]
        off += 8 * ns
        dig_mins = [int(raw[off + 8 * i: off + 8 * (i + 1)].decode("ascii").strip()) for i in range(ns)]
        off += 8 * ns
        dig_maxs = [int(raw[off + 8 * i: off + 8 * (i + 1)].decode("ascii").strip()) for i in range(ns)]
        off += 8 * ns
        prefilters = [raw[off + 80 * i: off + 80 * (i + 1)].decode("ascii").strip() for i in range(ns)]
        off += 80 * ns
        nsamples = [int(raw[off + 8 * i: off + 8 * (i + 1)].decode("ascii").strip()) for i in range(ns)]
        off += 8 * ns
        off += 32 * ns  # reserved per-signal

        assert off == self.n_header_bytes, (
            f"header size mismatch: computed {off} vs declared {self.n_header_bytes}"
        )

        self.signals = []
        for i in range(ns):
            sig = EDFSignal()
            sig.label = labels[i]
            sig.transducer = transducers[i]
            sig.phys_dim = phys_dims[i]
            sig.phys_min = phys_mins[i]
            sig.phys_max = phys_maxs[i]
            sig.dig_min = dig_mins[i]
            sig.dig_max = dig_maxs[i]
            sig.prefiltering = prefilters[i]
            sig.n_samples_per_record = nsamples[i]
            self.signals.append(sig)

    def _parse_data(self):
        raw = self.raw
        ns = self.n_signals
        record_size_samples = sum(sig.n_samples_per_record for sig in self.signals)
        record_size_bytes = record_size_samples * 2
        data_start = self.n_header_bytes
        available_bytes = len(raw) - data_start
        n_records_actual = available_bytes // record_size_bytes
        if self.n_data_records == -1:
            n_records = n_records_actual
        else:
            n_records = self.n_data_records
            assert n_records <= n_records_actual, "declared more data records than bytes available"

        all_raw = np.frombuffer(raw, dtype="<i2", count=n_records * record_size_bytes // 2,
                                 offset=data_start)
        all_raw = all_raw.reshape(n_records, record_size_samples)

        # split by signal within each record
        self._digital = []
        col = 0
        for sig in self.signals:
            n = sig.n_samples_per_record
            block = all_raw[:, col:col + n].reshape(-1)  # concatenate records in time order
            self._digital.append(block)
            col += n
        self.n_records = n_records

    def physical_signal(self, index):
        """Return the physical-unit signal for channel `index` as float64."""
        sig = self.signals[index]
        dig = self._digital[index].astype(np.float64)
        drange = (sig.dig_max - sig.dig_min)
        if drange == 0:
            raise ValueError(f"zero digital range for channel {sig.label}")
        gain = (sig.phys_max - sig.phys_min) / drange
        offset = sig.phys_max - sig.dig_max * gain
        return dig * gain + offset

    def channel_index(self, label_exact=None, label_contains=None):
        for i, sig in enumerate(self.signals):
            if label_exact is not None and sig.label == label_exact:
                return i
            if label_contains is not None and label_contains in sig.label:
                return i
        return None

    def sample_rate(self, index):
        sig = self.signals[index]
        return sig.n_samples_per_record / self.record_duration
