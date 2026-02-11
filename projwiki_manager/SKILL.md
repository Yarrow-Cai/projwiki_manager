---
name: projwiki_manager
description: 嵌入式项目技术文档管理Skill - 创建、更新、浏览项目技术文档。支持Markdown格式文档编写，自动生成可在浏览器查看的HTML文档站点，提供文档导航和搜索功能。专为嵌入式微逆变器项目设计。
---

# ProjWiki Manager - 嵌入式项目技术文档管理

## 概述

本Skill用于管理嵌入式项目（GD32G553 2400W微逆变器）的技术文档。所有文档以Markdown格式存储在 `.zed/.projwiki/` 目录下，并可通过Python脚本生成自包含的HTML站点，在浏览器中查看、导航和搜索。

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

6. **重新生成HTML站点**
   - 运行 `python .claude/skills/projwiki_manager/scripts/build_wiki.py`
   - 确认生成成功

### 流程二：更新现有文档

当用户要求更新已有文档时：

1. **定位目标文档**
   - 在 `.zed/.projwiki/` 目录下搜索目标文档
   - 如果文档不存在，提示用户并询问是否创建新文档

2. **读取现有内容**
   - 读取文档当前内容
   - 理解文档结构和上下文

3. **执行更新**
   - 根据用户要求修改内容
   - 保持文档格式和风格一致
   - 更新文档头部的修改日期
   - 如涉及API变更，同步更新相关API文档

4. **重新生成HTML站点**
   - 运行构建脚本更新HTML查看器

### 流程三：生成HTML查看器

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