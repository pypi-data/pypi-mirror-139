#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@Time    :2022/2/18 17:03
# !@Author  : murInj
# !@Filer    : .py
import random
def random_aenstein(Env):
    actionSpace = Env.getActionSpace()
    index = random.randint(0, len(actionSpace[0]) - 1)
    return [actionSpace[0][index], actionSpace[1][index]]

def random_tictactoe(Env):
    actionSpace = Env.getActionSpace()
    index = random.randint(0, len(actionSpace) - 1)
    return [actionSpace[index][0], actionSpace[index][1]]

randomMethod = {"aenstein" : random_aenstein,"tictactoe" : random_tictactoe}