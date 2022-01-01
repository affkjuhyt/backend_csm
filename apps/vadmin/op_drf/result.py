def funcSuccess(data=None, msg='success', **kwargs):
    """
    :param data:
    :param msg:
    :return:
    """
    return {
        "result": True,
        "msg": msg,
        "data": data,
    }


def funcError(data=None, msg='error', **kwargs):
    """
    :param data:
    :param msg:
    :return:
    """
    return {
        "result": False,
        "msg": msg,
        "data": data,
    }


def funcResult(result=True, data=None, msg='success', **kwargs):
    """
    :param result:
    :param data:
    :param msg:
    :return:
    """
    if result:
        return funcSuccess(data=data, msg=msg)
    return funcError(data=data, msg=msg)


def paginate(data=None, count=0, next=None, previous=None, msg='success', code=2000):
    """
    :param data: 默认为[]
    :param count: 默认为len(data); 总计值, 不是data的元素个数,相当于count(*);仅当不传入count时, count==len(data)
    :param next: 默认为None, 下一页
    :param previous: 默认为None, 上一页
    :param msg: 默认为success
    :param code: 默认为2000, 建议不传入参数,使用默认即可
    :return:
    """
    if not data:
        data = []
    if not count:
        count = len(data)
    return {
        "code": code,
        "data": {
            "count": count,
            "next": next,
            "previous": previous,
            "results": data
        },
        "msg": msg,
        "status": "success"
    }
