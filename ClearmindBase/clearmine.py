from lib2to3.pgen2.token import MINEQUAL
import numpy as np
from random import randint
from typing import Tuple, Dict
from colorrander import ColorRander

class ClearMine:
    MINE = 9
    CELLTYPE = np.int16
    Dir = tuple(zip(
        (-1, -1, -1,  0,  1,  1,  1,  0),
        (-1,  0,  1,  1,  1,  0, -1, -1),
    ))
    def __init__(
        self, 
        size_row : int = 1000, 
        size_col : int = 1000,
        part_size: int = 16, # 每一子块边长, 保证不要超过numpy.int16
        part_mine_num : int = 48, # 每一子块的雷数, 保证不要超过子块大小
        seed : int = 1437,
        mod : int = 998244353,
    ) -> None:
        '''初始化'''

        # 种子, 模数
        self.__seed, self.__mod = seed, mod

        # 雷区子块边长
        self.__part_size = part_size

        self.cfg(size_row, size_col, part_mine_num)
        self.restart()

    def restart(self, change_game = False) -> None:
        '''重置游戏数据, 若参数change_game为True, 更换游戏种子'''
        
        # 已经扫开的非雷格子数量
        self.__safe = 0 

        # 随机颜色生成器, 用户编号
        self.__ColorRander = ColorRander()
        self.__userIter = 0

        # [用户 - 编号 - 颜色]映射表
        self.__dict_user2number : Dict[str, int] = {}
        self.__dict_number2color : Dict[int, str] = {}

        # 用种子重置随机数
        if change_game: self.__seed = randint(297, 998244352)
        self.__fib1, self.__fib2, self.__delta = 1, 2, self.__seed

        # 生成雷区地图
        self.__distribute()

    def cfg(self, new_row : int, new_col : int, new_mine_num : int) -> None:
        '''改变雷区大小、雷数等基础配置'''
        self.__size_row = new_row
        self.__size_col = new_col
        self.__mine_num = new_mine_num

    def __judgeEdge(self, x : int, y : int) -> bool:
        '''判断一个点是否超出雷区范围'''
        return x >= 0 and x < self.__size_row and y >= 0 and y < self.__size_col

    def __iter_get_position(self, row_size : int, col_size : int) -> Tuple[int, int]:
        '''更新用于制造雷区子块的随机数, 并获得交换坐标'''
        # 迭代更新随机数
        self.__fib1, self.__fib2 = self.__fib2, (self.__fib1 + self.__fib2) % self.__mod
        while True:
            self.__delta = (self.__delta * self.__fib1) % self.__mod
            if self.__delta > row_size * col_size: break

        # 获取要交换的坐标
        delta = self.__delta
        x = delta % row_size
        delta //= row_size
        y = delta % col_size

        return x, y

    def __distribute(self) -> None:
        '''构造雷区, 对象的属性board和color在这里面定义/重置'''
        print('pre')
        sst = time.time()
        # 雷区地图
        self.__board = np.zeros([self.__size_row, self.__size_col], dtype = ClearMine.CELLTYPE)
        
        # 雷区格子颜色(为0时表示状态格子掩盖)
        self.__color = np.zeros([self.__size_row, self.__size_col], dtype = ClearMine.CELLTYPE)

        def sub_block(row_size : int, col_size : int, mine_num : int) -> np.ndarray:
            '''构造雷区子块'''

            array = np.array([i for i in range(row_size * col_size)], dtype = ClearMine.CELLTYPE).reshape(row_size, col_size)
            for i in range(row_size):
                for j in range(col_size):
                    x, y = self.__iter_get_position(row_size, col_size)
                    array[i][j], array[x][y] = array[x][y], array[i][j]

            ret = np.zeros([row, col], dtype = ClearMine.CELLTYPE)
            ret[array < mine_num] = ClearMine.MINE

            return ret

        # 生成雷
        for i in range(0, self.__size_row, self.__part_size):
            for j in range(0, self.__size_col, self.__part_size):

                # 动态判断得到雷区子块形状以及雷的个数
                row, col, num, tag = self.__part_size, self.__part_size, self.__mine_num, False 
                if i + row > self.__size_row:
                    row = self.__size_row - i
                    tag = True
                if j + col > self.__size_col:
                    col = self.__size_col - j
                    tag = True
                if tag:
                    num = row * col * num // (self.__part_size * self.__part_size)

                # 构造雷区子块
                self.__board[i : i + row, j : j + col] = sub_block(row, col, num)
        print(f'{time.time() - sst}')
        print('ok')
        sst = time.time()
        # 为雷区格子算数
        for i in range(self.__size_row):
            for j in range(self.__size_col):
                if self.__board[i][j] == ClearMine.MINE:
                    for dir in ClearMine.Dir:
                        xx, yy = i + dir[0], j + dir[1]
                        if self.__judgeEdge(xx, yy) and self.__board[xx][yy] != ClearMine.MINE:
                            self.__board[xx][yy] += 1
                    
        print(f'{time.time() - sst}')


    def updateMask(self, x : int, y : int, color : int, F : bool = True) -> None:
        '''扫雷的DFS部分'''

        if self.__color[x][y] == 0:
            self.__color[x][y] = color
            self.__safe += 1

        if self.__board[x][y] == 0:
            for dir in ClearMine.Dir:
                xx, yy = x + dir[0], y + dir[1]
                if self.__judgeEdge(xx, yy) == False: continue
                if self.__color[xx][yy] == 0: 
                    self.updateMask(xx, yy, color, False)
        elif F == True:
            for dir in ClearMine.Dir:
                xx, yy = x + dir[0], y + dir[1]
                if self.__judgeEdge(xx, yy) == False: continue
                if self.__color[xx][yy] == 0 and self.__board[xx][yy] == 0: 
                    self.updateMask(xx, yy, color, False)

    def give_color(self, username : str) -> None:
        '''给新用户随机分配一个颜色'''
        if username not in self.__dict_user2number:
            self.__userIter += 1
            iter = self.__userIter

            self.__dict_user2number[username] = iter

            self.__dict_number2color[iter] = self.__ColorRander.rand_color()

if __name__ == '__main__':
    import time
    def draw():
        a = ClearMine()
        cnt = 0
        for i in range(a._ClearMine__size_row):
            for j in range(a._ClearMine__size_col):
                print(a._ClearMine__board[i][j], end = ' ')
                if a._ClearMine__board[i][j] == 0: cnt += 1
            print()
        print('sum = %d  cnt0 = ' % (a._ClearMine__size_row * a._ClearMine__size_col) + str(cnt))
    def test():
        st = time.time()
        a = ClearMine()
        print(f'用时:{time.time() - st}s')
    #draw()
    test()
    
