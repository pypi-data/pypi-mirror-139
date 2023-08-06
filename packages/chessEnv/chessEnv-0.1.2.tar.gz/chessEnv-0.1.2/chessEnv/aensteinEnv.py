#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@Time    :2022/1/12 17:24
# !@Author  : murInj
# !@Filer    : .py
import copy
import random
from chessEnv import baseEnv
from chessEnv import AI

class aensteinEnv(baseEnv.baseEnv):
    def __init__(self,rd=1,boardMethod=0, firstHandMethod=0,
                 diceMethod1=0,diceMethod2=0,AI1=None,AI2=None):
        super().__init__(rd=rd)
        self.__board = [[0] * 5 for _ in range(5)]  # 5*5棋盘 正数为team1,负数为team2
        self.__dice = 0  # 骰子[1,2,3,4,5,6]
        self.__turn = None  # 回合方["team1", "team2"]
        self.diceMethod1 = diceMethod1
        self.diceMethod2 = diceMethod2
        self.done = False
        self.round = rd
        self.boardMethod = boardMethod
        self.firstHandMethod = firstHandMethod
        self.AI1 = AI1
        self.AI2 = AI2
        self.score = [0,0]

    # override
    def reset(self, boardMethod=None, firstHandMethod=None, board=None, rd=None,
              team_loc=None, fristHand=None, diceMethod1=None, diceMethod2=None, AI1=None, AI2=None):
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
        self.__board = [[0] * 5 for _ in range(5)]
        if boardMethod is not None:
            self.boardMethod = boardMethod
        if self.boardMethod == 0:
            # 随机初始化board
            team1 = [1, 2, 3, 4, 5, 6]
            team2 = [-1, -2, -3, -4, -5, -6]
            # 打乱顺序
            random.shuffle(team1)
            random.shuffle(team2)

            # 给左边初始化
            index = 0
            for i in range(3):
                for j in range(3 - i):
                    self.__board[i][j] = team1[index]
                    index += 1

            # 给右边初始化
            index = 0
            temp = 0
            for i in range(2, 5):
                for j in range(4 - temp, 5):
                    self.__board[i][j] = team2[index]
                    index += 1
                temp += 1
        elif self.boardMethod == 1:
            # 人工输入board
            print("请输入棋盘")
            for i in range(5):
                for j in range(5):
                    self.__board[i][j] = int(input())
        elif self.boardMethod == 2:
            # TODO:传入board数组
            pass
        else:
            raise Exception("boardMethod值有误!")
        #############################################
        # 骰子方法####################################
        if diceMethod1 is not None:
            self.diceMethod1 = diceMethod1
        if diceMethod2 is not None:
            self.diceMethod2 = diceMethod2
        ############################################
        # 初始化先手###################################
        if firstHandMethod is not None:
            self.firstHandMethod = firstHandMethod
        if self.firstHandMethod == 0:
            self.__turn = random.choice(['team1','team2'])
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
        return [self.__board, self.__turn, self.__dice, self.score,self.buffer]

    # override
    def getActionSpace(self):
        return aensteinEnv.getPossibleChess(self.__board, self.__turn, self.__dice)

    # override
    def step(self, action=None):
        if action is None:
            action = AI.randomMethod['aenstein'](self)

        # 移动################################
        row = col = -1
        chess = action[0]
        opr = action[1]
        newBoard = copy.deepcopy(self.__board)

        # 扫描棋盘位置
        for i in range(5):
            for j in range(5):
                if (self.__turn == 'team1' and newBoard[i][j] == chess) or \
                        (self.__turn == 'team2' and newBoard[i][j] == -chess):
                    row = i
                    col = j

        # 棋子合法判断
        if self.__dice != 0:
            if not aensteinEnv.isLegalChess(chess, self.__turn, newBoard, self.__dice):
                raise Exception("移动非法！非合法棋子！")
            if opr != 'vertical' and opr != 'transverse' and opr != 'oblique':
                raise Exception("错误操作！")

        # 构造缓冲单元
        self.bufferUnit['board'] = newBoard
        self.bufferUnit['chess'] = action[0]
        self.bufferUnit['opr'] = action[1]


        # 竖向移动
        if opr == 'vertical':
            # 上移
            if self.__turn == 'team2':
                if not aensteinEnv.isLegalMove(row - 1, col):
                    raise Exception("移动非法，越界！")
                else:
                    newBoard[row - 1][col] = newBoard[row][col]
                    newBoard[row][col] = 0
            # 下移
            elif self.__turn == 'team1':
                if not aensteinEnv.isLegalMove(row + 1, col):
                    raise Exception("移动非法，越界！")
                else:
                    newBoard[row + 1][col] = newBoard[row][col]
                    newBoard[row][col] = 0

        # 横向移动
        elif opr == 'transverse':
            # 左移
            if self.__turn == 'team2':
                if not aensteinEnv.isLegalMove(row, col - 1):
                    raise Exception("移动非法，越界！")
                else:
                    newBoard[row][col - 1] = newBoard[row][col]
                    newBoard[row][col] = 0
            # 右移
            elif self.__turn == 'team1':
                if not aensteinEnv.isLegalMove(row, col + 1):
                    raise Exception("移动非法，越界！")
                else:
                    newBoard[row][col + 1] = newBoard[row][col]
                    newBoard[row][col] = 0

        # 斜向移动
        elif opr == 'oblique':
            # 左上移
            if self.__turn == 'team2':
                if not aensteinEnv.isLegalMove(row - 1, col - 1):
                    raise Exception("移动非法，越界！")
                else:
                    newBoard[row - 1][col - 1] = newBoard[row][col]
                    newBoard[row][col] = 0
            # 右下移
            elif self.__turn == 'team1':
                if not aensteinEnv.isLegalMove(row + 1, col + 1):
                    raise Exception("移动非法，越界！")
                else:
                    newBoard[row + 1][col + 1] = newBoard[row][col]
                    newBoard[row][col] = 0

        self.__board = newBoard
        self.done, self.winner = aensteinEnv.isTerminal(newBoard)
        #####################################

    # override
    def gender(self,genderMethod=0):
        # 文本显示
        if genderMethod == 0:
            for row in range(5):
                for col in range(5):
                    print("{:^5}".format(int(self.__board[row][col])), end=" ")
                print("")
        # TODO:图形界面显示
        elif genderMethod == 1:
            pass

    # override
    def beforeUpdate(self):
        # 摇骰子#####################################
        if self.__turn == 'team1':
            # 随机摇
            if self.diceMethod1 == 0:
                self.__dice = random.randint(1,6)
        else:
            # 随机摇
            if self.diceMethod1 == 0:
                self.__dice = random.randint(1,6)
        ###########################################

        # 显示对战信息###############################
        print("回合方: ",self.__turn)
        print("骰子数: ",self.__dice)
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
            self.score[0] += 1
        elif self.winner == 'team2':
            self.score[1] += 1
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
    def getPossibleChess(board, turn, dice=0):
        """
        获取所有可能行动，传入dice值则进行限制，不传入则返回所有己方棋子的可能走法
        Args:
            dice: 输入dice则采用有dice的所有可能，不输入则采用无dice的所有可能
            board:
            turn:

        Returns: 二维数组，一维为棋子，二维为行动

        """
        possibleChess = [[], []]
        for i in range(len(board)):
            for j in range(len(board[0])):
                if turn == 'team1' and board[i][j] > 0 and \
                        (dice == 0 and True or aensteinEnv.isLegalChess(board[i][j], turn, board, dice)):
                    if aensteinEnv.isLegalMove(i + 1, j):
                        possibleChess[0].append(board[i][j])
                        possibleChess[1].append("vertical")
                    if aensteinEnv.isLegalMove(i, j + 1):
                        possibleChess[0].append(board[i][j])
                        possibleChess[1].append("transverse")
                    if aensteinEnv.isLegalMove(i + 1, j + 1):
                        possibleChess[0].append(board[i][j])
                        possibleChess[1].append("oblique")
                elif turn == 'team2' and board[i][j] < 0 and \
                        (dice == 0 and True or aensteinEnv.isLegalChess(-board[i][j], turn, board, dice)):
                    if aensteinEnv.isLegalMove(i - 1, j):
                        possibleChess[0].append(-board[i][j])
                        possibleChess[1].append("vertical")
                    if aensteinEnv.isLegalMove(i, j - 1):
                        possibleChess[0].append(-board[i][j])
                        possibleChess[1].append("transverse")
                    if aensteinEnv.isLegalMove(i - 1, j - 1):
                        possibleChess[0].append(-board[i][j])
                        possibleChess[1].append("oblique")
        return possibleChess

    @staticmethod
    def isLegalMove(row, col):
        """
        判断该棋子位置是否合法

        Args:
            row: 行
            col: 列

        Returns: 合法返回True,非法返回False

        """
        if row < 0 or row >= 5 or col < 0 or col >= 5:
            return False
        return True

    @staticmethod
    def isLegalChess(chess, turn, board, dice):
        """
        判断该棋子是否为合法棋子

        Args:
            dice:
            board:
            turn:
            chess: 当前棋子

        Returns: 合法返回True,非法返回False

        """
        chess_exist = [False] * 8
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0:
                    if turn == 'team1' and board[i][j] > 0:
                        chess_exist[board[i][j]] = True
                    elif turn == 'team2' and board[i][j] < 0:
                        chess_exist[-board[i][j]] = True

        if chess_exist[dice] and chess == dice:
            return True
        elif not chess_exist[dice]:
            left = right = dice
            while left > 0 and (not chess_exist[left]):
                left -= 1
            while right <= 6 and (not chess_exist[right]):
                right += 1
            if left == 0 and right != 7:
                if chess == right:
                    return True
            elif left != 0 and right == 7:
                if chess == left:
                    return True
            elif left != 0 and right != 7:
                if chess == left or chess == right:
                    return True
        return False

    @staticmethod
    def isTerminal(board):
        """
        判断是否为终局

        Returns:[终局返回True,非终局返回False,winner]

        """
        winner = None
        # 终局位置
        if board[0][0] < 0:
            winner = 'team2'
            return [True, winner]
        elif board[4][4] > 0:
            winner = 'team1'
            return [True, winner]

        # 终局棋子数
        cnt1 = cnt2 = 0
        for i in range(5):
            for j in range(5):
                cnt1 += board[i][j] > 0 and 1 or 0
                cnt2 += board[i][j] < 0 and 1 or 0
        if cnt1 == 0:
            winner = 'team2'
            return [True, winner]
        if cnt2 == 0:
            winner = 'team1'
            return [True, winner]

        return [False, winner]
