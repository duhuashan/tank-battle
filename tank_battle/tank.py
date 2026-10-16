# -*- coding: utf-8 -*-

"""tank.py —— 坦克：玩家坦克和敌方坦克。"""

import pygame
import random

from settings import DIR_NAMES, DIR_VECTORS, TILE_SIZE, COLORS, SHOT_COOLDOWN
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from game_map import collides_with_map
from bullet import Bullet

def collides_with_tank(tank, tanks):
    """检测坦克之间的碰撞"""
    for t in tanks:
        if t is not tank and tank.rect.colliderect(t.rect):
            return True
    return False

class Tank:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.old_rect = self.rect.copy()
        self.speed = 5  # 坦克移动速度
        self.direction = "UP"  # 坦克初始方向为向上
        self.pressed_order = []  # 记录按下方向键的顺序列表
        self.last_shoot = 0  # 上次攻击的时间
        self.shoot_cooldown = SHOT_COOLDOWN  # 射击冷却时间
        self.bullets = []  # 坦克的子弹列表

    def move(self, direction):
        """实现坦克的移动"""
        self.old_rect = self.rect.copy()
        if direction is None:
            return
        self.direction = direction
        dx, dy = DIR_VECTORS[direction]
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def check_collision(self, screen_rect, tanks):
        """实现坦克与墙、地图边界、其他坦克的碰撞"""
        if collides_with_map(self.rect) or collides_with_tank(self, tanks):
            self.rect = self.old_rect.copy()
        self.rect.clamp_ip(screen_rect)

    def draw(self, surface):
        """实现坦克的绘制"""
        if self.direction == "UP":
            pygame.draw.rect(surface, COLORS["track"], (self.rect.left, self.rect.top + 4, 10, 36))
            pygame.draw.rect(surface, COLORS["track"], (self.rect.right - 10, self.rect.top + 4, 10, 36))
            for i in range(5, 38, 4):
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.left, self.rect.top + i, 10, 2))
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.right - 10, self.rect.top + i, 10, 2))
            pygame.draw.rect(surface, COLORS["body"], (self.rect.centerx - 10, self.rect.top + 6, 20, 32))
            pygame.draw.rect(surface, COLORS["body_highlight"], (self.rect.centerx - 7, self.rect.top + 9, 14, 26))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.centerx - 2, self.rect.top, 4, 11))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.centerx - 5, self.rect.top + 11, 10, 22))
            pygame.draw.rect(surface, COLORS["turret_highlight"], (self.rect.centerx - 3, self.rect.top + 13, 6, 18))
        elif self.direction == "DOWN":
            pygame.draw.rect(surface, COLORS["track"], (self.rect.left, self.rect.top, 10, 36))
            pygame.draw.rect(surface, COLORS["track"], (self.rect.right - 10, self.rect.top, 10, 36))
            for i in range(1, 34, 4):
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.left, self.rect.top + i, 10, 2))
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.right - 10, self.rect.top + i, 10, 2))
            pygame.draw.rect(surface, COLORS["body"], (self.rect.centerx - 10, self.rect.top + 2, 20, 32))
            pygame.draw.rect(surface, COLORS["body_highlight"], (self.rect.centerx - 7, self.rect.top + 5, 14, 26))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.centerx - 2, self.rect.bottom - 11, 4, 11))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.centerx - 5, self.rect.bottom - 33, 10, 22))
            pygame.draw.rect(surface, COLORS["turret_highlight"], (self.rect.centerx - 3, self.rect.bottom - 31, 6, 18))
        elif self.direction == "LEFT":
            pygame.draw.rect(surface, COLORS["track"], (self.rect.left + 4, self.rect.top, 36, 10))
            pygame.draw.rect(surface, COLORS["track"], (self.rect.left + 4, self.rect.bottom - 10, 36, 10))
            for i in range(5, 38, 4):
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.left + i, self.rect.top, 2, 10))
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.left + i, self.rect.bottom - 10, 2, 10))
            pygame.draw.rect(surface, COLORS["body"], (self.rect.left + 6, self.rect.centery - 10, 32, 20))
            pygame.draw.rect(surface, COLORS["body_highlight"], (self.rect.left + 9, self.rect.centery - 7, 26, 14))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.left, self.rect.centery - 2, 11, 4))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.left + 11, self.rect.centery - 5, 22, 10))
            pygame.draw.rect(surface, COLORS["turret_highlight"], (self.rect.left + 13, self.rect.centery - 3, 18, 6))
        elif self.direction == "RIGHT":
            pygame.draw.rect(surface, COLORS["track"], (self.rect.left, self.rect.top, 36, 10))
            pygame.draw.rect(surface, COLORS["track"], (self.rect.left, self.rect.bottom - 10, 36, 10))
            for i in range(1, 34, 4):
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.left + i, self.rect.top, 2, 10))
                pygame.draw.rect(surface, COLORS["track_line"], (self.rect.left + i, self.rect.bottom - 10, 2, 10))
            pygame.draw.rect(surface, COLORS["body"], (self.rect.left + 2, self.rect.centery - 10, 32, 20))
            pygame.draw.rect(surface, COLORS["body_highlight"], (self.rect.left + 5, self.rect.centery - 7, 26, 14))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.right - 11, self.rect.centery - 2, 11, 4))
            pygame.draw.rect(surface, COLORS["turret"], (self.rect.right - 33, self.rect.centery - 5, 22, 10))
            pygame.draw.rect(surface, COLORS["turret_highlight"], (self.rect.right - 31, self.rect.centery - 3, 18, 6))

    def update_bullets(self):
        """更新还存活子弹，移除应该被销毁的子弹"""
        alive_bullets = []
        for bullet in self.bullets:
            bullet.move()
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                continue  # 出界，丢掉
            if bullet.hit_wall():
                continue  # 撞墙，丢掉（地图已改）
            alive_bullets.append(bullet)
        self.bullets[:] = alive_bullets

    def draw_bullet(self, surface):
        """实现坦克子弹的绘制"""
        for bullet in self.bullets:
            bullet.draw(surface)

class Enemy_Tank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = random.choice(DIR_NAMES)  # 初始朝向随机
        self.last_turn = 0  # 上次转向的时间点
        self.next_turn = 1000  # 下次换向的时间间隔（毫秒）
        self.next_shoot = 1000  #下次射击的间隔时间

    def turn(self):
        """立刻换一个不同方向（不受计时器限制）"""
        self.direction = random.choice([d for d in DIR_NAMES if d != self.direction])

    def maybe_turn(self, ticks):
        """定时随机换向（到点了才换）"""
        if ticks - self.last_turn >= self.next_turn:
            self.turn()
            self.last_turn = ticks
            self.next_turn = random.randint(1000, 3000)

    def check_collision(self, screen_rect, tanks):
        """在父类实现碰撞的基础上，实现撞墙换向，防止卡墙角"""
        temp_rect = self.rect.copy()
        super().check_collision(screen_rect, tanks)
        if self.rect != temp_rect:
            self.turn()

    def shoot(self, ticks):
        """实现敌方坦克的随机射击"""
        if ticks - self.last_shoot >= self.next_shoot:
            self.bullets.append(Bullet(self.rect, self.direction))
            self.last_shoot = ticks
            self.next_shoot = random.randint(800, 2500)