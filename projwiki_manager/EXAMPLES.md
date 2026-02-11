# ProjWiki Manager - 使用示例

## 示例1：创建模块文档

**用户请求**：
> 帮我为 BSP_TIMER 模块创建技术文档

**执行步骤**：

1. AI读取 `Hardware/BSP_TIMER.c` 和 `Hardware/BSP_TIMER.h` 源文件
2. 提取函数签名、结构体定义、Doxygen注释
3. 使用 `templates/module_doc.md` 模板
4. 生成文档并写入 `.zed/.projwiki/modules/bsp_timer.md`
5. 更新 `index.md` 文档索引
6. 运行构建脚本生成HTML站点

**生成的文档示例**：

```markdown
---
title: BSP_TIMER - PWM定时器驱动
category: modules
date: 2025-07-11
author: Yarrow
tags: [Hardware, PWM, Timer, GaN]
status: published
layer: Hardware
---

# BSP_TIMER - PWM定时器驱动

## 概述

BSP_TIMER模块提供PWM生成和定时器管理功能，用于驱动逆变器GaN开关管。

**所属层级**：`Hardware`
**源文件**：`Hardware/BSP_TIMER.c` / `Hardware/BSP_TIMER.h`

## 公开接口

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `BSP_TIMER_Init()` | void | void | 定时器初始化 |
| `BSP_TIMER_SetPWM()` | channel, duty | void | 设置PWM占空比 |
| `BSP_TIMER_SetDeadTime()` | ns | void | 设置死区时间 |

> **WARNING**: 死区时间直接关系GaN器件安全，最小值200ns，严禁低于此值！
```

## 示例2：创建设计文档

**用户请求**：
> 创建并网逆变控制的设计文档

**执行步骤**：

1. AI了解并网逆变的功能需求和技术要点
2. 使用 `templates/design_doc.md` 模板
3. 生成文档并写入 `.zed/.projwiki/design/grid_tie_control.md`
4. 运行构建脚本

**对话交互示例**：

```
AI: 主人，我来帮你创建并网逆变控制的设计文档～
    需要确认几个信息：
    1. 控制策略是采用电压型还是电流型？
    2. 并网频率是50Hz还是60Hz？
    3. 需要包含哪些保护机制？

用户: 电流型控制，50Hz，需要孤岛检测、过压过流保护

AI: 收到！我会基于设计文档模板创建，包含以下章节：
    - 需求分析（并网标准、电气参数）
    - 系统架构（控制环路设计）
    - 详细设计（PLL锁相、电流环PID、MPPT）
    - 安全分析（孤岛检测、保护策略）
    - 测试计划
```

## 示例3：更新已有文档

**用户请求**：
> 更新 MDW_Sensor 模块文档，添加新增的温度采样通道

**执行步骤**：

1. AI读取 `.zed/.projwiki/modules/mdw_sensor.md` 现有内容
2. 读取 `Middleware/MDW_Sensor.c` 源码了解新增的温度通道
3. 在文档的"公开接口"章节添加新函数
4. 在"数据结构"章节更新通道枚举
5. 更新文档头部的修改日期
6. 重新生成HTML站点

## 示例4：从代码自动生成API文档

**用户请求**：
> 帮我从 MDW_PWM.h 自动生成API文档

**执行步骤**：

1. AI读取 `Middleware/MDW_PWM.h` 头文件
2. 提取所有非static函数声明和Doxygen注释
3. 提取结构体、枚举、宏定义
4. 使用 `templates/api_doc.md` 模板
5. 自动填充：
   - 接口总览表
   - 各函数详细说明（参数、返回值、注意事项）
   - 类型定义
   - 调用时序
   - 线程/中断安全性表格
6. 写入 `.zed/.projwiki/api/mdw_pwm_api.md`

## 示例5：生成HTML文档站点

**用户请求**：
> 生成文档站点，我要在浏览器里看

**执行步骤**：

1. 运行构建脚本：
```bash
python .claude/skills/projwiki_manager/scripts/build_wiki.py
```

2. 脚本输出：
```
[INFO] Project root : D:\CYC\PROJUSE\YTC_code
[INFO] Wiki directory: D:\CYC\PROJUSE\YTC_code\.zed\.projwiki
[INFO] Output dir    : D:\CYC\PROJUSE\YTC_code\.zed\.projwiki\_site

[INFO] Found 8 document(s)
[INFO] Categories: root(1), modules(3), api(2), design(1), hardware(1)

[OK] Generated: D:\CYC\PROJUSE\YTC_code\.zed\.projwiki\_site\index.html
[OK] File size: 156.3 KB
[OK] Open in browser to view documentation
```

3. 在浏览器中打开 `.zed/.projwiki/_site/index.html`

**HTML查看器功能**：
- 左侧栏：按分类浏览文档（模块、API、设计、硬件、变更日志）
- 顶部：全文搜索（支持标题、内容、标签搜索）
- 右侧栏：当前文档目录（TOC）
- 主题切换：亮色/暗色模式
- 键盘快捷键：`Ctrl+K` 或 `/` 聚焦搜索框

## 示例6：创建硬件接口文档

**用户请求**：
> 为ADC采样电路创建硬件接口文档

**执行步骤**：

1. AI使用 `templates/hw_interface_doc.md` 模板
2. 与用户交互收集硬件参数：
   - 引脚映射
   - ADC通道分配
   - 信号调理电路参数（分压比、滤波截止频率）
   - 采样时序参数
   - 校准参数
3. 生成文档写入 `.zed/.projwiki/hardware/adc_sampling.md`

## 示例7：创建变更日志

**用户请求**：
> 记录这个月的代码变更

**执行步骤**：

1. AI使用 `templates/changelog.md` 模板
2. 通过 git log 或用户描述收集变更信息
3. 按日期和类型（新增/修复/优化/安全）分类整理
4. 生成文档写入 `.zed/.projwiki/changelog/2025-07.md`

## 常用命令速查

| 操作 | 命令/请求 |
|------|----------|
| 创建模块文档 | "为 XXX 模块创建技术文档" |
| 创建API文档 | "从 XXX.h 生成API文档" |
| 创建设计文档 | "创建 XXX 功能的设计文档" |
| 创建硬件文档 | "为 XXX 硬件接口创建文档" |
| 更新文档 | "更新 XXX 文档，添加/修改 YYY" |
| 生成站点 | "生成文档站点" 或 "构建wiki" |
| 查看文档 | "打开文档查看器" |
| 记录变更 | "记录本月变更日志" |