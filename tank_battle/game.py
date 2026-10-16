# -*- coding: utf-8 -*-

"""game.py —— 游戏主逻辑：初始化、主循环、事件处理、碰撞、结算。"""

import pygame

from settings import KEY_TO_DIR, DIR_KEYS, COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, HUD_COLOR
from game_map import MAP_DATA, MAP_1, draw_map
from tank import Tank, Enemy_Tank
from bullet import Bullet

# 初始化 pygame
pygame.init()
# 初始化字体
pygame.font.init()
HUD_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)
TITLE_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 64)
INFO_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 32)

# 设置窗口大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

# 设置窗口标题
pygame.display.set_caption("坦克大战")

# 结算画面的半透明黑色遮罩
OVERLAY = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
OVERLAY.fill((0, 0, 0))
OVERLAY.set_alpha(170)

# 设置游戏时钟
clock = pygame.time.Clock()

def handle_hits():
    """处理子弹命中坦克"""
    global score, lives
    # 玩家子弹击中敌方坦克
    for e in enemies[:]:
        hit = None
        for b in tank.bullets:
            if b.rect.colliderect(e.rect):
                hit = b
                break
        if hit is not None:
            enemies.remove(e)
            tank.bullets.remove(hit)
            e.bullets.clear()
            score += 100
    # 敌方子弹击中敌方坦克、玩家坦克
    for e in enemies:
        for b in e.bullets[:]:
            # 打到玩家
            if b.rect.colliderect(tank.rect):
                e.bullets.remove(b)
                lives -= 1
                continue
            # 打到其他敌人
            for other in enemies:
                if other is not e and b.rect.colliderect(other.rect):
                    e.bullets.remove(b)
                    break

def draw_hud(surface):
    """实现在右上角绘制分数和剩余生命"""
    score_surface = HUD_FONT.render(f"分数  {score}", True, HUD_COLOR)
    life_surface = HUD_FONT.render(f"剩余生命  {lives}", True, HUD_COLOR)
    surface.blit(score_surface, score_surface.get_rect(topright=(SCREEN_WIDTH -  10, 10)))
    surface.blit(life_surface, life_surface.get_rect(topright = (SCREEN_WIDTH -10, 40)))

def check_game_over():
    """检查本局是否结束；结束则把状态切成 over"""
    global game_state, result_title, result_sub
    if lives <= 0:
        game_state = "over"
        result_title = "游戏结束"
        result_sub = "生命耗尽"
        return "lose"
    if not enemies:
        game_state = "over"
        result_title = "胜利！"
        result_sub = "敌人已全部消灭"
        return "win"
    return None

def reset_game():
    """重开一局：地图、坦克、敌人、分数、生命全部回到初始状态"""
    global tank, enemies, score, lives, game_state, result_title, result_sub
    score = 0
    lives = 3
    game_state = "playing"
    result_title = ""
    result_sub = ""
    MAP_DATA[:] = [row[:] for row in MAP_1]   # 切片赋值：原地改，不需要 global
    tank = Tank(360, 280)
    enemies = [Enemy_Tank(40, 40), Enemy_Tank(720, 40), Enemy_Tank(40, 520)]
    now = pygame.time.get_ticks()
    for e in enemies:
        e.last_shoot = now
        e.last_turn = now

def draw_result(surface):
    """结算画面：遮罩 + 标题 + 说明 + 最终得分 + 重开提示"""
    surface.blit(OVERLAY, (0, 0))
    for font, text, cy in [
        (TITLE_FONT, result_title, 240),
        (INFO_FONT, result_sub, 330),
        (INFO_FONT, f"最终得分  {score}", 385),
        (INFO_FONT, "按 R 重新开始", 460),
    ]:
        surf = font.render(text, True, HUD_COLOR)
        surface.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, cy)))

# 创建一个坦克实例，初始位置在屏幕中心
tank = Tank(360, 280)
score = 0  # 得分
lives = 3  # 剩余生命

enemies = [Enemy_Tank(40, 40), Enemy_Tank(720, 40), Enemy_Tank(40, 520)]

# 游戏状态：playing = 正在玩，over = 结算画面
game_state = "playing"
result_title = ""
result_sub = ""
# 设置程序循环状态
running = True

def run():
    """主循环：一直跑，直到窗口被关掉或按了 Ctrl+W"""
    global running
    running = True
    while running:

        game_ticks = pygame.time.get_ticks()
        all_tanks = [tank] + enemies  # 所有坦克的列表

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击窗口关闭按钮结束程序
                running = False
            elif event.type == pygame.KEYDOWN:  # 检测按下按键事件
                # 结算画面按 R 重开一局
                if event.key == pygame.K_r and game_state == "over":
                    reset_game()
                    continue
                # 方向键按下：按先后顺序记录，先按的优先；not in 防止键盘重复连发
                if event.key in DIR_KEYS:
                    if event.key not in tank.pressed_order:
                        tank.pressed_order.append(event.key)
                # 空格开火：冷却结束才发射子弹，并刷新上次开火时间
                if event.key == pygame.K_SPACE and game_ticks - tank.last_shoot >= tank.shoot_cooldown:
                    if game_state == "playing":  # 修复结算期间玩家还能发射子弹的问题
                        tank.bullets.append(Bullet(tank.rect, tank.direction))
                        tank.last_shoot = game_ticks
            elif event.type == pygame.KEYUP:  # 检测抬起按键事件
                # 松开方向键时从 pressed_order 按“先按先移除”的顺序移除
                if event.key in DIR_KEYS:
                    if event.key in tank.pressed_order:
                        tank.pressed_order.remove(event.key)
        # 按下 Ctrl + W 时退出游戏
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_w]:
            running = False

        # 更新位置
        if game_state == "playing":
            first_pressed_key = tank.pressed_order[0] if tank.pressed_order else None  # 获取当前按下的第一个方向键
            tank.move(KEY_TO_DIR.get(first_pressed_key))  # 根据第一个按下的方向键更新坦克位置和方向, .get 安全取值：没按方向键时返回 None，避免 KeyError
            tank.check_collision(screen_rect, all_tanks)  # 确保坦克不会越过墙、超出边界
            tank.update_bullets()  # 更新坦克子弹位置
            for e in enemies:
                e.maybe_turn(game_ticks)
                e.move(e.direction)
                e.check_collision(screen_rect, all_tanks)
                e.shoot(game_ticks)
                e.update_bullets()
            handle_hits()
            check_game_over()

        # 填充游戏背景颜色，清除屏幕内容
        screen.fill(COLORS["background"])

        # 绘制
        draw_map(screen)
        tank.draw(screen)
        for e in enemies:
            e.draw(screen)
            e.draw_bullet(screen)
        tank.draw_bullet(screen)
        draw_hud(screen)
        if game_state == "over":
            draw_result(screen)

        # 更新屏幕显示
        pygame.display.flip()

        # 设置游戏帧率
        clock.tick(60)

    # 退出 pygame，释放资源
    pygame.quit()