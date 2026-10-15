# Git 提交规范（速查）

> **用途**：写 `git commit -m "..."` 时对照本文。
> **来源**：约定式提交 v1.0.0 规范、commitlint 的 `config-conventional`（基于 Angular 约定）、Tim Pope《A Note About Git Commit Messages》。2026-10-15 逐条对照原文核实。
> **一句话**：**"规范条文"只有几条硬要求，网上流传的另外几条其实是社区惯例** —— 本文把两者分开标注，免得记混。

---

## 1. 一个提交信息长什么样

```
<类型>[可选范围][!]: <描述>

[可选正文]

[可选脚注]
```

实际最常用的就是第一行：

```powershell
git commit -m "feat: 新增 Enemy_Tank，定时随机换向 + 撞墙换向 + 随机开火"
git commit -m "fix(碰撞): 子弹先判出界导致撞墙检测永不执行"
```

| 部分 | 规范怎么要求 |
|---|---|
| 类型 | **必须**有，是一个名词（`feat`、`fix`…），小写 |
| 范围 | 可选，圆括号包住的**名词**，说明影响哪块代码，如 `fix(parser):` |
| `!` | 可选，**紧贴冒号前面**，表示破坏性变更 |
| 冒号 + 空格 | **必须有**（英文半角冒号 + 一个空格） |
| 描述 | **必须**紧跟在冒号空格之后，是对改动的一句话总结 |
| 正文 | 可选；**必须**与描述之间空一行 |
| 脚注 | 可选；**必须**与正文之间空一行 |

---

## 2. 类型表（11 个）

> ⚠️ **规范本身只强制两个**：`feat`（新功能）和 `fix`（修 bug）。下面这张表的其余 9 个来自 **commitlint / Angular 约定**，是社区事实标准 —— 用 `commitlint` 校验时，**只有这 11 个能通过**，写别的会被拦。

| 类型 | 含义 | 版本影响 |
|---|---|---|
| `feat` | 新功能 | MINOR |
| `fix` | 修 bug | PATCH |
| `docs` | 只改文档（README、注释文档等） | 无 |
| `style` | 不影响逻辑的格式调整（空格、缩进、分号） | 无 |
| `refactor` | 重构：既不加功能也不修 bug | 无 |
| `perf` | 性能优化 | 无 |
| `test` | 加/改测试用例 | 无 |
| `build` | 构建系统、外部依赖 | 无 |
| `ci` | 持续集成配置（GitHub Actions 等） | 无 |
| `chore` | 杂项：非业务代码、工具配置 | 无 |
| `revert` | 还原某次提交 | 无 |

> 除了 `feat` / `fix`，**其余类型对版本号没有隐式影响** —— 除非它带上了破坏性变更标记（见第 3 节）。

**本项目在用的**：`feat` / `fix` / `docs` / `refactor` / `chore` —— 全部在白名单内。

---

## 3. 破坏性变更（BREAKING CHANGE）→ MAJOR

两种写法，**任选一种，效果相同**：

**写法 A：类型/范围后面加 `!`**

```
feat(api)!: 重新设计认证流程
```

**写法 B：脚注里写 `BREAKING CHANGE:`**

```
feat: 移除已废弃的 v1 接口

BREAKING CHANGE: `/api/v1/users` 接口已移除，请迁移至 `/api/v2/users`。
```

⚠️ **规范原文只给了两个位置**：`<类型>(范围)` 前缀里，或**脚注**里。**"写在正文里"不算数** —— 这是网上总结最常见的错。

细节：

- 脚注里的 `BREAKING CHANGE` **必须全大写**，后面紧跟冒号、空格、描述；
- 用了 `!` 之后，脚注里**可以**不写 `BREAKING CHANGE:`；
- 作为脚注令牌时，`BREAKING-CHANGE` 是 `BREAKING CHANGE` 的同义词（第 16 条）；
- 破坏性变更可以是**任意类型**提交的一部分（不限于 `feat`）。

---

## 4. 硬规则 vs 软惯例（最容易记混的地方）

### ✅ 硬规则 —— 规范强制；装了 commitlint 就会拦下

| 规则 | 来源 |
|---|---|
| 类型**必须存在** | 规范第 1 条 |
| 类型**小写**、且在 11 个白名单内 | commitlint `type-case` / `type-enum`（规范第 15 条只要求工具*不区分*大小写） |
| 描述必须非空 | 规范第 5 条；`subject-empty` |
| 描述**不以句号结尾** | commitlint `subject-full-stop` |
| 描述**不能用** Sentence case / Start Case / PascalCase / UPPERCASE 开头 | commitlint `subject-case` |
| 首行**≤ 100** 字符 | commitlint `header-max-length` |
| 正文、脚注每行 **≤ 100** 字符 | `body-max-line-length` / `footer-max-line-length` |
| 正文、脚注前**必须空一行** | 规范第 6、8 条 |

### 💡 软惯例 —— 规范没要求，但强烈推荐

| 惯例 | 出处 |
|---|---|
| 用**命令式、现在时**（`add` 而非 `added`/`adds`） | **Angular 约定 + Tim Pope**，规范全文没有这条 |
| 描述首字母小写 | commitlint 强制，**规范本身说大小写都可以** |
| 标题**约 50** 字符 | Tim Pope 的**软**建议（原文特意注明"不是硬上限"） |
| 正文按 **72** 列折行 | Tim Pope（为 80 列终端留回复缩进） |
| 一次提交只做一件事 | 社区最佳实践 |

> **实操结论**：把 100 当硬线，50 当软目标，正文 72 折行。命令式和小写照做，但要知道它们是 Angular / Tim Pope 的惯例，不是规范条款。

---

## 5. 脚注（footer）怎么写

格式：**令牌 + `:<空格>` 或 `<空格>#` + 值**。

```
Fixes #13
Reviewed-by: Z
Refs: #123
```

- 令牌里的空格**必须**换成 `-`（如 `Acked-by`），这样才能和正文段落区分开；
- 唯一例外：`BREAKING CHANGE` 可以带空格；
- 值可以跨行，直到出现下一个合法令牌为止。

关联 Issue 时：`Fixes #13`、`Closes #13` 会在合并后自动关闭 Issue。

---

## 6. revert 提交

规范**故意不定义** revert 的行为，只给了一条建议写法：

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

实际用 `git revert <sha>` 时 Git 会自动生成 `Revert "..."` 格式 —— 两种都能用。

---

## 7. 自查清单

提交前问自己五句：

1. **类型选对了吗？**（`feat` 还是 `fix` 还是 `refactor` —— 拿不准就想想"这次改动给使用者带来什么"）
2. **描述是命令式短句吗？**（`add` / `fix` / `remove`，不是 `added` / `fixes`）
3. **末尾没有句号？首字母小写？**
4. **首行在 100 字符以内？**（能压在 50 左右更好）
5. **只做了一件事吗？** 做了两件事就拆成两个提交。

> 规范 FAQ 也承认：*"回退并尽可能创建多次提交"* —— 一次提交只做一件事，是这套规范真正的价值所在。

---

## 8. 出处（本文的每一条都能追溯）

- 约定式提交 v1.0.0 规范：[简体中文](https://www.conventionalcommits.org/zh-hans/v1.0.0/) / [English](https://www.conventionalcommits.org/en/v1.0.0/)
- 类型表与硬规则：[`@commitlint/config-conventional` 源码](https://github.com/conventional-changelog/commitlint/blob/master/%40commitlint/config-conventional/src/index.ts)
- 命令式 / 小写 / 无句号：[Angular CONTRIBUTING（commit message guidelines）](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md)
- 50 / 72 字符：[Tim Pope, *A Note About Git Commit Messages* (2008)](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
- 语义化版本：[SemVer 中文](https://semver.org/lang/zh-CN/)
