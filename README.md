# leetcode-generator

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

根据 LeetCode 题目详情 CSV 数据，生成 Markdown 刷题草稿和多语言代码模板，并支持将题目移动到刷题项目。

## 支持语言

| 语言 | 状态 | 文件名 |
|------|------|--------|
| Java | ✅ 支持 | `Solution.java` |
| Python | ✅ 支持 | `solution.py` |
| C++ | ✅ 支持 | `Solution.cpp` |
| Go | 待支持 | - |
| Rust | 待支持 | - |
| JavaScript | 待支持 | - |

## 功能

| 命令 | 说明 |
|------|------|
| `lc-gen` | 读取 CSV，按语言和题型分类生成 Markdown 文件和代码模板 |
| `lc-move` | 将指定题号从生成目录移动到刷题项目目录 |

## 快速开始

### 前置依赖

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### 1. 安装

```bash
git clone <repo-url> leetcode-generator
cd leetcode-generator
uv sync
```

### 2. 准备数据

将 LeetCode 题目详情 CSV 放入 `data/` 目录，文件名为 `题目详情.csv`。

CSV 需包含以下字段：

| 字段 | 说明 |
|------|------|
| `questionFrontendId` | 题号（如 "1"、"LCP 01"、"LCR 001"） |
| `titleSlug` | URL slug（如 "two-sum"） |
| `translatedTitle` | 中文标题 |
| `questionTitle` | 英文标题（备用） |
| `difficulty` | 难度 |
| `topicTags` | 标签 |
| `isPaidOnly` | 是否会员题 |
| `url` | 题目链接 |
| `translatedContent` | 中文描述（HTML） |
| `content` | 英文描述（HTML，备用） |
| `exampleTestcases` | 示例 |
| `javaCode` | Java 代码模板 |
| `pythonCode` | Python 代码模板 |
| `cppCode` | C++ 代码模板 |

> 如需其他语言的代码模板，可自定义 `scripts/split_code_snippets.py` 从 `题目详情.csv` 的 `codeSnippets` 字段拆解出新列，然后补充对应的生成逻辑。

### 3. 配置语言

编辑 `.env`：

```env
# 生成的语言，逗号分隔（可选: java, python, cpp）
LC_LANGUAGES=java,python,cpp
```

### 4. 生成 Markdown

```bash
uv run lc-gen
```

输出到 `generated/` 下，按语言和题型分类：

```text
generated/
├── java/
│   └── leetcode/
│       ├── problems/     # 标准题目 (lc0001_two_sum/)
│       ├── LCP/          # LCP (LCP01_xxx/)
│       ├── LCR/          # LCR (LCR001_xxx/)
│       ├── LCS/          # LCS (LCS01_xxx/)
│       └── interview/    # 面试题 (mst_01_01_xxx/)
├── python/
│   └── leetcode/
│   └── ...
└── cpp/
    └── leetcode/
    └── ...
```

每个题目目录包含：
- `lc0001_两数之和.md` — 题目 Markdown（含描述、示例、参考答案、刷题笔记模板）
- `Solution.java` / `solution.py` / `Solution.cpp` — 代码模板

### 5. 移动题目到刷题项目

`lc-gen` 生成的 Java/C++ 代码模板来自 LeetCode 官方，不包含完整的 `import` 和 `return` 部分。

如果一次性全部导入 IDE 项目，其他未完成的题目会导致编译报错，干扰当前正在做的题。因此推荐做哪题就移哪题，`lc-move` 就是用来按需复制的。Python 不受此影响，因为脚本可以独立运行。

#### 推荐用法：全局命令

在 Shell 配置文件中添加别名，之后可在任意终端直接使用 `lc-move`。
请将 `<project-path>` 替换为你的 leetcode-generator 项目实际路径。

**macOS (zsh)**

```bash
# 方式一：直接写入
echo 'alias lc-move="cd <project-path> && uv run lc-move"' >> ~/.zshrc
source ~/.zshrc

# 方式二：手动编辑
vim ~/.zshrc
# 在末尾添加: alias lc-move="cd <project-path> && uv run lc-move"
# 保存后执行:
source ~/.zshrc
```

**Linux (bash)**

```bash
# 方式一：直接写入
echo 'alias lc-move="cd <project-path> && uv run lc-move"' >> ~/.bashrc
source ~/.bashrc

# 方式二：手动编辑
vim ~/.bashrc
# 在末尾添加: alias lc-move="cd <project-path> && uv run lc-move"
# 保存后执行:
source ~/.bashrc
```

**Windows (PowerShell)**

```powershell
# 方式一：直接写入
Add-Content -Path $PROFILE -Value 'function lc-move { Set-Location "<project-path>"; uv run lc-move @args }'
. $PROFILE

# 方式二：手动编辑
notepad $PROFILE
# 在末尾添加: function lc-move { Set-Location "<project-path>"; uv run lc-move @args }
# 保存后执行:
. $PROFILE
```

> 将 `<project-path>` 替换为你的 leetcode-generator 项目实际路径。

配置完成后，在任意终端中使用：

```bash
# 移动 Java 题目（默认）
lc-move 1
lc-move 1 42 200

# 移动 Python 题目
lc-move --lang python 1

# 移动 C++ 题目
lc-move --lang cpp 1
```

示例输出：

```text
源目录:   .../leetcode-generator/generated/python/leetcode/problems
目标目录: .../leetcode/python
语言:     python
共 1 题

  [1] .../generated/python/leetcode/problems/lc0001_two-sum
     -> .../leetcode/python/lc0001_two-sum

完成！
```

需要在 `.env` 中配置各语言的目标项目路径：

```env
LC_TARGET_DIR_JAVA=<java-project-path>
LC_TARGET_DIR_PYTHON=<python-project-path>
LC_TARGET_DIR_CPP=<cpp-project-path>
```

## 可选配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `LC_LANGUAGES` | 生成的语言（逗号分隔） | `java` |
| `LC_MOVE_LANG` | lc-move 默认移动语言 | `LC_LANGUAGES` 第一个值 |
| `LC_OUTPUT_DIR` | CSV 数据目录 | `data` |
| `LC_GENERATED_DIR` | 生成产物目录 | `generated` |
| `LC_DETAIL_CSV` | 详情 CSV 路径 | `{LC_OUTPUT_DIR}/题目详情.csv` |
| `LC_TARGET_DIR_JAVA` | Java 刷题目标目录 | （空，需自行配置） |
| `LC_TARGET_DIR_PYTHON` | Python 刷题目标目录 | （空，需自行配置） |
| `LC_TARGET_DIR_CPP` | C++ 刷题目标目录 | （空，需自行配置） |

## License

[MIT](LICENSE)
