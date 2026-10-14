import pygame

DIR_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)  # 定义方向键的元组，用于检测按键顺序
DIR_VECTORS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
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
MAP_DATA = [
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

MAP_ROWS = len(MAP_DATA)
MAP_COLS = len(MAP_DATA[0])
BULLET_COOLDOWN = 400  # 子弹发射冷却时间
TILE_SIZE = 40  # 地图基本格大小

# 初始化 pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

# 设置窗口标题
pygame.display.set_caption("坦克大战")

# 设置游戏时钟
clock = pygame.time.Clock()

def draw_map(surface):
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            if MAP_DATA[row][col] == 1:
                pygame.draw.rect(surface, COLORS["brick_wall"], (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 绘制砖墙
            elif MAP_DATA[row][col] == 2:
                pygame.draw.rect(surface, COLORS["steel_wall"], (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 绘制钢墙

def collides_with_map(rect):  # 检测矩形是否与地图碰撞
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

# 定义坦克类
class Tank:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.old_rect = self.rect.copy()
        self.speed = 5  # 坦克移动速度
        self.direction = "UP"  # 坦克初始方向为向上
        self.pressed_order = []  # 用于记录按键顺序的列表
        self.last_shot = 0
        self.bullets = []  # 坦克自身的子弹列表

    def move(self, key):
        self.old_rect = self.rect.copy()
        if key == pygame.K_UP:
            self.direction = "UP"
            self.rect.y -= self.speed
        elif key == pygame.K_DOWN:
            self.direction = "DOWN"
            self.rect.y += self.speed
        elif key == pygame.K_LEFT:
            self.direction = "LEFT"
            self.rect.x -= self.speed
        elif key == pygame.K_RIGHT:
            self.direction = "RIGHT"
            self.rect.x += self.speed
        else:
            pass  # 如果没有按下方向键，则不移动坦克

    def check_collision(self):
        if collides_with_map(self.rect):
            self.rect = self.old_rect.copy()

    def draw(self, surface):
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
        for bullet in self.bullets:
            bullet.draw(surface)

    def clamp_position(self, screen_rect):
        self.rect.clamp_ip(screen_rect)  # 确保坦克不会移出屏幕边界

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

    def hit_wall(self):  # 子弹是否撞墙
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

# 设置游戏循环状态
running = True

# 游戏循环
while running:

    game_ticks = pygame.time.get_ticks()

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in DIR_KEYS:
                if event.key not in tank.pressed_order:
                    tank.pressed_order.append(event.key)  # 按键按下时记录按键顺序
            if event.key == pygame.K_SPACE and game_ticks - tank.last_shot >= BULLET_COOLDOWN:
                tank.bullets.append(Bullet(tank.rect, tank.direction))
                tank.last_shot = game_ticks
        elif event.type == pygame.KEYUP:
            if event.key in DIR_KEYS:
                if event.key in tank.pressed_order:
                    tank.pressed_order.remove(event.key)  # 按键释放时从按键顺序中移除
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL] and keys[pygame.K_w]:
        running = False  # 按下 Ctrl + W 时退出游戏

    # 更新位置
    first_pressed_key = tank.pressed_order[0] if tank.pressed_order else None  # 获取当前按下的第一个方向键
    tank.move(first_pressed_key)  # 根据第一个按下的方向键更新坦克位置和方向
    tank.check_collision()
    tank.clamp_position(screen_rect)  # 确保坦克不会移出屏幕边界
    tank.update_bullets()  # 更新坦克子弹位置

    # 填充游戏背景颜色，清除屏幕内容
    screen.fill(COLORS["background"])

    # 绘制
    draw_map(screen)
    tank.draw(screen)
    tank.draw_bullet(screen)

    # 更新屏幕显示
    pygame.display.flip()

    # 设置游戏帧率
    clock.tick(60)

# 退出 pygame，释放资源
pygame.quit()