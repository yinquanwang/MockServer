from flask import request, json

from MockServer.response import VALID, TYPE_NOT_MATCH, EQUALS, NOT_BETWEEN, STR_NOT_CONTAINS, STR_TOO_LONG, MISS, \
    INVALID


def get_response(response, actual):
    return json.dumps(response, ensure_ascii=False) if response else json.dumps(actual, ensure_ascii=False)


class Validator:
    """
    Validator for mock check
    """

    @classmethod
    def valid(cls, response=None):
        return get_response(response, VALID)

    @classmethod
    def type_not_match(cls, type, data, response=None):
        msg = '{data} must be {type} type'.format(data=data, type=type)
        TYPE_NOT_MATCH['msg'] = msg
        if type == 'int':
            if not isinstance(data, int):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'float':
            if not isinstance(data, float):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'string':
            if not isinstance(data, str):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'bool':
            if not isinstance(data, bool):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'list':
            if not isinstance(data, list):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'dict':
            if not isinstance(data, dict):
                return get_response(response, TYPE_NOT_MATCH)
        else:
            return False

    @classmethod
    def is_not_equals(cls, data, expect, response=None):
        if data != expect:
            msg = '{data} must be equals {expect}'.format(data=data, expect=expect)
            EQUALS['msg'] = msg
            return get_response(response, EQUALS)
        else:
            return False

    @classmethod
    def is_not_between(cls, data, between, response=None):
        try:
            min = between[0]
            max = between[1]
        except IndexError:
            return {'msg': 'mock config error'}
        if data > max or min < min:
            msg = '{data} must be between in {between}'.format(data=data, between=between)
            NOT_BETWEEN['msg'] = msg
            return get_response(response, NOT_BETWEEN)
        else:
            return False

    @classmethod
    def is_not_contains(cls, data, expect, response=None):
        if data not in expect:
            msg = '{data} not in {expect}'.format(data=data, expect=expect)
            STR_NOT_CONTAINS['msg'] = msg
            return get_response(response, STR_NOT_CONTAINS)
        else:
            return False

    @classmethod
    def is_too_long(cls, data, length, response=None):
        if len(data) > length:
            msg = '{data} is  too long, max length is {length}'.format(data=data, length=length)
            STR_TOO_LONG['msg'] = msg
            return get_response(response, STR_TOO_LONG)
        else:
            return False


def domain_server(**kwargs):
    """
    used for POST PUT DELETE
    :param kwargs: standard json mock scripts
    :return: response msg
    """
    data = kwargs.get('data', {})
    invalid = kwargs.get('invalid', {})

    if request.json:
        form = request.json

    elif request.form:
        form = request.form

    elif request.args:
        form = request.args

    if data is {}:  # do not have any parameters
        return Validator.valid(response=kwargs.get('valid'))

    else:
        if len(form) != len(data):  # data do not matched
            return json.dumps(MISS, ensure_ascii=False)

        for key in form.keys():
            if key not in data.keys():
                return json.dumps(INVALID, ensure_ascii=False)

        for key, value in form.items():  # usually validators
            expect = data.get(key)
            type = expect.get('type')
            msg = Validator.type_not_match(type, value, response=invalid.get('type'))
            if msg:
                return msg

            contains = expect.get('contains')
            if contains:
                msg = Validator.is_not_contains(value, contains, response=invalid.get('contains'))
                if msg:
                    return msg

            equals = expect.get('equals')
            if equals:
                msg = Validator.is_not_equals(value, equals, response=invalid.get('equals'))
                if msg:
                    return msg

            long = expect.get('long')
            if long:
                msg = Validator.is_too_long(value, long, response=invalid.get('length'))
                if msg:
                    return msg

            between = expect.get('between')
            if between:
                msg = Validator.is_not_between(value, between, response=invalid.get('between'))
                if msg:
                    return msg

        return Validator.valid(response=kwargs.get('valid'))
