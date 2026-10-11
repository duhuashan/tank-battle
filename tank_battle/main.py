import pygame

DIR_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)  # 定义方向键的元组，用于检测按键顺序


# 初始化 pygame
pygame.init()

# 设置窗口大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置窗口标题
pygame.display.set_caption("坦克大战")

# 设置游戏时钟
clock = pygame.time.Clock()

# 定义坦克类
class Tank:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = (0, 255, 0)  # 坦克颜色为绿色
        self.speed = 5  # 坦克移动速度
        self.direction = "UP"  # 坦克初始方向为向上
        self.pressed_order = []  # 用于记录按键顺序的列表

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def handle_keys(self):
        first_pressed_key = self.pressed_order[0] if self.pressed_order else None  # 获取当前按下的第一个方向键
        if first_pressed_key == pygame.K_UP:
            self.direction = "UP"
            self.rect.y -= self.speed
        elif first_pressed_key == pygame.K_DOWN:
            self.direction = "DOWN"
            self.rect.y += self.speed
        elif first_pressed_key == pygame.K_LEFT:
            self.direction = "LEFT"
            self.rect.x -= self.speed
        elif first_pressed_key == pygame.K_RIGHT:
            self.direction = "RIGHT"
            self.rect.x += self.speed

    def clamp_position(self, screen_rect):
        self.rect.clamp_ip(screen_rect)  # 确保坦克不会移出屏幕边界

# 创建一个坦克实例，初始位置在屏幕中心
tank = Tank(380, 280)

# 设置游戏循环状态
running = True

# 游戏循环
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in DIR_KEYS:
                if event.key not in tank.pressed_order:
                    tank.pressed_order.append(event.key)  # 按键按下时记录按键顺序
        elif event.type == pygame.KEYUP:
            if event.key in DIR_KEYS:
                if event.key in tank.pressed_order:
                    tank.pressed_order.remove(event.key)  # 按键释放时从按键顺序中移除

    # 更新坦克位置和方向
    tank.handle_keys()
    tank.clamp_position(screen.get_rect())

    # 填充游戏背景颜色，清除屏幕内容
    screen.fill((30, 30, 30))

    # 绘制坦克
    tank.draw(screen)

    # 更新屏幕显示
    pygame.display.flip()

    # 设置游戏帧率
    clock.tick(60)

# 退出 pygame，释放资源
pygame.quit()