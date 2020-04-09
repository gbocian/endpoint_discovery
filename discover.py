#!/usr/bin/env python3.6

from urllib.request import urlopen
import socket
from json import loads
import sys
import copy

BASE_DICT = {'domain': '', 'ip': '', 'host': ''}


def get_host_name_by_ip_address(base_dict_list):
    for i in base_dict_list:
        try:
            value = socket.gethostbyaddr(i['ip'])[0]
        except socket.herror as err:
            i['host'] = f"Socket error: {err}"
        except OSError as err:
            i['host'] = f"OS error: {err}"
        else:
            i['host'] = value


def get_host_ip_by_name(base_dict_list):
    for i in base_dict_list:
        try:
            value = socket.gethostbyname(i['domain'])
        except socket.gaierror as err:
            i['ip'] = f"OS error: {err}"
        else:
            i['ip'] = value


def create_nested_dict(data):
    values = []
    for r in data:
        tmp = copy.copy(BASE_DICT)
        tmp['domain'] = r

        values.append(tmp)

    return values


def domain_data(json_data):
    value = []
    for r in json_data:
        if "\n" in r['name_value']:
            for i in r['name_value'].split("\n"):
                value.append(i)
        else:
            value.append(r['name_value'])

    return value


def request_data(url_address):
    with urlopen(url_address) as response:
        try:
            value = response.read()
        except KeyboardInterrupt:
            value = None
        else:
            return value


def main(start_url):
    print(f"[i] requesting data from: {request_url}")
    data = request_data(request_url)

    domains_json = loads(data.decode('utf-8'))
    print(f"[+] collected {len(domains_json)} records")

    domains = domain_data(domains_json)
    print(f"[+] extracted {len(domains)} domains entries")

    unique_domains = set(domains)
    print(f"[+] identified {len(unique_domains)} unique domains")

    domain_details = create_nested_dict(unique_domains)
    print("[+] transforming unique domains into list of base dicts")

    get_host_ip_by_name(domain_details)
    print("[+] collecting host ip address")

    get_host_name_by_ip_address(domain_details)
    print("[+] collecting host name")

    # TODO: save to file
    for i in domain_details:
        print(i)


if __name__ == "__main__":
    domain_name = "example.com"
    request_url = f"https://crt.sh/?q={domain_name}&output=json"
    main(request_url)
    sys.exit(0)
