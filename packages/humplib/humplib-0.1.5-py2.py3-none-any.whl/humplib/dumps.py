#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""
import json

UNICODE_JSON = True,
COMPACT_JSON = True,

# `separators` argument to `json.dumps()` differs between 2.x and 3.x
# See: https://bugs.python.org/issue22767
SHORT_SEPARATORS = (',', ':')
LONG_SEPARATORS = (', ', ': ')
INDENT_SEPARATORS = (',', ': ')


def dumps(data, indent=None,
          ensure_ascii=UNICODE_JSON,
          allow_nan=not COMPACT_JSON,
          separators=INDENT_SEPARATORS,
          )->str:
    json_str = json.dumps(
        data, cls=json.JSONEncoder,
        indent=indent,
        ensure_ascii=ensure_ascii,
        allow_nan=allow_nan,
        separators=separators
    )
    return json_str


def main():
    data = {
        'name': 'compile',
        'params': {
            'bdg': '1758431528494305280',
            'is_publish': True,
            'token': 'aa.bb.Fx93qRLDHsrQPp8ab1C6Lg4_pnM'
        }
    }
    ret = dumps(data)
    print(ret)
    pass


if __name__ == '__main__':
    main()
