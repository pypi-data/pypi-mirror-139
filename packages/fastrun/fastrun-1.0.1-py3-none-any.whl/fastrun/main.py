#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 13:48
# @Author  : Lifeng
# @Site    : 
# @File    : main.py
# @Software: PyCharm

import argparse
from fastrun.android.script import StabilityTestAndroid

__all__ = ["running"]


def running():
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", type=str, help="包名-必传参数")
    parser.add_argument("-m", "--minute", type=int, help="设置分钟-可选参数 固定值 [10, 15, 20, 25, 30]")
    args = parser.parse_args()

    time_quantum = [10, 15, 20, 25, 30]

    if args.minute:
        if args.minute in time_quantum:
            minute = args.minute
        else:
            raise Exception("可选参数不正确，只允许[10, 15, 20, 25, 30]")
    else:
        minute = 5

    return StabilityTestAndroid(args.packages).execute(parameter=minute)

