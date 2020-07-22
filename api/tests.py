# -*- coding: utf-8 -*-

# @Date    : 2018-10-30
# @Author  : Peng Shiyu

"""
这个文档注释pydoc的示例
"""


# 函数名上方的文字
def func():
    """
    函数名下方的注释
    @return: None
    """
    print("hello")


# 类名上方的文字
class Demo():
    """
    类名下方的文字
    """

    # 类中方法上方的文字
    def hello(self):
        """
        类中方法下方的文字
        @return: None
        """
        print("hello")
