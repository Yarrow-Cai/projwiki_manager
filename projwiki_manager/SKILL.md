---
name: projwiki_manager
description: 嵌入式项目技术文档管理Skill - 创建、更新、浏览项目技术文档。强制使用中文编写，支持自动刷新HTML查看器，以及首次运行时自动全量扫描项目模块。专为嵌入式微逆变器项目设计。
---

# ProjWiki Manager - 嵌入式项目技术文档管理

## 概述

本Skill用于管理嵌入式项目（GD32G553 2400W微逆变器）的技术文档。所有文档以Markdown格式存储在 `.zed/.projwiki/` 目录下，并可通过Python脚本生成自包含的HTML站点，在浏览器中查看、导航和搜索。

**核心规则**：
1. **强制中文**：所有生成的文档内容（包括注释、描述、标题等）必须使用中文编写（代码标识符除外）。
2. **自动刷新**：每次创建或更新文档后，必须自动运行构建脚本刷新HTML查看器。
3. **全量扫描**：首次初始化时，自动扫描项目源码并为所有模块生成文档草稿。
4. **文档格式**：所有技术文档必须保存为标准的 Markdown 格式（.md）。

## 文档目录结构

```
.zed/.projwiki/
├── index.md              # 首页/项目总览
├── modules/              # 模块文档（按四层架构分类）
│   ├── app_xxx.md        # 应用层模块文档
│   ├── mdw_xxx.md        # 中间层模块文档
│   ├── calc_xxx.md       # 计算层模块文档
│   └── bsp_xxx.md        # 硬件层模块文档
├── api/                  # API接口文档
│   └── xxx_api.md        # 具体API文档
├── design/               # 设计文档
│   └── xxx_design.md     # 架构/功能设计
├── hardware/             # 硬件接口文档
│   └── xxx_hw.md         # 硬件接口说明
├── changelog/            # 变更日志
│   └── YYYY-MM.md        # 按月变更记录
└── _site/
    └── index.html        # 生成的HTML查看器（自动生成，勿手动编辑）
```

## 工作流程

### 流程零：初始化与全量扫描

当用户首次使用或明确要求“初始化”、“全量更新”时：

1. **自动扫描与生成**
   - 运行脚手架脚本：`python .claude/skills/projwiki_manager/scripts/scaffold_docs.py`
   - 该脚本会自动扫描项目源码，为所有缺失文档的模块生成初始文档草稿。

2. **自动刷新HTML站点**
   - 执行构建脚本：`python .claude/skills/projwiki_manager/scripts/build_wiki.py`
   - 提示用户：“全量扫描完成，文档已生成。请打开 HTML 查看器。”

### 流程一：创建新文档

当用户要求创建新的技术文档时，按以下步骤执行：

1. **确定文档类型和分类**
   - 询问用户文档属于哪个分类：`modules`（模块）、`api`（接口）、`design`（设计）、`hardware`（硬件）、`changelog`（变更）
   - 如果用户不确定，根据内容智能判断分类

2. **选择文档模板**
   - 根据分类从 `templates/` 目录选择对应模板：
     - 模块文档 → `templates/module_doc.md`
     - API文档 → `templates/api_doc.md`
     - 设计文档 → `templates/design_doc.md`
     - 硬件接口文档 → `templates/hw_interface_doc.md`
     - 变更日志 → `templates/changelog.md`

3. **收集文档信息**
   - 文档标题和简述
   - 关键技术内容（可从代码中提取）
   - 相关模块和依赖关系
   - 安全注意事项（如涉及功率级/保护逻辑）

4. **生成文档内容**
   - 基于模板填充内容
   - 遵循Doxygen风格的注释规范
   - 添加适当的交叉引用链接
   - 对于模块文档，自动从源码提取函数签名和结构体定义

5. **写入文件**
   - 文件命名规则：小写字母+下划线，如 `bsp_timer.md`
   - 写入到 `.zed/.projwiki/<分类>/` 对应目录
   - 更新 `index.md` 中的文档索引

6. **自动刷新HTML站点**
   - **必须执行**：运行 `python .claude/skills/projwiki_manager/scripts/build_wiki.py`
   - 提示用户：“文档已创建，HTML查看器已刷新。”

### 流程二：智能更新与分析 (Smart Update)

当用户要求更新文档，或不确定哪些文档需要更新时：

1. **执行新鲜度分析**
   - 运行分析脚本：`python .claude/skills/projwiki_manager/scripts/check_outdated.py`
   - 该脚本会对比源码 (.c/.h) 和文档 (.md) 的修改时间。

2. **呈现分析结果**
   - 脚本会输出一个表格，列出所有文档的状态（Fresh / OUTDATED / Missing Src）。
   - **必须**将此表格展示给用户。
   - 如果有过期的文档（OUTDATED），询问用户：“发现以上文档已过期，请选择需要更新的模块（或者回复'全部更新'）。”

3. **执行更新操作**
   - 根据用户的选择，对指定的模块执行更新：
     - 读取该模块的最新源码。
     - 读取现有的 `.md` 文档。
     - 根据源码变更更新文档内容（功能描述、API列表、结构体定义等）。
     - 更新文档头部的 `date` 字段。

4. **自动刷新HTML站点**
   - **必须执行**：运行 `python .claude/skills/projwiki_manager/scripts/build_wiki.py`
   - 提示用户：“所选文档已更新，HTML查看器已刷新。”

### 流程三：手动刷新HTML查看器

当用户要求生成或刷新文档站点时：

1. **执行构建脚本**
   ```bash
   python .claude/skills/projwiki_manager/scripts/build_wiki.py
   ```
   脚本会扫描 `.zed/.projwiki/` 下所有 `.md` 文件，生成自包含的HTML

2. **打开查看器**
   - 生成文件位于 `.zed/.projwiki/_site/index.html`
   - 可直接在浏览器中打开（双击或使用 `open` 工具）

### 流程四：从代码自动生成文档

当用户要求从源码生成文档时：

1. **扫描源文件**
   - 读取指定的 `.c` / `.h` 文件
   - 提取Doxygen注释、函数签名、结构体/枚举定义

2. **生成模块文档**
   - 使用模块文档模板
   - 自动填充函数列表、参数说明、返回值
   - 标注安全关键函数和中断服务函数

3. **生成API文档**
   - 整理公开接口（头文件中的非static函数）
   - 生成参数表格和使用示例

## 文档编写规范

### Markdown格式要求

- 一级标题(`#`)：仅用于文档标题，每个文档只有一个
- 二级标题(`##`)：主要章节
- 三级标题(`###`)：子章节
- 代码块：使用三反引号，标注语言类型（`c`、`bash`等）
- 表格：用于参数列表、寄存器映射等结构化数据
- 告警块：使用 `> **WARNING**:` 标注安全关键内容
- 链接：使用相对路径引用其他文档，如 `[BSP_TIMER](../modules/bsp_timer.md)`

### 文档头部元数据

每个文档必须包含YAML格式的头部元数据（用于HTML查看器解析）：

```markdown
---
title: 文档标题
category: modules | api | design | hardware | changelog
date: YYYY-MM-DD
author: Yarrow
tags: [标签1, 标签2]
status: draft | review | published
---
```

### 嵌入式项目特殊要求

- 所有涉及时序的描述必须标注具体数值（如 "死区时间2us"）
- 寄存器操作必须标注寄存器地址和位域
- 安全保护相关内容必须使用 `> **WARNING**:` 高亮
- 硬件接口文档必须包含引脚映射表
- 电气参数必须标注单位和有效范围

## 用户手册与专项指令

本 Skill 配备了详细的用户手册，包含初始化、更新、刷新等专项指令的说明。
- **手册位置**：`projwiki_manager/USER_MANUAL.md`
- **常用指令**：
  - `Init` / `初始化`：全量扫描并生成草稿
  - `Check` / `检查更新`：分析文档新鲜度
  - `Update` / `更新`：智能更新文档
  - `Build` / `刷新`：重新生成 HTML

## 模板参考

详细的文档模板请参考：
- 模块文档模板：`templates/module_doc.md`
- API接口模板：`templates/api_doc.md`
- 设计文档模板：`templates/design_doc.md`
- 硬件接口模板：`templates/hw_interface_doc.md`
- 变更日志模板：`templates/changelog.md`

## 使用示例

详细的使用示例请参考：`EXAMPLES.md`

## 注意事项

1. **不要手动编辑** `_site/index.html`，它由构建脚本自动生成
2. 文档文件名只使用小写字母、数字和下划线
3. 每次文档变更后建议重新生成HTML站点
4. 涉及安全关键内容的文档变更需要标注 `status: review`
5. 构建脚本需要 Python 3.6+ 环境