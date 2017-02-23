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
        # Hide the repeated lines
        if line == prev_line:
            repeat_count += 1
            continue # Skip printing
        else:
            if repeat_count > 0:
                print(colored("(Repeats {0} times)".format(repeat_count), attrs=["dark"]))
            repeat_count = 0
            prev_line = line

        # Handling lines with segments
        if 'segments' in line:
            for segment in line['segments']:
                # Use sys.stdout.write to supress space added by print
                # Consider using print('foo', end='') from python 3
                if 'bt_id' in segment['tags']:
                    sys.stdout.write(colored(segment['text'], 'blue', attrs=[]))
                    continue
                if 'address' in segment['tags']:
                    sys.stdout.write(colored(segment['text'], 'white', attrs=['dark']))
                    continue
                if 'func' in segment['tags']:
                    sys.stdout.write(colored(segment['text'], 'yellow', attrs=[]))
                    continue
                if 'func_args' in segment['tags']:
                    sys.stdout.write(colored(segment['text'], 'green', attrs=['dark']))
                    continue
                if 'filename' in segment['tags']:
                    sys.stdout.write(colored(segment['text'], 'cyan', attrs=['dark']))
                    continue
                sys.stdout.write(segment['text']),
            print("")  # new line
            continue

        # Handling full lines
        attrs = []
        if 'frequent' in line['tags']:
            attrs.append('dark')
        if 'too-long' in line['tags']:
            print(colored(line['line'][:600] +
                          "...({0} columns omitted)".format(len(line['line'][600:])),
                          attrs=attrs))
            continue
        if 'important' in line['tags']:
            print(colored(line['line'], 'white', 'on_red', attrs=attrs))
            continue
        if 'error' in line['tags']:
            print(colored(line['line'], 'red', attrs=attrs))
            continue
        if 'warn' in line['tags']:
            print(colored(line['line'], 'yellow', attrs=attrs))
            continue
        if 'bt-line' in line['tags']:
            print(colored(line['line'], 'green', attrs=attrs))
            continue
        if 'casename' in line['tags']:
            print(colored(line['line'], 'green', attrs=attrs))
            continue
        else:
            print(colored(line['line'], attrs=attrs))

if __name__ == '__main__':
    main()
