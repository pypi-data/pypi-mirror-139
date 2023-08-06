"""
Fastgame v1.3.0
>>> import fastgame

Fastgame是一个帮助你快速构建游戏或简单的GUI界面的python第三方库。
内部封装pygame2复杂的API。

作者: stripe-python
版本: 1.3.0
"""

import os
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'fastgame'  # 隐藏pygame欢迎信息
except AttributeError:  # 为了pep8
    pass

from fastgame.version import version
from fastgame.api import *   # 报pep8 error

# 报pep8 error
from pygame.locals import *

games = []  # 游戏对象队列
name = 'fastgame'
__version__ = version
