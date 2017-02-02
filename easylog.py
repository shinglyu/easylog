import argparse
import re
import json
import sys

# TODO: read the patterns from config file
patterns = [
    {'regex': re.compile(r'.*ERROR.*'), 'tags': ['error']},
    {'regex': re.compile(r'.*Assertion failure.*'), 'tags': ['error']},
    {'regex': re.compile(r'.*WARNING.*'), 'tags': ['warn']},
    {'regex': re.compile(r'.*received signal 11.*'), 'tags': ['important']},
    {'regex': re.compile(r'.*Assertion failure.*'), 'tags': ['important','error']},
]

def main():
    parser = argparse.ArgumentParser(description='Convert raw log to JSON format with tags')
    parser.add_argument('filename', type=argparse.FileType("r"),
                        help='the log file')

    args = parser.parse_args()

    lines = args.filename.readlines()
    args.filename.close()

    json = process_lines(lines, patterns)
    # print(json)
    sys.stdout.write(json)

def process_lines(lines, patterns):
    output = []
    for line in lines:
        line_tags = []
        for pattern in patterns:
            if pattern['regex'].match(line):
                line_tags.extend(pattern['tags'])
        output.append({'line': line, 'tags':line_tags})

    return json.dumps(output)

if __name__ == '__main__':
    main()
