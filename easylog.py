import argparse
import re
import json
import sys

# TODO: read the patterns from config file
patterns = [
    {'regex': re.compile(r'.*ERROR.*', re.IGNORECASE), 'tags': ['error']},
    {'regex': re.compile(r'.*WARNING.*', re.IGNORECASE), 'tags': ['warn']},
    {'regex': re.compile(r'.*received signal 11.*'), 'tags': ['important']},
    {'regex': re.compile(r'.*ASSERTION.*', re.IGNORECASE), 'tags': ['important','error']},
    {'regex': re.compile(r'^#[0-9]*', re.IGNORECASE), 'tags': ['bt-line']},
# Reftest
    {'regex': re.compile(r'^REFTEST TEST-LOAD', re.IGNORECASE), 'tags': ['casename']},
    {'regex': re.compile(r'TEST-UNEXPECTED-FAIL', re.IGNORECASE), 'tags': ['error']},
    {'regex': re.compile(r'^REFTEST PROCESS-CRASH', re.IGNORECASE), 'tags': ['error']},
    {'regex': re.compile(r'^REFTEST TEST-END', re.IGNORECASE), 'tags': ['casename']},

]

def too_many_times(line, lines):
    # This is very slow to repeat every time, but we keep it like this for
    # simplicity of the smart_rules list
    return lines.count(line) > 10

def line_too_long(line, lines):
    # This is very slow to repeat every time, but we keep it like this for
    # simplicity of the smart_rules list
    return len(line) > 600

smart_rules = [
    # {'filter': too_many_times, 'tags': ['frequent']},
    {'filter': line_too_long, 'tags': ['too-long']},
]

segment_rules = [
    {'regex': re.compile(r"(#[0-9]*)(.*)( in )([^\)]*)(\(.*\))( at )(.*)", re.IGNORECASE), 'tags': {
        0: ['bt_id'],
        1: ['address'],
        2: [],  # in
        3: ['func'],
        4: ['func_args'],
        5: [],  # at
        6: ['filename']
    }},
    {'regex': re.compile(r"(#[0-9]*)(.*)( in )([^\)]*)(\(.*\))", re.IGNORECASE), 'tags': {
        0: ['bt_id'],
        1: ['address'],
        2: [],  # in
        3: ['func'],
        4: ['func_args'],
    }},
    {'regex': re.compile(r"(\s*at )(.*)", re.IGNORECASE), 'tags': {
        0: [],  # at
        1: ['filename']
    }},
]

def main():
    parser = argparse.ArgumentParser(description='Convert raw log to JSON format with tags')
    parser.add_argument('filename', type=argparse.FileType("r"),
                        help='the log file')

    args = parser.parse_args()

    lines = args.filename.readlines()
    args.filename.close()

    #            don't need this vvvvvv
    processed_lines = process_lines(lines, patterns)
    # print(json)
    sys.stdout.write(json.dumps(processed_lines))

# FIXME: pass the patternn and rules through arguments
def process_lines(lines, patterns):
    output = []
    for line in lines:
        line_tags = []
        segments = []
        for pattern in patterns:
            if pattern['regex'].match(line):
                line_tags.extend(pattern['tags'])
        for rule in smart_rules:
            if rule['filter'](line, lines):
                line_tags.extend(rule['tags'])
        for rule in segment_rules:
            # Only match the first fit
            matches = rule['regex'].findall(line)
            if matches and len(matches[0]) > 0:
                for idx, segment in enumerate(matches[0]):
                    segments.append({'text': segment, 'tags': rule['tags'][idx]})
                break

        if segments:
            output.append({'line': line.rstrip(),
                           'tags': line_tags,
                           'segments': segments}) # Trim newline
        else:
            output.append({'line': line.rstrip(),
                           'tags': line_tags})

    return output

if __name__ == '__main__':
    main()
