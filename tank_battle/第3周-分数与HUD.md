# 第 3 周 · 条目 12：分数与 HUD

> **上游文档**：同目录的 `第3周-命中与销毁.md`（条目 11 已通过只读探针验收：本条 26/26、条目 8 回归 48/48）
> **本条状态**：⬜ 待实现
> **最后更新**：2026-10-16

---

## 1. 本条目标

**需求文档原文**：

> | 12 | 分数与 HUD | `font.render` 右上角画分数、剩余生命 | 分数随击杀实时变化 | commit |

一句话：**让玩家"看得见"自己的战绩** —— 条目 11 你已经把 `score` / `lives` 算对了，但它们现在只能靠 `print` 打到终端里。本条把它们画到屏幕右上角。

⚠️ 这是本项目**第一次在屏幕上画文字**。前面画的都是矩形（`pygame.draw.rect`），文字是另一套东西 —— `pygame.font`，而且**中文有坑**（见 3.3）。

---

## 2. 动手前：现在的代码长什么样

| 东西 | 现状 | 本条怎么用 |
|---|---|---|
| `score` / `lives` | 模块级变量（`score = 0`、`lives = 3`） | 直接读，就是 HUD 要显示的两个数 |
| `handle_hits()` | 命中判定函数，里面 `global score, lives` | **不用改** —— HUD 只负责读 |
| `print` 自测段 | 主循环里"只在变化时打印" | 本条**可以删掉**（信息上屏了） |
| `screen` | `pygame.display.set_mode((800, 600))` | 文字要 `blit` 到它上面 |
| 绘制顺序 | `draw_map` → `tank.draw` → `draw_bullet` → `pygame.display.flip()` | HUD 要画在**最后**，压在最上层 |

---

## 3. 核心概念

### 3.1 三步走：初始化 → 渲染 → 贴上去

```python
# ① 初始化（模块级，和 pygame.init() 放一起，只做一次）
pygame.font.init()

# ② 渲染（得到一张"文字图片"）
font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)     # 只在启动时创建一次！
text_surface = font.render("SCORE  100", True, (255, 255, 255))

# ③ 贴到屏幕上（blit = 把一张图复制到另一张图上）
screen.blit(text_surface, (10, 10))
```

**关键认知**：`render()` 返回的**不是文字，而是一张图片（`Surface`）**。pygame 不会"写一个字"，它先把字画成一张小图，再把小图贴到大图上。所以：

- 想改文字 → **重新 `render`**（一张新图）；
- 想改位置 → 重新 `blit`（同一张图可以贴多次）；
- `True` 那个参数是 **抗锯齿**（antialias，让边缘不那么锯齿），固定写 `True` 就好。

### 3.2 字体对象只能创建一次（本条最容易踩的性能坑）

```python
# ❌ 错的：写在主循环里
while running:
    font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)   # 每帧从磁盘读一遍字体文件
    ...
```

`pygame.font.Font(path, size)` 会**打开并解析字体文件**。放主循环里 = 每帧读 60 次盘，帧率直接掉一截。

正确做法：**字体对象提到循环外面，只创建一次。**

```python
# ✅ 模块级，启动时一次
HUD_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)

while running:
    ...
    screen.blit(HUD_FONT.render(f"SCORE  {score}", True, (255, 255, 255)), (10, 10))
```

### 3.3 中文必须指定字体文件（本条的真正大坑）

**实测结论（2026-10-16，Python 3.14.8 + pygame-ce 2.5.8）**：

| 写法 | 结果 |
|---|---|
| `pygame.font.Font(None, 24)` | **不报错**，但中文渲染成**方框**（默认字体是 `freesansbold.ttf`，没有中文字形） |
| `pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)` | ✅ 正常，`"分数 100"` 出来是 **(96, 28)** 像素 |
| `pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 24)` | ✅ 正常（微软雅黑），出来是 **(97, 32)** |
| `pygame.font.SysFont("simhei", 24)` | ✅ 也能用，但 `SysFont` 依赖系统注册的字体名，换台机器不一定有 |

⚠️ **最阴的地方在于 `Font(None)` 不报错** —— 它照样返回一张 (45, 18) 的小图，里面全是方框。你只会看到"字怎么变成乱码方块了"，而没有任何异常提示。**只要界面要显示中文，就老老实实写字体文件的绝对路径。**

三个可选字体（都在 `C:\Windows\Fonts\`，任选一个，本机都实测存在）：

| 文件 | 字体 | 风格 |
|---|---|---|
| `simhei.ttf` | 黑体 | 推荐 —— 笔画粗，游戏里最清楚 |
| `msyh.ttc` | 微软雅黑 | 现代，稍小一点 |
| `simsun.ttc` | 宋体 | 细笔画，小字号会糊 |

路径字符串里的反斜杠要转义：`"C:\\Windows\\Fonts\\simhei.ttf"`，或者干脆用正斜杠 `"C:/Windows/Fonts/simhei.ttf"`（两种都合法，后者更省事）。

> 📌 **顺带一提**：如果只想显示数字和字母，`Font(None, 24)` 完全够用（`"SCORE  100"` 就没问题）。本条要显示"分数"两个汉字，所以绕不开字体文件。

### 3.4 右上角定位：用 `get_rect()`

手写坐标（比如 `(650, 10)`）在文字变长时会跑出屏幕。更稳的写法是**告诉 pygame"我要贴哪个角"**，它自己算位置：

```python
surface = HUD_FONT.render(f"SCORE  {score}", True, (255, 255, 255))
rect = surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))    # 右上角，留 10px 边距
screen.blit(surface, rect)
```

`get_rect()` 的常用锚点：`topleft` / `topright` / `center` / `bottomleft` / `bottomright` / `midtop` / `midleft` / `midbottom` / `midright`。

### 3.5 分数和生命两行，还是一行？

**两种都可以**，本例推荐两行（右边一列，互不遮挡）：

```
                            SCORE  1200
                             LIFE  ♥♥♥
```

`lives` 画成心形符号要小心字体支持 —— 简单起见，先画数字：

```python
screen.blit(HUD_FONT.render(f"SCORE  {score}", True, (255, 255, 255)),
            HUD_FONT.render(f"SCORE  {score}", True, (255, 255, 255)).get_rect(topright=(790, 10)))
```

⚠️ 上面这行为了"只贴一行"把 `render` 写了两次 —— **别这么写**。分开写更清楚，也顺便给出了下一条优化：

```python
score_surface = HUD_FONT.render(f"SCORE  {score}", True, (255, 255, 255))
life_surface  = HUD_FONT.render(f"LIFE  {lives}", True, (255, 255, 255))
screen.blit(score_surface, score_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10)))
screen.blit(life_surface,  life_surface.get_rect(topright=(SCREEN_WIDTH - 10, 40)))
```

### 3.6 渲染结果要不要缓存？

分数和生命**不会每帧都变**。`render` 一次大约几百微秒，60 帧也就 2~3 毫秒，**实测影响很小**，本条**先不优化**，每帧重新渲染即可。

如果你以后发现帧率掉，再用这个套路（和条目 7 的 `last_score` 打印判断一模一样）：

```python
if score != cached_score or lives != cached_lives:
    cached_score, cached_lives = score, lives
    score_surface = HUD_FONT.render(...)      # 只在变化时重新渲染
```

**先把功能写对，再管性能** —— 这一条比任何技巧都重要。

---

## 4. 操作步骤

### 第 1 步 · 初始化字体（模块级）

在 `pygame.init()` 附近加 `pygame.font.init()`，再在常量区加字体对象：

```python
pygame.font.init()
HUD_FONT = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)
HUD_COLOR = (255, 255, 255)
```

### 第 2 步 · 写一个 `draw_hud(surface)` 函数

放在 `handle_hits()` 后面（同样是"读取全局变量、返回 None"的绘制函数）：

```python
def draw_hud(surface):
    """在右上角绘制分数与剩余生命"""
    score_surface = HUD_FONT.render(f"SCORE  {score}", True, HUD_COLOR)
    life_surface = HUD_FONT.render(f"LIFE  {lives}", True, HUD_COLOR)
    surface.blit(score_surface, score_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10)))
    surface.blit(life_surface, life_surface.get_rect(topright=(SCREEN_WIDTH - 10, 40)))
```

> ⚠️ `score` / `lives` 在函数里**只读不写**，所以这里**不需要 `global`**（条目 11 3.5 的规则：只读不用声明，只写要声明）。

### 第 3 步 · 主循环里调用（放在最最后）

```python
    draw_map(screen)
    tank.draw(screen)
    for e in enemies:
        e.draw(screen)
        e.draw_bullet(screen)
    tank.draw_bullet(screen)
    draw_hud(screen)          # ← 最最后，压在所有东西上面
    pygame.display.flip()
```

**为什么放最后**：HUD 是"浮在游戏上层的界面"，必须最后画。要是放在 `draw_map` 前面，坦克一开过去就把字盖住了。

### 第 4 步 · 删掉 `print` 自测段

主循环里那三行"只在变化时打印"现在可以删了（信息已经上屏）。

### 第 5 步 · 自测

打一个敌人，看右上角数字是不是 +100；让敌人打中你，看生命数减 1。

### 第 6 步 · 提交

```powershell
git add tank_battle/main.py
git commit -m "feat: 右上角 HUD 显示分数与剩余生命（pygame.font）"
git push
```

---

## 5. 验收标准（逐条打勾）

| # | 验收项 | 怎么验 | 期望结果 |
|---|---|---|---|
| 1 | 屏幕右上角出现分数 | 跑游戏 | 能看到 `SCORE  0` |
| 2 | 分数随击杀实时变化 | 打掉一个敌人 | 数字立刻 +100，不用重启 |
| 3 | 屏幕显示剩余生命 | 跑游戏 | 能看到生命数（初始 3） |
| 4 | 生命随中弹减少 | 让敌人打中 | 生命数 −1 |
| 5 | **中文显示正常** | 看界面 | 是汉字，**不是方框** |
| 6 | HUD 不被遮挡 | 把坦克开到右上角 | 字压在坦克上面 |
| 7 | 帧率没退化 | 探针里测 | 稳态 58–62 FPS，退出码 0 |
| 8 | 条目 11 没退化 | 重跑条目 11 的只读探针 | 26/26 PASS |
| 9 | 条目 8 没退化 | 重跑条目 8 的只读探针 | 48/48 PASS |
| 10 | Git 流程 | `git log --oneline` | 在 `dev` 上提交并已 push |

> **关于第 7 条的"帧率没退化"**：这一条就是用来防"把 `pygame.font.Font()` 写进主循环"的 —— 每帧读一次盘，帧率会明显往下掉。我可以用只读探针替你测。

---

## 6. 踩过就懂的坑

1. **`pygame.font.Font(None, 24)` 渲染中文 → 满屏方框，但不报错** —— 默认字体没有中文字形。**指定 `C:/Windows/Fonts/simhei.ttf`**（3.3）。
2. **忘了 `pygame.font.init()`** → `pygame.error: font not initialized`。它和 `pygame.init()` **不是一回事**，必须单独调一次。
3. **字体对象写在主循环里** → 每帧读一次字体文件，帧率往下掉。**提到模块级**（3.2）。
4. **HUD 画在 `draw_map` 之前** → 坦克开过就把字盖住。**最后画**（第 3 步）。
5. **`blit` 的位置写成 `(650, 10)` 这种硬编码** → 文字一长就出屏。**用 `get_rect(topright=...)`**（3.4）。
6. **路径写成 `"C:\Windows\Fonts\simhei.ttf"`** → `\W`、`\F`、`\s` 不是合法转义，Python 要么报错要么静默出错。**用双反斜杠 `\\` 或正斜杠 `/`**。
7. **给 `draw_hud` 里加 `global score, lives`** → 多余但无害；不过会误导读代码的人以为这里会改它们。**只读就不写 `global`**。
8. **`render` 的第二参数（抗锯齿）写成 `False`** → 文字边缘锯齿明显。固定写 `True`。
9. **把 `font.render()` 的返回值当字符串用** → 它是 `Surface`，`print` 出来是 `<Surface(...)>`。想调试的话用 `surface.get_size()`。
10. **生命显示成负数还在继续显示** → 条目 11 故意没处理游戏结束。显示 `-1` 有点难看，但**别在本条提前加结算逻辑** —— 那是条目 13 的事。实在难受可以写 `max(lives, 0)`。

---

## 7. Git 动作（速查）

```powershell
cd D:\vscodeproject
git switch dev
git pull
# 改 main.py（pygame.font.init + HUD_FONT + draw_hud() + 主循环调用 + 删 print）
git add tank_battle/main.py
git commit -m "feat: 右上角 HUD 显示分数与剩余生命（pygame.font）"
git push
```

---

## 8. 干完这条，下一条是什么

条目 13：**游戏结束与重开** —— 生命归零或敌人清空时出结算画面，按 `R` 重置全部状态重开。

到那时你会撞上一个**全新的问题**：条目 8 就已经发现的 **`MAP_DATA` 是可变的**（打掉的砖墙不会自己长回来）。重开一局时，除了 `score` / `lives` / `enemies` / `bullets`，**地图也必须恢复成初始状态** —— 这正是 Issue #3 记着的事，拖了三条终于要还了。
