#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@Time    :2022/2/18 17:13
# !@Author  : murInj
# !@Filer    : .py
import random
from chessEnv import baseEnv
from chessEnv import AI
class tictactoeEnv(baseEnv.baseEnv):
    def __init__(self, rd=1,firstHandMethod=0,boardMethod=0,AI1=None, AI2=None):
        super().__init__(rd=rd)
        self.__board = [[0] * 3 for _ in range(3)]  # 3*3棋盘 X,1为team1,O,2为team2
        self.__turn = None  # 回合方["team1", "team2"]
        self.done = False
        self.round = rd
        self.score = [0,0]
        self.firstHandMethod = firstHandMethod
        self.boardMethod = boardMethod
        self.AI1 = AI1
        self.AI2 = AI2



    # override
    def reset(self, boardMethod=None, firstHandMethod=None, board=None, rd=None,
              fristHand=None, AI1=None, AI2=None):
        self.done = False
        if rd is not None:
            self.round = rd
        # 初始化AI###################################
        if AI1 is not None:
            self.AI1 = AI1
        if AI2 is not None:
            self.AI2 = AI2
        ############################################
        # 初始化棋盘##################################
        if boardMethod is not None:
            self.boardMethod = boardMethod
        if self.boardMethod == 0:
            self.__board = [[0] * 3 for _ in range(3)]
        elif self.boardMethod == 1:
            # 人工输入board
            print("请输入棋盘")
            for i in range(3):
                for j in range(3):
                    self.__board[i][j] = input()
        elif self.boardMethod == 2:
            # TODO:传入board数组
            pass
        else:
            raise Exception("boardMethod值有误!")
        #############################################
        # 初始化先手###################################
        if firstHandMethod is not None:
            self.firstHandMethod = firstHandMethod
        if self.firstHandMethod == 0:
            self.__turn = random.choice(['team1', 'team2'])
        elif self.firstHandMethod == 1:
            self.__turn = input("请输入先手")
        elif self.firstHandMethod == 2:
            # TODO:传入先手turn
            pass
        else:
            raise Exception("firstHandMethod值有误!")
        #############################################

        # 重置缓冲区##################################
        self.buffer = list()
        self.bufferUnit = dict()
        ############################################

    # override
    def getObserveSpace(self):
        """
        获得观测空间
        返回[board,turn,dice,team1_score,team2_score]
        :return:
        """
        return [self.__board, self.__turn, self.score,self.buffer]

    # override
    def getActionSpace(self):
        return tictactoeEnv.getPossibleChess(self.__board)

    # override
    def step(self, action=None):
        if action is None:
            action = AI.randomMethod['tictactoe'](self)

        # 移动################################

        # 棋子合法判断
        if not tictactoeEnv.isLegalMove(self.__board,action):
            raise Exception("非法操作！")

        # 构造缓冲单元
        self.bufferUnit['board'] = self.__board
        self.bufferUnit['opr'] = action

        self.__board[action[0]][action[1]] = (1 if self.__turn == 'team1' else 2)

        self.done, self.winner = tictactoeEnv.isTerminal(self.__board)
        #####################################

    # override
    def gender(self, genderMethod=0):
        # 文本显示
        if genderMethod == 0:
            for row in range(3):
                for col in range(3):
                    print("{:^5}".format(int(self.__board[row][col])), end=" ")
                print("")
        # TODO:图形界面显示
        elif genderMethod == 1:
            pass

        # override

    def beforeUpdate(self):
        # 显示对战信息###############################
        print("回合方: ", self.__turn)
        print("-----------------------")
        ###########################################
        # 重置缓存单元###############################
        self.bufferUnit = dict()
        ##########################################

    # override
    def addBuffer(self):
        self.buffer.append(self.bufferUnit)

    # override
    def afterUpdate(self):
        self.__turn = self.__turn == "team1" and "team2" or "team1"
        self.bufferUnit['turn'] = self.__turn

    # override
    def gameoverUpdate(self):
        self.winner = self.isTerminal(self.__board)[1]
        print("-----------------------")
        print("胜利方:",self.winner)
        print("-----------------------")

        self.buffer.pop()
        self.buffer.append(self.winner)
        if self.winner == 'team1':
            self.score[0] += 0.5
            self.score[1] -= 0.1
        elif self.winner == 'team2':
            self.score[1] += 0.5
            self.score[0] -= 0.1
        else:
            self.score[0] += 0.1
            self.score[1] += 0.1
        self.terminalInfo.append(self.buffer)

    #override
    def getAction(self):
        if self.__turn == 'team1':
            if self.AI1 is None:
                return None
            return self.AI1(self.getObserveSpace())
        else:
            if self.AI2 is None:
                return None
            return self.AI2(self.getObserveSpace())

    @staticmethod
    def getPossibleChess(board):
        possChess = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    possChess.append([i,j])
        return possChess

    @staticmethod
    def isLegalMove(board,loc):
        if 0 <= loc[0] <= 2 and 0 <= loc[1] <= 2 and board[loc[0]][loc[1]] == 0:
            return True
        else:
            return False

    @staticmethod
    def isTerminal(board):
        for i in range(3):
            if board[i][0] != 0 and board[i][1] != 0 and board[i][2] != 0 \
            and board[i][0] == board[i][1] == board[i][2]:
                return [True, ('team1' if board[i][0] == 1 else 'team2')]
            if board[0][i] != 0 and board[1][i] != 0 and board[2][i] != 0 \
            and board[0][i] == board[1][i] == board[2][i]:
                return [True, ('team1' if board[0][i] == 1 else 'team2')]
        if board[0][0] != 0 and board[1][1] != 0 and board[2][2] != 0 \
        and board[0][0] == board[1][1] == board[2][2]:
            return [True, ('team1' if board[0][0] == 1 else 'team2')]
        if board[0][2] != 0 and board[1][1] != 0 and board[2][0] != 0 \
        and board[0][2] == board[1][1] == board[2][0]:
            return [True, ('team1' if board[2][0] == 1 else 'team2')]

        cnt = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] != 0:
                    cnt += 1
        if cnt == 9:
            return [True,None]
        return [False,None]