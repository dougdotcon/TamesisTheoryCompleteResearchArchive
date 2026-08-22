"""
Minimal, dependency-free EDF header parser used ONLY to verify file format
and basic acquisition parameters (channel count, channel labels, sampling
rate, record duration, number of records) of downloaded sample files.

Does NOT read/decode the signal data payload and does NOT compute any
discriminating statistic. EDF header layout per Kemp et al. (1992),
"A simple format for exchange of digitized polygraphic recordings",
Electroencephalography and Clinical Neurophysiology, 82(5), 391-393
(the standard EDF specification, https://www.edfplus.info/specs/edf.html).
"""
import sys


def read_edf_header(path):
    with open(path, "rb") as f:
        raw = f.read(256)
        version = raw[0:8].decode("ascii", "replace").strip()
        patient_id = raw[8:88].decode("ascii", "replace").strip()
        recording_id = raw[88:168].decode("ascii", "replace").strip()
        start_date = raw[168:176].decode("ascii", "replace").strip()
        start_time = raw[176:184].decode("ascii", "replace").strip()
        n_header_bytes = int(raw[184:192].decode("ascii", "replace").strip())
        n_records = int(raw[236:244].decode("ascii", "replace").strip())
        record_dur = float(raw[244:252].decode("ascii", "replace").strip())
        ns = int(raw[252:256].decode("ascii", "replace").strip())

        f.seek(256)
        signal_header = f.read(256 * ns)

    def field(block, i, width):
        return block[i * width:(i + 1) * width].decode("ascii", "replace").strip()

    off = 0
    labels = [field(signal_header, i, 16) for i in range(ns)]
    off += 16 * ns
    transducer = [signal_header[off + i * 80: off + (i + 1) * 80].decode("ascii", "replace").strip() for i in range(ns)]
    off += 80 * ns
    phys_dim = [signal_header[off + i * 8: off + (i + 1) * 8].decode("ascii", "replace").strip() for i in range(ns)]
    off += 8 * ns
    phys_min = [signal_header[off + i * 8: off + (i + 1) * 8].decode("ascii", "replace").strip() for i in range(ns)]
    off += 8 * ns
    phys_max = [signal_header[off + i * 8: off + (i + 1) * 8].decode("ascii", "replace").strip() for i in range(ns)]
    off += 8 * ns
    dig_min = [signal_header[off + i * 8: off + (i + 1) * 8].decode("ascii", "replace").strip() for i in range(ns)]
    off += 8 * ns
    dig_max = [signal_header[off + i * 8: off + (i + 1) * 8].decode("ascii", "replace").strip() for i in range(ns)]
    off += 8 * ns
    prefilt = [signal_header[off + i * 80: off + (i + 1) * 80].decode("ascii", "replace").strip() for i in range(ns)]
    off += 80 * ns
    n_samples = [int(signal_header[off + i * 8: off + (i + 1) * 8].decode("ascii", "replace").strip()) for i in range(ns)]
    off += 8 * ns

    fs = [n_samples[i] / record_dur if record_dur > 0 else float("nan") for i in range(ns)]

    return {
        "path": path,
        "edf_version": version,
        "patient_id": patient_id,
        "recording_id": recording_id,
        "start_date": start_date,
        "start_time": start_time,
        "n_header_bytes": n_header_bytes,
        "n_records": n_records,
        "record_duration_s": record_dur,
        "n_signals": ns,
        "labels": labels,
        "phys_dim": phys_dim,
        "prefiltering": prefilt,
        "n_samples_per_record": n_samples,
        "sampling_rate_hz": fs,
        "total_duration_s": n_records * record_dur,
    }


if __name__ == "__main__":
    for p in sys.argv[1:]:
        h = read_edf_header(p)
        print("=" * 70)
        print("file:", h["path"])
        print("EDF version tag:", repr(h["edf_version"]))
        print("patient_id field:", h["patient_id"])
        print("recording_id field:", h["recording_id"])
        print("start_date/time:", h["start_date"], h["start_time"])
        print("n_signals:", h["n_signals"])
        print("n_records:", h["n_records"], "record_duration_s:", h["record_duration_s"])
        print("total_duration_s:", h["total_duration_s"])
        print("labels:", h["labels"])
        print("phys_dim:", h["phys_dim"])
        print("sampling_rate_hz (per channel):", h["sampling_rate_hz"])
        print("prefiltering[0]:", h["prefiltering"][0] if h["prefiltering"] else None)
