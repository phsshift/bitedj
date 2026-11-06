#!/usr/bin/env python3
"""Read-only, bounded GitHub CI monitor. No credentials or VPN changes."""
import argparse
import json
import random
import time
import urllib.error
import urllib.request


def fetch(url):
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={
                'User-Agent': 'BiteDJ-CI-monitor',
                'Accept': 'application/vnd.github+json',
                'Connection': 'close',
            })
            with urllib.request.urlopen(request, timeout=15) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            if isinstance(error, urllib.error.HTTPError) and error.code not in (429, 500, 502, 503, 504):
                raise
            print(json.dumps({'transport_retry': attempt + 1,
                              'error_type': type(error).__name__}), flush=True)
            if attempt == 3:
                raise
            time.sleep(min(2 ** (attempt + 1), 8) + random.random())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('run_id', type=int)
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--minutes', type=int, default=120)
    args = parser.parse_args()
    url = f'https://api.github.com/repos/phsshift/bitedj/actions/runs/{args.run_id}/jobs'
    deadline = time.monotonic() + args.minutes * 60
    while time.monotonic() < deadline:
        try:
            data = fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            print(json.dumps({'status': 'unreachable', 'error_type': type(error).__name__}), flush=True)
            if args.once:
                return 2
            time.sleep(45)
            continue
        jobs = [{'id': job['id'], 'name': job['name'], 'status': job['status'],
                 'conclusion': job['conclusion'],
                 'step': next((step['name'] for step in job.get('steps', [])
                               if step['status'] == 'in_progress'), None),
                 'failed_steps': [step['name'] for step in job.get('steps', [])
                                  if step.get('conclusion') == 'failure']}
                for job in data['jobs']]
        print(json.dumps({'run_id': args.run_id, 'jobs': jobs}), flush=True)
        if jobs and all(job['status'] == 'completed' for job in jobs):
            return 0 if all(job['conclusion'] == 'success' for job in jobs) else 1
        if args.once:
            return 0
        time.sleep(60)
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
