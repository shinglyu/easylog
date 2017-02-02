import argparse
import fileinput
import json
from termcolor import colored
import sys

def main():
    parser = argparse.ArgumentParser(description='Print easylog JSON file')
    parser.add_argument('filename', type=argparse.FileType("r"),
                        help='the log json generated by easylog')

    args = parser.parse_args()

    json_str = args.filename.read()
    args.filename.close()

    lines = json.loads(json_str)
    for line in lines:
        if 'important' in line['tags']:
            print(colored(line['line'], 'white', 'on_red')),
            continue
        if 'error' in line['tags']:
            print(colored(line['line'], 'red')),
            continue
        if 'warn' in line['tags']:
            print(colored(line['line'], 'yellow')),
            continue
        else:
            print(colored(line['line'], attrs=['dark'])),

if __name__ == '__main__':
    main()
