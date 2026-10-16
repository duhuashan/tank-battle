# -*- coding: utf-8 -*-

"""bullet.py —— 子弹：怎么出生、怎么飞、撞墙了怎么办。"""

import pygame

from settings import DIR_VECTORS, TILE_SIZE, COLORS
from game_map import MAP_DATA, MAP_ROWS, MAP_COLS

class Bullet:
    def __init__(self, tank_rect, direction):
        self.speed = 10  # 子弹移动速度
        self.direction = direction  # 子弹的移动方向
        if self.direction == "UP":
            self.rect = pygame.Rect(tank_rect.centerx - 3, tank_rect.top - 6, 6, 6)
        elif self.direction == "DOWN":
            self.rect = pygame.Rect(tank_rect.centerx - 3, tank_rect.bottom, 6, 6)
        elif self.direction == "LEFT":
            self.rect = pygame.Rect(tank_rect.left - 6, tank_rect.centery - 3, 6, 6)
        elif self.direction == "RIGHT":
            self.rect = pygame.Rect(tank_rect.right, tank_rect.centery - 3, 6, 6)

    def move(self):
        dx, dy = DIR_VECTORS[self.direction]
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def hit_wall(self):
        """实现子弹击中墙的效果，并返回布尔值判断子弹是否应该被清除"""
        top_row = self.rect.top // TILE_SIZE  # 顶部所在行
        bottom_row = (self.rect.bottom - 1) // TILE_SIZE  # 底部所在行（-1 避免刚好压线时多算一行）
        left_col = self.rect.left // TILE_SIZE  # 左侧所在列
        right_col = (self.rect.right - 1) // TILE_SIZE  # 右侧所在列
        for row in range(top_row, bottom_row + 1):
            for col in range(left_col, right_col + 1):
                if 0 <= row < MAP_ROWS and 0 <= col < MAP_COLS:
                # 防止越界：矩形超出地图范围时直接跳过
                    tile = MAP_DATA[row][col]
                    if tile == 1:
                        MAP_DATA[row][col] = 0
                        return True
                    elif tile == 2:
                        return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, COLORS["bullet"], self.rect)

    def is_off_screen(self, screen_width, screen_height):
        return (self.rect.right < 0 or self.rect.left > screen_width
                or self.rect.bottom < 0 or self.rect.top > screen_height)