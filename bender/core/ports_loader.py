import os
import json
import urllib.request
import csv
import time

IANA_CSV_URL = "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"
CACHE_FILENAME = 'ports_cache.json'
CACHE_TTL = 7 * 24 * 60 * 60  # 1 week


def download_csv(csv_path):
    urllib.request.urlretrieve(IANA_CSV_URL, csv_path)


def parse_csv_to_json(csv_path):
    result = {'tcp': {}, 'udp': {}, 'sctp': {}, 'dccp': {}}
    with open(csv_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proto = row['Transport Protocol'].strip().lower()
            port = row['Port Number'].strip()
            service = row['Service Name'].strip()
            desc = row['Description'].strip()
            if not port.isdigit() or proto not in result:
                continue
            result[proto][port] = {
                "Service Name": service,
                "Description": desc
            }
    return result


def is_cache_valid(cache_file):
    if not os.path.exists(cache_file):
        return False
    cache_mtime = os.path.getmtime(cache_file)
    return (time.time() - cache_mtime) < CACHE_TTL


def update_cache(cache_file):
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    tmp_csv = os.path.join(os.path.dirname(cache_file), 'service-names-port-numbers.csv')
    download_csv(tmp_csv)
    ports_dict = parse_csv_to_json(tmp_csv)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(ports_dict, f, ensure_ascii=False, indent=2)
    os.remove(tmp_csv)
    return ports_dict


def get_ports_dict(protocol='tcp', app_dir=None):
    if app_dir is None:
        raise ValueError('app_dir must be provided')
    cache_file = os.path.join(app_dir, CACHE_FILENAME)
    if is_cache_valid(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            ports_dict = json.load(f)
    else:
        ports_dict = update_cache(cache_file)
    return ports_dict.get(protocol, {})