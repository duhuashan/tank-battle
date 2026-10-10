import pygame

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

# 设置游戏循环状态
running = True

# 游戏循环
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充游戏背景颜色，清除屏幕内容
    screen.fill((30, 30, 30))

    # 更新屏幕显示
    pygame.display.flip()

    # 设置游戏帧率
    clock.tick(60)

# 退出pygame，释放资源
pygame.quit()