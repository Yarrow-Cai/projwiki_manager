# AI填空功能使用指南

本文档详细说明如何使用ProjWiki Manager的AI智能填空功能，自动生成高质量的技术文档。

---

## 📋 目录

1. [功能概述](#功能概述)
2. [快速开始](#快速开始)
3. [完整工作流程](#完整工作流程)
4. [AI任务类型说明](#ai任务类型说明)
5. [提示文件格式](#提示文件格式)
6. [实际使用示例](#实际使用示例)
7. [常见问题](#常见问题)

---

## 功能概述

AI填空功能是ProjWiki Manager的增强特性，它能够：

- ✅ **自动识别待补充区域**：使用增强版模板，自动标记需要AI补充的内容
- ✅ **生成详细任务清单**：为每个待补充区域生成结构化的任务描述
- ✅ **提取源码上下文**：自动分析源文件，提取函数、结构体、枚举等信息
- ✅ **生成AI提示文件**：创建格式化的提示文档，供AI助手参考
- ✅ **支持优先级管理**：按高、中、低优先级组织任务
- ✅ **保持人工审核**：AI生成的内容需要人工验证，确保质量

---

## 快速开始

### 1. 使用AI填空模式初始化

```bash
cd /path/to/your/project
python .claude/skills/projwiki_manager/scripts/scaffold_docs.py --ai-fill
```

**输出示例**：
```
[INFO] Using template: module_doc_ai.md
[INFO] AI填空模式已启用
[INFO] Scanning sources in /path/to/project...
[INFO] Found 23 potential modules.
[NEW] Created bsp_timer.md
      └─ 生成了 17 个AI填空任务
[NEW] Created app_mppt.md
      └─ 生成了 17 个AI填空任务
----------------------------------------
[SUMMARY] Created: 23, Skipped (Existing): 0

[AI TASKS] 生成了 391 个待补充任务
[AI TASKS] 任务文件: .zed/.projwiki/.ai_tasks/pending_tasks_20250110_153045.json

AI填空任务摘要
============================================================
总任务数: 391

按优先级分类:
  - 高优先级 (high):   234
  - 中优先级 (medium): 117
  - 低优先级 (low):    40

按类型分类:
  - function_list: 23
  - function_table: 69
  - code_block: 69
  - description: 92
  ...

[NEXT] 运行 'python scripts/ai_complete.py .zed/.projwiki/.ai_tasks/pending_tasks_20250110_153045.json' 来处理AI填空任务
```

### 2. 生成AI提示文件

```bash
python .claude/skills/projwiki_manager/scripts/ai_complete.py \
    --generate-prompts \
    .zed/.projwiki/.ai_tasks/pending_tasks_20250110_153045.json
```

**输出**：
```
[INFO] 加载任务文件: .zed/.projwiki/.ai_tasks/pending_tasks_20250110_153045.json
[INFO] 找到 391 个任务
[INFO] 生成提示文件: .zed/.projwiki/.ai_tasks/ai_prompts_20250110_153245.md
[SUCCESS] 提示文件已生成！

请将以下文件提供给AI助手:
  /path/to/project/.zed/.projwiki/.ai_tasks/ai_prompts_20250110_153245.md
```

### 3. 将提示文件交给AI助手处理

将生成的 `ai_prompts_*.md` 文件内容提供给AI助手（如Claude、GPT等），AI会根据源码分析逐个完成任务。

---

## 完整工作流程

### 流程图

```
┌─────────────────────────────────────────────────────────┐
│  1. 运行 scaffold_docs.py --ai-fill                     │
│     扫描源码，使用AI填空模板生成文档草稿                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  2. 自动生成任务文件                                     │
│     - pending_tasks_*.json (任务数据)                    │
│     - 显示任务摘要统计                                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  3. 生成AI提示文件                                       │
│     运行 ai_complete.py --generate-prompts              │
│     创建 ai_prompts_*.md                                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  4. AI助手处理任务                                       │
│     - 阅读提示文件中的任务要求                           │
│     - 分析提供的源码上下文                               │
│     - 生成补充内容                                       │
│     - 直接编辑对应的.md文档文件                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  5. 人工审核与验证                                       │
│     - 检查AI生成的内容是否准确                           │
│     - 修正错误或不完整的部分                             │
│     - 确保符合项目规范                                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  6. 构建HTML查看器                                       │
│     运行 build_wiki.py                                  │
│     在浏览器中验证文档质量                               │
└─────────────────────────────────────────────────────────┘
```

---

## AI任务类型说明

### 1. description - 文字描述

**用途**：生成模块概述、功能说明、数据流描述等文字内容

**示例任务**：
```markdown
<!-- AI_FILL_START:overview_description
Type: description
Priority: high
Requirement: 根据源码分析，用1-3句话简要描述该模块的功能、用途和在系统中的角色。需要体现模块的核心职责和关键特性。
Context: source_analysis
-->
简要描述该模块的功能、用途和在系统中的角色（1-3句话）。
<!-- AI_FILL_END:overview_description -->
```

### 2. function_list - 功能列表

**用途**：列举模块的主要功能点

**示例任务**：
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

### 3. function_table - 函数表格

**用途**：生成函数接口的详细表格

**示例任务**：
```markdown
<!-- AI_FILL_START:init_functions
Type: function_table
Priority: high
Requirement: 从头文件中提取所有初始化相关的函数（通常包含Init、Config、Setup等关键词），生成表格。需包含：函数名、参数类型和说明、返回值类型和说明、简要功能描述。
Context: source_analysis
Format: | 函数名 | 参数 | 返回值 | 说明 |
-->
| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `MODULE_Init()` | void | void | 模块初始化 |
<!-- AI_FILL_END:init_functions -->
```

### 4. code_block - 代码块

**用途**：提取并格式化结构体、枚举等代码定义

**示例任务**：
```markdown
<!-- AI_FILL_START:config_struct
Type: code_block
Priority: high
Requirement: 从头文件中提取配置相关的结构体定义（通常包含Config、Cfg、Param等关键词）。保留完整的类型定义，并确保每个成员都有详细的中文注释，包括：含义、单位、有效范围。
Context: source_analysis
Format: C语言代码块
-->
```c
typedef struct {
    uint16_t param1;    // 参数1说明, 单位, 范围
    uint16_t param2;    // 参数2说明, 单位, 范围
    bool     enable;    // 使能标志
} ModuleConfig_t;
```
<!-- AI_FILL_END:config_struct -->
```

### 5. code_example - 使用示例

**用途**：生成完整的代码使用示例

**示例任务**：
```markdown
<!-- AI_FILL_START:basic_example
Type: code_example
Priority: medium
Requirement: 基于提取的API接口，生成一个完整的使用示例代码，展示模块的基本使用流程：初始化->配置->启动->状态读取。代码需要符合实际API定义，添加详细的步骤注释。
Context: source_analysis
Format: C语言代码块，带注释
-->
```c
// 1. 初始化模块
MODULE_Init();
```
<!-- AI_FILL_END:basic_example -->
```

### 6. table - 通用表格

**用途**：生成中断、故障处理、校准参数等表格

**示例任务**：
```markdown
<!-- AI_FILL_START:isr_functions
Type: table
Priority: high
Requirement: 从源码中识别所有中断服务函数（通常以IRQHandler、ISR结尾或在中断向量表中注册）。提取：ISR名称、触发源（定时器/外设/事件）、执行时间要求（从注释或代码分析）、中断优先级、功能说明。如无ISR则填写"本模块无中断服务函数"。
Context: source_analysis
Format: | ISR名称 | 触发源 | 执行时间限制 | 优先级 | 说明 |
-->
| ISR名称 | 触发源 | 执行时间限制 | 优先级 | 说明 |
|---------|--------|-------------|--------|------|
| `ISR_Name()` | 触发源 | <Xus | N | 说明 |
<!-- AI_FILL_END:isr_functions -->
```

### 7. dependency_analysis - 依赖关系分析

**用途**：分析并绘制模块依赖树

**示例任务**：
```markdown
<!-- AI_FILL_START:dependencies
Type: dependency_analysis
Priority: high
Requirement: 分析源码中的#include语句和函数调用关系，绘制依赖树。识别：1)上层调用者(哪些模块调用本模块) 2)同层依赖(本模块调用的同层模块) 3)下层依赖(本模块调用的底层模块/驱动)。如无法确定可标注"待分析"。
Context: source_analysis
-->
```
本模块
├── 上层调用者
│   └── [调用本模块的模块名]
├── 同层依赖
│   └── [同层引用的模块名]
└── 下层依赖
    ├── [依赖的下层模块1]
    └── [依赖的下层模块2]
```
<!-- AI_FILL_END:dependencies -->
```

---

## 提示文件格式

生成的 `ai_prompts_*.md` 文件包含所有任务的详细信息：

```markdown
# ProjWiki AI填空任务提示文件

生成时间: 2025-01-10 15:32:45
总任务数: 391

## 任务 1/391

================================================================================
AI填空任务 #bsp_timer_overview_description_000
================================================================================

【任务信息】
- 文档文件: .zed/.projwiki/modules/bsp_timer.md
- 模块名称: bsp_timer
- 任务标识: overview_description
- 任务类型: description
- 优先级: high
- 位置: 第 15 行 - 第 20 行

【补充要求】
根据源码分析，用1-3句话简要描述该模块的功能、用途和在系统中的角色。需要体现模块的核心职责和关键特性。

【格式提示】
无特殊格式要求

【当前占位内容】
----------------------------------------
简要描述该模块的功能、用途和在系统中的角色（1-3句话）。
----------------------------------------

【源码分析上下文】
源文件: BSP/bsp_timer.c, BSP/bsp_timer.h

## 函数列表
- void TIMER_Init(void)
- void TIMER_Config(uint32_t period, uint32_t prescaler)
- void TIMER_Start(void)
- void TIMER_Stop(void)
- uint32_t TIMER_GetCount(void)
- void TIMER_SetCallback(void (*callback)(void))

## 结构体定义
### TimerConfig_t
```c
uint32_t period;      // 定时周期, us
uint32_t prescaler;   // 预分频值
bool auto_reload;     // 自动重载使能
```

## 包含的头文件
- gd32g55x.h
- stdint.h
- stdbool.h

## 关键注释
```
/**
 * @file    bsp_timer.h
 * @brief   定时器底层驱动 - 提供高精度定时和PWM功能
 * @author  Yarrow
 * @date    2024-12-15
 * @attention 用于MPPT采样定时和GaN驱动PWM
 */
```

================================================================================
【请根据以上信息生成补充内容】
================================================================================
```

---

## 实际使用示例

### 场景1：为新项目生成完整文档

```bash
# 1. 切换到项目目录
cd /path/to/gd32_micro_inverter

# 2. 使用AI填空模式扫描全部源码
python .claude/skills/projwiki_manager/scripts/scaffold_docs.py --ai-fill

# 3. 查看生成的任务统计
# 输出会显示：总任务数、按优先级分类、按类型分类

# 4. 生成AI提示文件
python .claude/skills/projwiki_manager/scripts/ai_complete.py \
    --generate-prompts \
    .zed/.projwiki/.ai_tasks/pending_tasks_*.json

# 5. 将提示文件交给AI助手
# 打开 .zed/.projwiki/.ai_tasks/ai_prompts_*.md
# 复制内容并提供给AI助手

# 6. AI完成后，构建HTML
python .claude/skills/projwiki_manager/scripts/build_wiki.py

# 7. 在浏览器中查看
open .zed/.projwiki/_site/index.html
```

### 场景2：交互式处理任务

```bash
# 运行交互模式
python .claude/skills/projwiki_manager/scripts/ai_complete.py \
    .zed/.projwiki/.ai_tasks/pending_tasks_20250110_153045.json

# 交互界面会显示：
# - 任务总数和优先级分布
# - 所有任务的列表（带优先级标记）
# - 操作菜单：
#   1. 生成详细的任务提示文件
#   2. 查看单个任务详情
#   3. 标记任务为已完成
#   4. 退出

# 选择操作1，生成提示文件
# 或选择操作2，查看特定任务的详细信息
```

### 场景3：只处理高优先级任务

```bash
# 1. 使用交互模式查看任务列表
python .claude/skills/projwiki_manager/scripts/ai_complete.py \
    .zed/.projwiki/.ai_tasks/pending_tasks_*.json

# 2. 记录高优先级任务的编号（标记为🔴）

# 3. 生成提示文件
python .claude/skills/projwiki_manager/scripts/ai_complete.py \
    --generate-prompts \
    .zed/.projwiki/.ai_tasks/pending_tasks_*.json

# 4. 在生成的提示文件中，高优先级任务排在前面
# AI助手可以优先处理这些任务
```

---

## 常见问题

### Q1: AI填空模板和标准模板有什么区别？

**A**: 
- **标准模板** (`module_doc.md`)：包含占位文本，需要手动填写所有内容
- **AI填空模板** (`module_doc_ai.md`)：在标准模板基础上添加了详细的AI填空标记，每个待补充区域都有：
  - 明确的任务类型
  - 详细的补充要求说明
  - 格式提示
  - 优先级标记

### Q2: 如果不想使用AI填空功能怎么办？

**A**: 完全可以！只需运行不带 `--ai-fill` 参数的命令：
```bash
python .claude/skills/projwiki_manager/scripts/scaffold_docs.py
```
这样会使用标准模板，不会生成AI任务。

### Q3: AI生成的内容需要审核吗？

**A**: **必须审核！** AI填空功能是辅助工具，生成的内容可能存在：
- 理解偏差（AI对代码意图的理解可能不准确）
- 信息缺失（源码注释不完整时AI无法推断）
- 格式问题（需要调整以符合项目规范）

**建议流程**：AI生成 → 人工审核 → 修正完善 → 最终发布

### Q4: 任务文件可以手动编辑吗？

**A**: 可以！`pending_tasks_*.json` 是标准JSON格式，可以：
- 修改任务优先级
- 调整补充要求
- 删除不需要的任务
- 添加自定义任务

编辑后重新运行 `ai_complete.py` 即可。

### Q5: 源码没有注释怎么办？

**A**: AI仍然可以：
- 提取函数签名、结构体定义等
- 分析依赖关系（#include）
- 推断基本功能（根据函数名、变量名）

但生成质量会降低。建议：
1. 先为关键模块添加基本的Doxygen注释
2. 然后使用AI填空功能
3. 效果会明显提升

### Q6: 如何自定义AI填空标记？

**A**: 编辑 `templates/module_doc_ai.md`：
1. 添加新的 `<!-- AI_FILL_START:identifier ... -->` 标记
2. 设置任务类型、优先级、要求等
3. 添加占位内容
4. 以 `<!-- AI_FILL_END:identifier -->` 结束

重新运行脚手架脚本即可使用新标记。

### Q7: 可以只为特定模块生成AI任务吗？

**A**: 当前版本会为所有模块生成任务。如需筛选：
1. 运行完整扫描
2. 手动编辑 `pending_tasks_*.json`
3. 删除不需要的任务
4. 保存并重新生成提示文件

或者：
1. 手动创建特定模块的文档（使用AI模板）
2. 单独提取该文档的任务

### Q8: 提示文件太大怎么办？

**A**: 如果项目有数百个模块，提示文件可能很大。建议：
1. 分批处理：先处理高优先级任务
2. 按模块类型分组（如先处理BSP层，再处理APP层）
3. 使用交互模式单独查看任务详情

---

## 最佳实践

### 1. 渐进式补充

```
第一轮：只处理高优先级任务（核心功能、接口、结构体）
第二轮：处理中优先级任务（示例、时序、保护机制）
第三轮：处理低优先级任务（限制说明、相关文档链接）
```

### 2. 质量验证检查清单

- [ ] 函数签名与源码一致
- [ ] 参数说明包含单位和范围
- [ ] 结构体注释完整准确
- [ ] 代码示例可以编译运行
- [ ] 时序参数已验证
- [ ] 安全关键部分已标注WARNING
- [ ] 链接指向正确的文档

### 3. 团队协作

- **方案A**：集中处理
  - 指定一人运行脚本生成任务
  - 团队成员分工处理不同模块的AI任务
  - 统一审核后合并

- **方案B**：分散处理
  - 每个开发者负责自己模块的文档
  - 独立运行AI填空功能
  - 定期同步更新

### 4. 持续改进

- 收集AI生成质量较差的任务类型
- 改进对应的补充要求说明
- 更新模板中的标记定义
- 优化源码注释质量

---

## 技术支持

如有问题或建议，请：
1. 查看 `SKILL.md` 中的详细文档
2. 查看 `EXAMPLES.md` 中的使用示例
3. 检查生成的任务文件和提示文件格式

---

**最后更新**: 2025-01-10  
**版本**: v1.0  
**作者**: Yarrow