#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 1:18
# @Author  : 张大鹏
# @Site    : 
# @File    : exceptions.py
# @Software: PyCharm

class FastAPIError(Exception):
    def __init__(self, *args):
        super(FastAPIError, self).__init__(*args)

class ParamError(FastAPIError):
    def __init__(self, *args):
        super(FastAPIError, self).__init__(*args)
