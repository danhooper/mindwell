import os
import sys
import getopt
all_kind_list = [
    'UserInfo',
    'ClientInfo',
    'DOS',
    'DOSRecurr']

def download_item(item):
    os.popen('del %s.csv' % item)
    executing = 'appcfg.py download_data --config_file=bulkloader.yaml --filename=%s.csv --kind=%s --url http://mind-well.appspot.com/remote_api -e dan.c.hooper@gmail.com' %( item, item)
    print executing
    os.popen(executing)

def upload_item(item):
    executing = 'appcfg.py upload_data --config_file=bulkloader.yaml --filename=%s.csv --kind=%s --url http://mind-well.appspot.com/remote_api -e dan.c.hooper@gmail.com' %( item, item)
    print executing
    os.popen(executing)

def main(argv):
    for argument in sys.argv:
        optlist, args = getopt.getopt(argv, 'duk:', ['kind='])
    download = False
    upload = False
    kind_list = []
    for opt, arg in optlist:
        if opt == '-d':
            download = True
        if opt == '-u':
            upload = True
        if opt == '-k' or opt =='--kind':
            kind_list.append(arg)
    if not kind_list:
        kind_list = all_kind_list
    for item in kind_list:
        if download:
            download_item(item)
        if upload:
            upload_item(item)

if __name__ == '__main__':
    main(sys.argv[1:])