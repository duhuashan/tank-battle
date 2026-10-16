# -*- coding: utf-8 -*-

"""map.py —— 地图数据与"和地图有关"的两件事：画地图、判断矩形碰没碰到墙。"""

import pygame

from settings import TILE_SIZE, COLORS

MAP_1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAP_DATA = [row[:] for row in MAP_1]
MAP_ROWS = len(MAP_DATA)
MAP_COLS = len(MAP_DATA[0])

def draw_map(surface):
    """绘制地图"""
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            if MAP_DATA[row][col] == 1:
                pygame.draw.rect(surface, COLORS["brick_wall"], (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 绘制砖墙
            elif MAP_DATA[row][col] == 2:
                pygame.draw.rect(surface, COLORS["steel_wall"], (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 绘制钢墙

def collides_with_map(rect):
    """检测矩形是否与地图碰撞"""
    top_row = rect.top // TILE_SIZE  # 顶部所在行
    bottom_row = (rect.bottom - 1) // TILE_SIZE  # 底部所在行（-1 避免刚好压线时多算一行）
    left_col = rect.left // TILE_SIZE  # 左侧所在列
    right_col = (rect.right - 1) // TILE_SIZE  # 右侧所在列
    for row in range(top_row, bottom_row + 1):
        for col in range(left_col, right_col + 1):
            if 0 <= row < MAP_ROWS  and 0 <= col < MAP_COLS:
            # 防止越界：矩形超出地图范围时直接跳过
                tile = MAP_DATA[row][col]
                if tile == 1 or tile == 2:
                    return True  # 发生碰撞
    return False