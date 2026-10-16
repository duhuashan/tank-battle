import pygame
import random

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
SHOT_COOLDOWN = 400  # 攻击冷却时间
TILE_SIZE = 40  # 地图基本格大小

# 初始化 pygame
pygame.init()
# 初始化字体
pygame.font.init()
HUD_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)
TITLE_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 64)
INFO_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 32)
HUD_COLOR = (255, 255, 255)

# 设置窗口大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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

def collides_with_tank(tank, tanks):
    """检测坦克之间的碰撞"""
    for t in tanks:
        if t is not tank and tank.rect.colliderect(t.rect):
            return True
    return False

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

# 定义坦克类
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

# 程序循环
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