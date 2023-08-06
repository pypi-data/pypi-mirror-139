#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@Time    :2022/1/12 15:20
# !@Author  : murInj
# !@Filer    : .py
import json
import os
import time
import traceback


class baseEnv:
    def __init__(self,rd=1):
        self.__board = None  # 设置空棋盘的形状格式
        self.__turn = None  # 设置回合方
        self.buffer = None  # 设置行棋历史
        self.done = False
        self.winner = None
        self.AI1 = None
        self.AI2 = None
        self.terminalInfo = list()
        self.bufferUnit = None
        self.round = rd
        self.score = None

        if not os.path.exists('./log'):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs('./log')  # makedirs 创建文件时如果路径不存在会创建这个路径
            print('创建log文件夹')

    def getActionSpace(self):
        """
        获取行动空间
        :return: 行动空间
        """
        raise Exception("未重写getActionSpace")

    def getObserveSpace(self):
        """
        获取观测空间
        :return: 观测空间
        """
        raise Exception("未重写getObserveSpace")

    def getAction(self):
        """
        采取行动
        :return:返回行动值
        """
        return None

    def step(self, action=None):
        """
        行动一步
        :param action: 行动
        :return: 行动后的状态
        """
        raise Exception("未重写step")


    def gender(self, genderMethod=None):
        """
        用于显示棋局,可自定义用UI或者命令行
        :param genderMethod: 显示方法,默认None则为不显示
        :return:
        """
        pass

    def reset(self):
        """
        重置棋局
        :return: None
        """
        raise Exception("未重写reset")

    def beforeUpdate(self):
        """
        采取行动前的棋盘更新
        :return:
        """
        pass

    def afterUpdate(self):
        pass

    def gameoverUpdate(self):
        """
        一轮棋局结束后的处理函数
        :return:
        """
        pass

    def addBuffer(self):
        """
        添加行棋记录
        :return:
        """
        pass

    def oneRound(self):
        """
        完整的进行一轮棋局
        :return: 返回终局信息
        """
        try:
            self.reset()
            self.gender()
            while not self.done:
                self.beforeUpdate()
                action = self.getAction()
                self.step(action)
                self.gender()
                self.addBuffer()
                self.afterUpdate()
            self.gameoverUpdate()
        except Exception as result:
            print(result)
            traceback.print_exc()

    def log(self):
        self.terminalInfo.append({'score':self.score})
        fileName = './log/' + str(time.time())[0:10] + '.json'
        json_str = json.dumps(tuple(self.terminalInfo))
        with open(fileName, 'w') as json_file:
            json_file.write(json_str)
        print('对战日志记录成功')

    def run(self):
        for step in range(self.round):
            self.oneRound()
        print("team1 score:", self.score[0],"\nteam2 score:", self.score[1])
        self.log()
