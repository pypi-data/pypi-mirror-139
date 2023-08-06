#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

__author__ = "CountChangye <121116728@qq.com>"
__version__ = "0.0.3"


class string(str):
    """ Python strings for humans """

    def len(self):
        return self.__len__()

    @property
    def length(self):
        return self.len()

    @property
    def size(self):
        return self.length

    def add(self, value):
        return self + string(value)

    # 将字符串分割成字符
    @property
    def character_set(self):
        return list(self)

    # 将字符串分割成字符并获取指定位置字符
    def decompose(self, index):
        return self.character_set[index - 1]

    # 判断某个字符在字符串中出现了多少次
    def judgment_times(self, target_character: str):
        return sum(
            single_character == target_character
            for single_character in self.character_set
        )


if __name__ == "__main__":
    s = string("Hello")
    x = s.add(", world")
    print(type(x))
    print(s.decompose(5))
    print(s.judgment_times('l'))
