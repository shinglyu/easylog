import re
import easylog


def test_segments():
    segment_rules = [
        {'regex': re.compile(r"(#[0-9]*)(.*)( in )([^\)]*)(\(.*\))( at )(.*)", re.IGNORECASE), 'tags': {
            0: ['bt_id'],
            1: ['address'],
            2: [],  # in
            3: ['func'],
            4: ['func_args'],
            5: [],  # at
            6: ['filename']
        }}
    ]
    smart_rules = []
    pattern = []

    line = "#6  0x00007f90249d8a2a in nsStyleSet::ResolveStyleFor(mozilla::dom::Element*, nsStyleContext*, TreeMatchContext&) (this=0x7f8fef2fc420, aElement=0x7f8fe4571230, aParentContext=0x7f8fef19d6b0, aTreeMatchContext=...) at /home/shinglyu/workspace/stylo/mozilla-central/layout/style/nsStyleSet.cpp:1406"
#7  0x00007f9024ad09d4 in nsStyleSet::ResolveStyleFor(mozilla::dom::Element*, nsStyleContext*, mozilla::LazyComputeBehavior, TreeMatchContext&) (this=0x7f8fef2fc420, aElement=0x7f8fe4571230, aParentContext=0x7f8fef19d6b0, aMayCompute=mozilla::LazyComputeBehavior::Assert, aTreeMatchContext=...)
#    at /home/shinglyu/workspace/stylo/mozilla-central/layout/style/nsStyleSet.h:135
    expected = [{
        "line": line,
        "tags": [],
        "segments": [
            {'text': "#6", 'tags': ['bt_id']},
            {'tags': ['address'], 'text': '  0x00007f90249d8a2a'},
            {'tags': [], 'text': ' in '},
            {'tags': ['func'], 'text': 'nsStyleSet::ResolveStyleFor'},
            {'tags': ['func_args'],
                'text': '(mozilla::dom::Element*, nsStyleContext*, TreeMatchContext&) (this=0x7f8fef2fc420, aElement=0x7f8fe4571230, aParentContext=0x7f8fef19d6b0, aTreeMatchContext=...)'},
            {'tags': [], 'text': ' at '},
            {'tags': ['filename'],
                'text': '/home/shinglyu/workspace/stylo/mozilla-central/layout/style/nsStyleSet.cpp:1406'}
        ]
    }]

    actual = easylog.process_lines([line], pattern)
    assert expected == actual

def test_segments_no_match():
    segment_rules = [
        {'regex': re.compile(r"(#[0-9]*)(.*)( in )([^\)]*)(\(.*\))( at )(.*)", re.IGNORECASE), 'tags': {
            0: ['bt_id'],
            1: ['address'],
            2: [],  # in
            3: ['func'],
            4: ['func_args'],
            5: [],  # at
            6: ['filename']
        }}
    ]
    smart_rules = []
    pattern = []

    line = "Foo"
    expected = [{
        "line": line,
        "tags": [],
    }]

    actual = easylog.process_lines([line], pattern)
    assert expected == actual
