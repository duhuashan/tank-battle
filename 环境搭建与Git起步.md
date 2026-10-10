# 环境搭建与 Git 起步（照抄即可）

> **用途**：把「坦克大战」项目的开发环境和 Git 仓库从零建起来。每一步都带**可验证的验收标志**。
> **最后更新**：2026-10-10

---

## 使用前必读：先确认终端和目录

本文的命令**全部是 PowerShell 语法**。在 CMD（命令提示符）里敲会报
`'Get-ChildItem' 不是内部或外部命令`。

### 1. 怎么分辨自己在哪个终端

| 提示符长这样 | 是什么 |
|---|---|
| `C:\Users\brilliant>` | **CMD** —— 本文命令**不能**直接抄 |
| `PS C:\Users\brilliant>` | **PowerShell** ✅ 可以照抄 |

如果不是 PowerShell：在当前窗口敲 `powershell` 回车，提示符出现 `PS` 就成了。

### 2. ★ CMD 的跨盘符陷阱（最容易踩）

在 CMD 里 `cd D:\vscodeproject` **只改 D 盘的记忆位置，不会真的切过去** ——
提示符依然显示 `C:\Users\brilliant>`，人还在 C 盘。

- CMD 里必须写：`cd /d D:\vscodeproject`（`/d` = 允许跨盘符）
- ⚠️ **此时若敲 `git init`，仓库会建到 `C:\Users\brilliant`（用户主目录）**，事后清理很麻烦。

### 3. 怎么确认「站对目录了」

单独敲 `cd` 回车，输出的路径**必须是** `D:\vscodeproject`。看不到这个路径就别往下走。

### 4. CMD 等价命令对照表

| 本文写的（PowerShell） | CMD 里要写成 |
|---|---|
| `Get-ChildItem -Force` | `dir /a` |
| `cd D:\vscodeproject` | `cd /d D:\vscodeproject` |
| `py -V:Astral\CPython3.12.15 -m venv .venv` | 一样 ✅ |
| `git` 全部命令 | 一样 ✅ |
| `.\.venv\Scripts\Activate.ps1` | `.venv\Scripts\activate.bat` |

### 5. 推荐的长期做法

在 **VS Code 里开发**：`File → Open Folder` 打开 `D:\vscodeproject`，
按 **Ctrl + `**（反引号，Esc 下面那个键）打开集成终端 —— 它默认就是 PowerShell，
命令可以完全照本文抄，也不用反复切窗口。

---

## 0. 本机环境体检结论（2026-10-10 实测）

| 项目 | 状态 | 实测结果 |
|---|---|---|
| Python 3.12+ | ✅ | 默认 **3.14.8**；另有 uv 装的 **3.12.15**（不在 PATH，py 启动器认它） |
| **pygame** | ❌ **未装，且默认解释器装不上** | 官方 pygame 2.6.1 的 Windows wheel 最高只到 **cp313**，3.14 上会回退源码编译并失败 |
| pip | ✅ | 26.2.1（3.14 与 3.12 均有） |
| VS Code | ✅ | 1.141.0，扩展齐全：`ms-python.python`、`vscode-pylance`、`debugpy`、`python-envs` |
| Git | ✅ | 2.55.0.windows.4，身份 `duhuashan / 2447219269@qq.com` |
| GitHub 认证 | ✅ | Git Credential Manager 已登录账号 **duhuashan** |
| gh CLI | ⚪ 未装 | 非必需，建仓库/发 Release 用网页即可 |

**唯一障碍**：pygame 的安装（见第 1 节）。

---

## 1. 装 pygame（二选一）

> **为什么不能直接敲 `pip install pygame`**：默认 Python **3.14.8** 上没有官方 pygame 的预编译包
> （pygame 2.6.1 的 Windows wheel 只做到 **cp313**），pip 会退回编译源码，而本机没有 VS Build Tools
> → 报 `ERROR: Failed to build 'pygame' when getting requirements to build wheel`。
> 所以要么**换包**，要么**换解释器**。

### 路线 A：给现有 Python 3.14 装社区版 `pygame-ce`（最省事，推荐先跑通）

```powershell
python -m pip install pygame-ce
python -c "import pygame; print(pygame.__version__)"
```

- **验收标志**：第二条命令打印出 `2.5.8`，且没有 `Traceback`。
- **说明**：`pygame-ce` 是 pygame 的社区维护分支（Community Edition），**代码写法完全一样** ——
  照任何 pygame 教程写 `import pygame`、`pygame.display.set_mode()` 都通用，原版 pygame 已基本停止更新。

### 路线 B：给项目建虚拟环境，用官方 pygame（工程习惯最好）

```powershell
cd D:\vscodeproject
py -V:Astral\CPython3.12.15 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pygame
.\.venv\Scripts\python.exe -c "import pygame; print(pygame.__version__)"
```

- **验收标志**：最后一条打印 `2.6.1`（官方 pygame），无报错。
- **说明**：官方 pygame 在 3.12 上有现成包。之后所有命令都要用 `.\.venv\Scripts\python.exe`，
  或先激活 `.\.venv\Scripts\Activate.ps1`（被 PowerShell 执行策略拦时，直接用前者绕开）。

### 两条路都要做的收尾

在 VS Code 里按 `Ctrl+Shift+P` → 输入 `Python: Select Interpreter` → 选中装好 pygame 的那个解释器
（路线 A 选 3.14；路线 B 选 `.\venv`）。

---

## 2. 建 Git 仓库（10 步）

### 第 0 步 · 确认身份（本机已配好，验一下）

```powershell
git config --global user.name
git config --global user.email
git config --global init.defaultBranch
git config --global core.quotepath false
```

- **验收**：前两条分别输出 `duhuashan` 和 `2447219269@qq.com`。
- 第三条若**没有输出**，第 2 步必须带 `-b main`（下面的命令已带）。
- 最后一条是必做的设置 —— 否则 `git status` 会把中文文件名显示成一串 `\346\226\207` 八进制码。

### 第 1 步 · 进项目目录

```powershell
cd D:\vscodeproject
Get-ChildItem -Force
```

- **验收**：只看到本需求说明这一个文件。

### 第 2 步 · 初始化仓库

```powershell
git init -b main
```

- **验收**：输出 `Initialized empty Git repository in D:/vscodeproject/.git/`；
  再跑 `Get-ChildItem -Force`，多出一个隐藏的 `.git` 目录。

### 第 3 步 · 写 `.gitignore`

在 VS Code 里（File → Open Folder 打开 `D:\vscodeproject`），新建文件 `.gitignore`，粘贴：

```gitignore
# Python
__pycache__/
*.py[cod]
build/
dist/

# 虚拟环境
.venv/
venv/

# VS Code（保留调试配置）
.vscode/*
!.vscode/launch.json
!.vscode/settings.json

# 系统 / 临时
Thumbs.db
desktop.ini
*.log
```

- **验收**：资源管理器里出现 `.gitignore`，文件名**不是** `gitignore.txt`（注意扩展名）。

### 第 4 步 · 第一次看状态（重要学习点）

```powershell
git status
```

- **验收**：能看到红色的 `Untracked files:`，里面有 `.gitignore`、需求说明和本指南 ——
  这就是「git 已经看见它们，但还没纳入版本管理」。
- 用 VS Code 打开过这个文件夹后，这里还会多出一个 `.vscode/settings.json`
  （VS Code 的 Python 扩展自动生成的，见「踩坑预告」第 7 条），属正常。

### 第 5 步 · 首次提交

```powershell
git add .
git status
git commit -m "chore: 初始化仓库，加入需求说明、起步指南与 .gitignore"
```

- **验收**：`git add` 后 `git status` 里文件变**绿色**（staged）；
  `git commit` 输出 `3 files changed`（若 VS Code 已生成 `.vscode/settings.json`，则是 `4 files changed`）；
  `git log --oneline` 有且只有 1 条记录。
- **说明**：这一次提交的内容是 `.gitignore` + 需求说明 + 本指南，共 3 个文件；
  用 VS Code 打开过项目后会多一个 `.vscode/settings.json`，变成 4 个 —— **两种都对**，以 `git status` 实际列出的为准。

### 第 6 步 · 在 GitHub 上建空仓库

浏览器打开 <https://github.com/new>：

- Repository name：`tank-battle`
- 可见性：**Public**（要发 Release 对外可见，Public 最省事；确认里面没有隐私内容）
- ⚠️ **三个勾全部不要勾**：不勾 Add a README file、不勾 Add .gitignore、不选 license
  —— 勾了会和本地文件打架
- 点 `Create repository`

- **验收**：跳转到一个写着 "…quick setup" 的空仓库页面。

### 第 7 步 · 把本地和远端接上

```powershell
git remote add origin https://github.com/duhuashan/tank-battle.git
git remote -v
```

- **验收**：`git remote -v` 输出两行，`origin` 的 fetch 和 push 都是这个地址。

### 第 8 步 · 推送

```powershell
git push -u origin main
```

- **验收**：网页刷新，仓库里有 `.gitignore`、需求说明和本指南（外加 VS Code 自动生成的
  `.vscode/settings.json`，共 3~4 个文件）；
  本地 `git status` 显示 `Your branch is up to date with 'origin/main'`。
- **说明**：本机 Git 凭据管理器已登录 `duhuashan`，正常情况不会让你输密码。

### 第 9 步 · 切出 `dev` 分支（需求文档第 1 周要求）

```powershell
git switch -c dev
git push -u origin dev
```

- **验收**：网页仓库页面的分支下拉里能看到 `main` 和 `dev` 两个分支。

---

## 3. 验收总清单（做完逐条打勾）

| # | 验收项 | 命令 / 看哪里 | 期望结果 |
|---|---|---|---|
| 1 | Python 可用 | `python --version` | `Python 3.14.8`（或 3.12.x） |
| 2 | pygame 能 import | `python -c "import pygame; print(pygame.__version__)"` | 打印版本号，无 Traceback ← **需求文档第 1 项就是这条** |
| 3 | VS Code 认出解释器 | `Ctrl+Shift+P` → Python: Select Interpreter | 列表里能选中装 pygame 的那个 |
| 4 | 仓库已初始化 | `git log --oneline` | ≥ 1 条提交，分支 `main` |
| 5 | 忽略规则生效 | `git status` | 干净，且 `.venv`（若走路线 B）**不在**待提交列表里 |
| 6 | 远端已关联 | `git remote -v` | 两行指向 `github.com/duhuashan/tank-battle` |
| 7 | 已推送 | `git status` | `Your branch is up to date with 'origin/main'` |
| 8 | GitHub 可见 | 网页刷新仓库 | 3~4 个文件、2 个分支、1 条提交记录 |
| 9 | IDE 断点调试 | 待第 1 周条目 2（`main.py` 主循环）落地后再验 | —— |

第 9 条现在验不了，因为还没有 `.py` 文件 —— 它属于「搭主循环骨架」那一步的验收。

---

## 4. 踩坑预告（遇到再回来看）

1. **VS Code 终端里 `python` 找不到** → 关掉终端重开一个（它要重新读 PATH）。
2. **PowerShell 拦 `Activate.ps1`**（提示执行策略）→ 不用激活，直接
   `.\.venv\Scripts\python.exe main.py` 即可绕开。
3. **push 报 `remote: Repository not found`** → 第 7 步地址写错了（用户名或仓库名），
   或第 6 步建成了 Private 而凭据是别的号。
4. **建仓库时手抖勾了 README** → push 会被拒（non-fast-forward）：
   先 `git pull --rebase origin main`，再 `git push -u origin main`。
5. **看到 `LF will be replaced by CRLF` 警告** → 正常，Windows 换行符处理，不用管。
6. **中文文件名显示成乱码** → 第 0 步那条 `core.quotepath false` 忘了敲。
7. **未跟踪列表里冒出 `.vscode/settings.json`**（内容形如
   `{"python-envs.defaultEnvManager": "ms-python.python:system"}`）→ 这是 VS Code 自带的
   Python 扩展**自动生成**的，不是你写的。`.gitignore` 里的 `!.vscode/settings.json`
   这条例外（`!` = 反悔、重新纳入跟踪）主动放行了它，所以被 `git add .` 收进来，**属正常**。
   若确实不想跟踪它：`git rm --cached .vscode/settings.json`，再把 `.gitignore` 里那条例外删掉。
