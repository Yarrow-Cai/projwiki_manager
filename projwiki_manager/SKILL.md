---
name: projwiki_manager
description: 嵌入式项目技术文档管理Skill - 创建、更新、浏览项目技术文档。强制使用中文编写，支持自动刷新HTML查看器，以及首次运行时自动全量扫描项目模块。新增AI智能填空功能，自动生成待补充任务。专为嵌入式微逆变器项目设计。
---

# ProjWiki Manager - 嵌入式项目技术文档管理

## 概述

本Skill用于管理嵌入式项目（GD32G553 2400W微逆变器）的技术文档。所有文档以Markdown格式存储在 `.zed/.projwiki/` 目录下，并可通过Python脚本生成自包含的HTML站点，在浏览器中查看、导航和搜索。

**核心规则**：
1. **强制中文**：所有生成的文档内容（包括注释、描述、标题等）必须使用中文编写（代码标识符除外）。
2. **自动刷新**：每次创建或更新文档后，必须自动运行构建脚本刷新HTML查看器。
3. **全量扫描**：首次初始化时，自动扫描项目源码并为所有模块生成文档草稿。
4. **文档格式**：所有技术文档必须保存为标准的 Markdown 格式（.md）。
5. **AI智能填空**：支持使用AI填空模板生成文档，自动标记待补充区域并生成任务清单。

## 文档目录结构

```
.zed/.projwiki/
├── index.md              # 首页/项目总览
├── modules/              # 模块文档（按功能域和架构层次分类）
│   ├── application/      # 应用层
│   │   ├── app_xxx.md
│   │   └── ...
│   ├── middleware/       # 中间层
│   │   ├── mdw_xxx.md
│   │   └── ...
│   ├── calculation/      # 计算层
│   │   ├── calc_xxx.md
│   │   └── ...
│   ├── bsp/              # 硬件抽象层
│   │   ├── bsp_xxx.md
│   │   └── ...
│   ├── communication/    # 通信模块（可选分类）
│   ├── control/          # 控制模块（可选分类）
│   ├── protection/       # 保护模块（可选分类）
│   └── diagnostic/       # 诊断模块（可选分类）
├── api/                  # API接口文档
│   └── xxx_api.md        # 具体API文档
├── design/               # 设计文档
│   └── xxx_design.md     # 架构/功能设计
├── hardware/             # 硬件接口文档
│   └── xxx_hw.md         # 硬件接口说明
├── changelog/            # 变更日志
│   └── YYYY-MM.md        # 按月变更记录
├── .ai_tasks/            # AI填空任务目录（新增）
│   ├── pending_tasks_YYYYMMDD_HHMMSS.json  # 待处理任务
│   └── ai_prompts_YYYYMMDD_HHMMSS.md       # AI补充提示文件
└── _site/
    └── index.html        # 生成的HTML查看器（自动生成，勿手动编辑）
```

## 工作流程

### 流程零：初始化与全量扫描

当用户首次使用或明确要求"初始化"、"全量更新"时：

#### 标准模式（不含AI填空）

1. **自动扫描与生成**
   - 运行脚手架脚本：`python .claude/skills/projwiki_manager/scripts/scaffold_docs.py`
   - 该脚本会自动扫描项目源码，为所有缺失文档的模块生成初始文档草稿。

2. **自动刷新HTML站点**
   - 执行构建脚本：`python .claude/skills/projwiki_manager/scripts/build_wiki.py`
   - 提示用户："全量扫描完成，文档已生成。请打开 HTML 查看器。"

#### AI填空模式（推荐）

1. **使用AI填空模板扫描**
   - 运行命令：`python .claude/skills/projwiki_manager/scripts/scaffold_docs.py --ai-fill`
   - 脚本会使用增强版模板（`module_doc_ai.md`），其中包含详细的AI填空标记

2. **执行文件分模块操作**
   - 初始化时自动将所有生成的文档按功能模块进行文件夹分类
   - 分类依据：
     * 按架构层次（应用层/中间层/计算层/硬件层）
     * 按功能域（通信/控制/保护/诊断等）
     * 按硬件接口（SPI/I2C/ADC/PWM等）
   - 在 `modules/` 目录下创建对应的子文件夹结构

3. **自动生成AI任务**
   - 扫描完成后，脚本会自动提取所有AI填空标记
   - 生成任务JSON文件：`.zed/.projwiki/.ai_tasks/pending_tasks_YYYYMMDD_HHMMSS.json`
   - **第一项任务必定为"重新分模块"任务**：
     * 任务标识：`reorganize_modules`
     * 优先级：`critical`
     * 要求：审查当前文件分类是否合理，根据项目实际架构重新组织模块文档结构
     * 输出：更新后的文件夹结构和文档移动清单
   - 显示任务摘要：按优先级和类型分类的任务列表

4. **处理AI填空任务**
   - 运行AI补充工具（交互模式）：
     ```bash
     python .claude/skills/projwiki_manager/scripts/ai_complete.py .zed/.projwiki/.ai_tasks/pending_tasks_*.json
     ```
   - 或生成提示文件供AI助手参考：
     ```bash
     python .claude/skills/projwiki_manager/scripts/ai_complete.py --generate-prompts .zed/.projwiki/.ai_tasks/pending_tasks_*.json
     ```

5. **AI补充工作流程**
   - 查看生成的提示文件（`.ai_tasks/ai_prompts_*.md`）
   - 每个任务包含：
     * 详细的补充要求和格式说明
     * 从源码自动提取的上下文（函数、结构体、枚举等）
     * 当前占位内容
   - AI助手根据提示文件逐个完成任务，直接编辑对应的文档文件

6. **验证与刷新**
   - 完成补充后，运行构建脚本：`python .claude/skills/projwiki_manager/scripts/build_wiki.py`
   - 在HTML查看器中验证文档质量

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

## AI填空标记格式

AI填空模板使用特殊的HTML注释标记来定义待补充区域：

```markdown
<!-- AI_FILL_START:identifier
Type: 任务类型（如 function_list, description, code_block 等）
Priority: 优先级（high, medium, low）
Requirement: 详细的补充要求说明
Context: 上下文类型（source_analysis, existing_comments, both）
Format: 格式提示（可选，如表格格式、代码块语言等）
-->
[占位内容或留空]
<!-- AI_FILL_END:identifier -->
```

**支持的任务类型**：
- `reorganize_modules` - **重新分模块（初始化时第一项任务）**
- `description` - 文字描述
- `function_list` - 功能列表
- `function_table` - 函数表格
- `code_block` - 代码块（结构体、枚举等）
- `code_example` - 使用示例代码
- `table` - 表格（如ISR表、故障处理表等）
- `specification_list` - 规格列表
- `dependency_analysis` - 依赖关系分析
- `design_analysis` - 设计分析
- `link_list` - 相关文档链接列表

**示例**：
```markdown
<!-- AI_FILL_START:main_functions
Type: function_list
Priority: high
Requirement: 通过分析源码中的函数和注释，列举该模块的3-5个主要功能点。每个功能点需要简洁说明其作用。优先关注public接口函数体现的功能。
Context: source_analysis
-->
- 功能1：简要说明
- 功能2：简要说明
- 功能3：简要说明
<!-- AI_FILL_END:main_functions -->
```

## 使用示例

详细的使用示例请参考：`EXAMPLES.md`

## 注意事项

1. **不要手动编辑** `_site/index.html`，它由构建脚本自动生成
2. 文档文件名只使用小写字母、数字和下划线
3. 每次文档变更后建议重新生成HTML站点
4. 涉及安全关键内容的文档变更需要标注 `status: review`
5. 构建脚本需要 Python 3.6+ 环境
6. AI填空功能完全可选，可以继续使用标准模板
7. AI任务文件（JSON和提示文件）保存在 `.ai_tasks/` 目录，不会影响文档结构
8. AI补充的内容需要人工审核，确保准确性和完整性
