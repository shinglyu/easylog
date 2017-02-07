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

    prev_line = None
    repeat_count = 0

    for line in lines:
        if line == prev_line:
            repeat_count += 1
            continue # Skip printing
        else:
            if repeat_count > 0:
                print(colored("(Repeats {0} times)".format(repeat_count), attrs=["dark"]))
            repeat_count = 0
            prev_line = line

        attrs = []
        if 'frequent' in line['tags']:
            attrs.append('dark')
        if 'important' in line['tags']:
            print(colored(line['line'], 'white', 'on_red', attrs=attrs))
            continue
        if 'error' in line['tags']:
            print(colored(line['line'], 'red', attrs=attrs))
            continue
        if 'warn' in line['tags']:
            print(colored(line['line'], 'yellow', attrs=attrs))
            continue
        else:
            print(colored(line['line'], attrs=attrs))

if __name__ == '__main__':
    main()
