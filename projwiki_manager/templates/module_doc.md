---
title: [模块名称]
category: modules
date: YYYY-MM-DD
author: Yarrow
tags: [层级, 功能标签]
status: draft
layer: Application | Middleware | Calculation | Hardware
---

# [模块名称]

## 概述

简要描述该模块的功能、用途和在系统中的角色（1-3句话）。

**所属层级**：`Application` | `Middleware` | `Calculation` | `Hardware`

**源文件**：
- `<Layer>/<MODULE_NAME>.c`
- `<Layer>/<MODULE_NAME>.h`

## 功能描述

### 主要功能

- 功能1：简要说明
- 功能2：简要说明
- 功能3：简要说明

### 设计目标

- 目标1
- 目标2

## 模块架构

### 依赖关系

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

### 数据流

描述数据在模块内的流向，输入来源和输出去向。

## 公开接口

### 初始化函数

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `MODULE_Init()` | void | void | 模块初始化 |
| `MODULE_Config()` | config参数 | 状态码 | 模块配置 |

### 核心功能函数

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `MODULE_Func1()` | 参数说明 | 返回值说明 | 功能描述 |
| `MODULE_Func2()` | 参数说明 | 返回值说明 | 功能描述 |

### 状态查询函数

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `MODULE_GetStatus()` | void | 状态结构体 | 获取模块状态 |

## 数据结构

### 配置结构体

```c
typedef struct {
    uint16_t param1;    // 参数1说明, 单位, 范围
    uint16_t param2;    // 参数2说明, 单位, 范围
    bool     enable;    // 使能标志
} ModuleConfig_t;
```

### 状态结构体

```c
typedef struct {
    uint16_t value1;    // 状态值1说明, 单位
    uint8_t  flags;     // 状态标志位
    uint32_t count;     // 统计计数
} ModuleStatus_t;
```

### 枚举定义

```c
typedef enum {
    MODULE_STATE_IDLE = 0,    // 空闲状态
    MODULE_STATE_RUNNING,     // 运行状态
    MODULE_STATE_ERROR        // 错误状态
} ModuleState_t;
```

## 使用示例

### 基本使用

```c
// 1. 初始化模块
MODULE_Init();

// 2. 配置参数
ModuleConfig_t cfg = {
    .param1 = 100,
    .param2 = 200,
    .enable = true
};
MODULE_Config(&cfg);

// 3. 启动运行
MODULE_Start();

// 4. 读取状态
ModuleStatus_t status;
MODULE_GetStatus(&status);
```

### 典型应用场景

描述模块在系统中的典型使用方式和调用时序。

## 中断与时序

> **WARNING**: 以下时序参数为安全关键参数，修改前必须进行评审！

### 中断服务函数

| ISR名称 | 触发源 | 执行时间限制 | 优先级 | 说明 |
|---------|--------|-------------|--------|------|
| `ISR_Name()` | 触发源 | <Xus | N | 说明 |

### 时序要求

- 响应时间：Xus / Xms
- 周期要求：Xus / Xms
- 死区时间：Xus（如适用）

## 安全与保护

> **WARNING**: 安全关键模块，修改需要评审！

### 保护机制

- 保护项1：阈值、动作、恢复条件
- 保护项2：阈值、动作、恢复条件

### 故障处理

| 故障类型 | 检测方式 | 处理动作 | 恢复条件 |
|---------|---------|---------|---------|
| 故障1 | 检测方式 | 处理动作 | 恢复条件 |

## 校准参数

| 参数名 | 默认值 | 范围 | 单位 | 说明 |
|--------|-------|------|------|------|
| param1 | 默认值 | min-max | 单位 | 工厂校准说明 |

## 已知限制

- 限制1：说明及影响
- 限制2：说明及影响

## 变更历史

| 日期 | 版本 | 作者 | 变更内容 |
|------|------|------|---------|
| YYYY-MM-DD | v1.0 | Yarrow | 初始版本 |

## 相关文档

- [相关模块1文档](../modules/related_module1.md)
- [相关API文档](../api/related_api.md)
- [相关设计文档](../design/related_design.md)