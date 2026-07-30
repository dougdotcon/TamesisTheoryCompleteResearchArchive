#!/usr/bin/env python3
"""Read-only summary of Mathlib cache containers and partial objects."""
import argparse, json, os
from pathlib import Path
from urllib.parse import urlparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cache-dir', default=os.path.expanduser('~/.cache/mathlib'))
    p.add_argument('--config', default=None)
    a = p.parse_args()
    cache = Path(a.cache_dir)
    cfg = Path(a.config) if a.config else cache / 'curl.cfg'
    containers = {}
    urls = []
    if cfg.exists():
        for line in cfg.read_text(errors='replace').splitlines():
            line = line.strip()
            if not line.lower().startswith('url = '): continue
            u = line[6:].strip(); urls.append(u)
            parts = urlparse(u).path.strip('/').split('/')
            if len(parts) >= 2:
                containers[parts[0]] = containers.get(parts[0], 0) + 1
    parts = []
    for f in sorted(cache.glob('*.part')):
        data = f.read_bytes()[:512]
        if not data: status = 'empty'
        elif b'The specified blob does not exist' in data or b'BlobNotFound' in data: status = 'http_404_body'
        else: status = 'nonempty_other'
        parts.append({'name': f.name, 'size': f.stat().st_size, 'status': status})
    ltars = sorted(cache.glob('*.ltar'))
    result = {'cache_dir': str(cache), 'config': str(cfg), 'config_exists': cfg.exists(),
              'url_count': len(urls), 'containers': containers,
              'ltar_count': len(ltars), 'part_count': len(parts),
              'part_status_counts': {s: sum(x['status']==s for x in parts) for s in sorted({x['status'] for x in parts})},
              'part_samples': parts[:20] + ([] if len(parts) <= 20 else parts[-20:])}
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__': main()
