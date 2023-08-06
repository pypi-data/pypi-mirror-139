#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
参考drf JSONRenderer/ HumpJSONRenderer

"""
from humplib.tools import json_underline2hump


def hump_json_renderer_str(data: dict=None)->str:
    """
    Convert to camel case and use double quotes
    1
    b'{"a": 1,"aB": 1}'

    :param data:
    :return:
    """
    ret = json_underline2hump(json_obj=data)
    # We always fully escape \u2028 and \u2029 to ensure we output JSON
    # that is a strict javascript subset.
    # See: http://timelessrepo.com/json-isnt-a-javascript-subset
    ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return ret


def hump_json_renderer_byte(data: dict=None):
    """

    :param data:
    :return:
    """
    ret_str = hump_json_renderer_str(data=data)
    return ret_str.encode()


def main():
    data = {
        'name': 'compile',
        'params': {
            'bdg': '1758431528494305280',
            'is_publish': True,
            'token': 'aa.bb.Fx93qRLDHsrQPp8ab1C6Lg4_pnM'
        }
    }
    ret = hump_json_renderer_str(data)
    print(ret)
    pass


if __name__ == '__main__':
    main()

