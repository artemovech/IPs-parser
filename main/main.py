import argparse
import json
import re
import sys
import time
import urllib
import urllib.request


class ParseIPs():
    '''Parse log file to find all IP'''

    def __init__(self):
        self.dict_ip = {}
        self.time_f = time.ctime().strip()
        self.ip_list = []

    def open(self, file):
        '''Open log file'''
        with open(file) as f:
            l = f.readlines()
            for lines in l:
                ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', lines)  # find all IP in file (log, txt, etc..)
                self.ip_list.append(str(ip[0])[4:])
        self.get_info()  # get info for ip in current list

    def get_info(self):
        '''Get info from ip-api website'''
        ip_set = set(self.ip_list)  # delete not-unique elements
        len_set = len(ip_set)
        cap = 0
        for ip in ip_set:
            if cap < 150:
                url = f'http://ip-api.com/json/{ip}'
                response = urllib.request.urlopen(url)
                data = json.loads(response.read())
                self.check_fail_ip_status(data)
                cap += 1
            else:
                print('Zzzz... {} IP left'.format(len_set - 150))
                time.sleep(61)
                cap = 0

    def check_fail_ip_status(self, data):
        '''Return right status to IP'''
        if data['status'] == 'fail':
            self.dict_ip[data['query']] = {'status': 'Privat IP adress'}
        else:
            self.dict_ip[data['query']] = {'countryCode': data['countryCode'],
                                           'country': data['country'],
                                           'city': data['city']
                                           }
        js = json.dumps(self.dict_ip)
        self.add_to_file(js)

    def add_to_file(self, a):
        '''Add to file a result for all IP'''
        with open('{}.json'.format(str(self.time_f)), 'w', encoding='utf-8') as w:
            w.write(a)


class Argarsing:
    def initialize_args(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-f', '--file')  # file name arg
        args = self.parser.parse_args(sys.argv[1:])
        values = vars(args)
        return values['file']


if __name__ == '__main__':
    file = Argarsing().initialize_args()
    a = ParseIPs()
    a.open(file)
