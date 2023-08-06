#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
参考drf JSONRenderer/ HumpJSONRenderer

"""
import json

from humplib import underline2hump

UNICODE_JSON = True,
COMPACT_JSON = True,

# `separators` argument to `json.dumps()` differs between 2.x and 3.x
# See: https://bugs.python.org/issue22767
SHORT_SEPARATORS = (',', ':')
LONG_SEPARATORS = (', ', ': ')
INDENT_SEPARATORS = (',', ': ')


def hump_json_renderer(data, indent=None,
                       ensure_ascii=UNICODE_JSON,
                       allow_nan=not COMPACT_JSON,
                       separators=INDENT_SEPARATORS,
                       ):
    """
    Convert to camel case and use double quotes
    1
    b'{"a": 1,"aB": 1}'

    :param data:
    :param indent:
    :param ensure_ascii:
    :param allow_nan:
    :param separators:
    :return:
    """
    ret = json.dumps(
        data, cls=json.JSONEncoder,
        indent=indent,
        ensure_ascii=ensure_ascii,
        allow_nan=allow_nan,
        separators=separators
    )
    ret = underline2hump(ret)

    # We always fully escape \u2028 and \u2029 to ensure we output JSON
    # that is a strict javascript subset.
    # See: http://timelessrepo.com/json-isnt-a-javascript-subset
    ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return ret.encode()


def main():
    data = {
        "a": 1,
        "a_b": 1
    }
    ret = hump_json_renderer(data)
    print(ret)
    pass


if __name__ == '__main__':
    main()

