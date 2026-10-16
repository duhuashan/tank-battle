# -*- coding: utf-8 -*-

"""settings.py —— 全局常量。这个文件里不应该有函数和类，只有"数值/颜色/按键"。"""

import pygame

DIR_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)  # 定义按下方向键的元组，用于检测按键顺序
DIR_VECTORS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0),}  #定义不同方向的位移(dx, dy)
DIR_NAMES = tuple(DIR_VECTORS.keys())  # ("UP", "DOWN", "LEFT", "RIGHT")
KEY_TO_DIR = {pygame.K_UP: "UP", pygame.K_DOWN: "DOWN",
              pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT"}  # 按下方向键状态到按键的对应
COLORS = {
    "background": (0, 0, 0),  # 游戏背景颜色
    "track": (50, 50, 50),  #坦克履带颜色
    "track_line": (80, 80, 80),  #坦克履带线条颜色
    "body": (76, 175, 80),  #坦克车身颜色
    "body_highlight": (96, 195, 100),  #坦克车身高亮颜色
    "turret": (60, 60, 60),  #坦克炮塔颜色
    "turret_highlight": (90, 90, 90),  #坦克炮塔高亮颜色

    "brick_wall": (139, 69, 19),  # 砖墙颜色
    "steel_wall": (128, 128, 128),  # 钢墙颜色

    "bullet": (255, 255, 255),  #子弹颜色
}

SHOT_COOLDOWN = 400  # 攻击冷却时间
TILE_SIZE = 40  # 地图基本格大小

HUD_COLOR = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
