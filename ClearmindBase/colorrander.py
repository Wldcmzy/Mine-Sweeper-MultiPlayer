from random import randint

class ColorRander:
    BaseColor = (
        ('#3C3C3C','#4F4F4F','#5B5B5B','#6C6C6C','#7B7B7B','#8E8E8E','#9D9D9D','#ADADAD','#BEBEBE','#d0d0d0','#E0E0E0','#F0F0F0'),
        ('#600000','#750000','#930000','#AE0000','#CE0000','#EA0000','#FF0000','#FF2D2D','#FF5151','#ff7575','#FF9797','#FFB5B5'),
        ('#9F0050','#BF0060','#D9006C','#F00078','#FF0080','#FF359A','#FF60AF','#FF79BC','#FF95CA','#ffaad5','#FFC1E0','#FFD9EC'),
        ('#750075','#930093','#AE00AE','#D200D2','#E800E8','#FF00FF','#FF44FF','#FF77FF','#FF8EFF','#ffa6ff','#FFBFFF','#FFD0FF'),
        ('#4B0091','#5B00AE','#6F00D2','#8600FF','#921AFF','#9F35FF','#B15BFF','#BE77FF','#CA8EFF','#d3a4ff','#DCB5FF','#E6CAFF'),
        ('#0000C6','#0000C6','#0000E3','#2828FF','#4A4AFF','#6A6AFF','#7D7DFF','#9393FF','#AAAAFF','#B9B9FF','#CECEFF','#DDDDFF'),
        ('#004B97','#005AB5','#0066CC','#0072E3','#0080FF','#2894FF','#46A3FF','#66B3FF','#84C1FF','#97CBFF','#ACD6FF','#C4E1FF'),
        ('#007979','#009393','#00AEAE','#00CACA','#00E3E3','#00FFFF','#4DFFFF','#80FFFF','#A6FFFF','#BBFFFF','#CAFFFF','#D9FFFF'),
        ('#019858','#01B468','#02C874','#02DF82','#02F78E','#1AFD9C','#4EFEB3','#7AFEC6','#96FED1','#ADFEDC','#C1FFE4','#D7FFEE'),
        ('#009100','#00A600','#00BB00','#00DB00','#00EC00','#28FF28','#53FF53','#79FF79','#93FF93','#A6FFA6','#BBFFBB','#CEFFCE'),
        ('#64A600','#73BF00','#82D900','#8CEA00','#9AFF02','#A8FF24','#B7FF4A','#C2FF68','#CCFF80','#D3FF93','#DEFFAC','#E8FFC4'),
        ('#737300','#8C8C00','#A6A600','#C4C400','#E1E100','#F9F900','#FFFF37','#FFFF6F','#FFFF93','#FFFFAA','#FFFFB9','#FFFFCE'),
        ('#977C00','#AE8F00','#C6A300','#D9B300','#EAC100','#FFD306','#FFDC35','#FFE153','#FFE66F','#FFED97','#FFF0AC','#FFF4C1'),
        ('#BB5E00','#D26900','#EA7500','#FF8000','#FF9224','#FFA042','#FFAF60','#FFBB77','#FFC78E','#FFD1A4','#FFDCB9','#FFE4CA'),
        ('#A23400','#BB3D00','#D94600','#F75000','#FF5809','#FF8040','#FF8F59','#FF9D6F','#FFAD86','#FFBD9D','#FFCBB3','#FFDAC8'),
    )

    def __init__(self) -> None:
        self.__colors = len(ColorRander.BaseColor)
        self.__kinds = len(ColorRander.BaseColor[0])
        self.__counts = {
            'sum' : 0,
            'colors' : [0] * self.__colors,
            'kinds' : [[0] * self.__kinds for i in range(self.__colors)],
        }

    def rand_color(self) -> str:
        '''尽可能有区分度且不重复地随机得到一种颜色'''
        choosen_color, choosen_kind = 0, 0

        index = randint(0, self.__colors - 1)
        threshold = self.__counts['sum'] // self.__colors
        while True:
            if self.__counts['colors'][index] <= threshold:
                choosen_color = index
                break
            index = (index + 1) % self.__colors
        
        index = randint(0, self.__kinds - 1)
        threshold = self.__counts['colors'][choosen_color] // self.__kinds
        while True:
            if self.__counts['kinds'][choosen_color][index] <= threshold:
                choosen_kind = index
                break
            index = (index + 1) % self.__kinds

        self.__counts['sum'] += 1
        self.__counts['colors'][choosen_color] += 1
        self.__counts['kinds'][choosen_color][choosen_kind] += 1

        return ColorRander.BaseColor[choosen_color][choosen_kind]
    