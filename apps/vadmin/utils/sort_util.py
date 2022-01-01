import operator
from collections import Iterable


def sortSimpleTypeList(li, reverse=False):
    """
    :param li:
    :param reverse:
    :return:
    """
    li.sort()
    if reverse:
        li.reverse()
    return li


def sortObjectList(obj_list, by_prop):
    """
    :param obj_list:
    :param by_prop:
    :return:
    """
    reverse = False
    if by_prop.startswith('-'):
        reverse = True
        by_prop = by_prop[1:]
    fun = operator.attrgetter(by_prop)
    obj_list.sort(key=fun)
    if reverse:
        obj_list.reverse()
    return obj_list


def sortDictList(dict_list, by_key):
    """
    :param dict_list:
    :param by_key:
    :return:
    """
    reverse = False
    if by_key.startswith('-'):
        reverse = True
        by_key = by_key[1:]
    dict_list.sort(key=lambda ele: ele[by_key])
    if reverse:
        dict_list.reverse()
    return dict_list


def sortList(li, by=''):

    reverse = False
    if not li or not isinstance(li, Iterable):
        return li
    if by.startswith('-'):
        reverse = True
    if isinstance(li[0], (int, float, str)):
        return sortSimpleTypeList(li, reverse)
    if not by:
        return li
    if isinstance(li[0], dict):
        return sortDictList(li, by)
    return sortObjectList(li, by)
