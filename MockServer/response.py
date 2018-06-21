VALID = {
    "success": True,
    "code": "0000",
    "msg": "success"
}

INVALID = {
    'code': '0020',
    'msg': 'request data invalid',
    'success': False
}

MISS = {
    'code': '0021',
    'msg': 'request data missed',
    'success': False
}

TYPE_NOT_MATCH = {
    "success": False,
    "code": "0001",
}

EQUALS = {
    "success": False,
    "code": "0005",
}

NOT_BETWEEN = {
    "success": False,
    "code": "0007",
}

STR_NOT_CONTAINS = {
    "success": False,
    "code": "0004",
}

STR_TOO_LONG = {
    "success": False,
    "code": "0006",
}
