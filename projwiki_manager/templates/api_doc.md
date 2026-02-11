---
title: [API名称]
category: api
date: YYYY-MM-DD
author: Yarrow
tags: [层级, 模块名, 功能标签]
status: draft
module: [所属模块名]
layer: Application | Middleware | Calculation | Hardware
---

# [API名称] 接口文档

## 概述

简要描述该API接口集的功能、用途和设计意图（1-3句话）。

**所属模块**：`[MODULE_NAME]`
**所属层级**：`Application` | `Middleware` | `Calculation` | `Hardware`
**头文件**：`<Layer>/<MODULE_NAME>.h`

## 接口总览

| 函数名 | 功能简述 | 安全等级 |
|--------|---------|---------|
| `MODULE_Init()` | 模块初始化 | 普通 |
| `MODULE_Config()` | 参数配置 | 普通 |
| `MODULE_Start()` | 启动运行 | 普通 |
| `MODULE_Stop()` | 停止运行 | 安全关键 |
| `MODULE_GetStatus()` | 状态查询 | 普通 |

## 类型定义

### 配置结构体

```c
typedef struct {
    uint16_t param1;    // 参数1, 单位, 有效范围: min~max
    uint16_t param2;    // 参数2, 单位, 有效范围: min~max
    bool     enable;    // 功能使能标志
} ModuleConfig_t;
```

### 状态结构体

```c
typedef struct {
    uint16_t value;     // 当前值, 单位
    uint8_t  state;     // 运行状态, 见 ModuleState_t
    uint32_t err_count; // 累计错误计数
} ModuleStatus_t;
```

### 枚举类型

```c
typedef enum {
    MODULE_OK          = 0x00,  // 操作成功
    MODULE_ERR_PARAM   = 0x01,  // 参数错误
    MODULE_ERR_STATE   = 0x02,  // 状态错误（未初始化/未使能）
    MODULE_ERR_TIMEOUT = 0x03,  // 操作超时
    MODULE_ERR_HW      = 0x04   // 硬件故障
} ModuleError_t;
```

### 回调函数类型

```c
/**
 * @brief  事件回调函数类型
 * @param  event: 事件类型
 * @param  data: 事件附带数据（可为NULL）
 */
typedef void (*ModuleCallback_t)(uint8_t event, void *data);
```

## 接口详细说明

### MODULE_Init

```c
/**
 * @brief   模块初始化
 * @param   无
 * @retval  无
 */
void MODULE_Init(void);
```

**功能描述**：初始化模块内部状态、清零缓冲区、配置默认参数。

**调用时机**：系统上电后调用一次，必须在其他接口之前调用。

**前置条件**：
- 依赖的下层模块已完成初始化

**注意事项**：
- 该函数不可重入
- 调用后模块处于 `IDLE` 状态

---

### MODULE_Config

```c
/**
 * @brief   配置模块参数
 * @param   config: 配置结构体指针, 不可为NULL
 * @retval  ModuleError_t: MODULE_OK=成功, MODULE_ERR_PARAM=参数越界
 */
ModuleError_t MODULE_Config(const ModuleConfig_t *config);
```

**功能描述**：设置模块运行参数。

**参数说明**：

| 参数 | 类型 | 方向 | 说明 |
|------|------|------|------|
| config | `const ModuleConfig_t *` | 输入 | 配置参数指针, 不可为NULL |

**返回值**：

| 值 | 说明 |
|----|------|
| `MODULE_OK` | 配置成功 |
| `MODULE_ERR_PARAM` | 参数越界或指针为NULL |
| `MODULE_ERR_STATE` | 模块未初始化 |

**参数有效范围**：

| 成员 | 最小值 | 最大值 | 默认值 | 单位 |
|------|--------|--------|--------|------|
| param1 | 0 | 4095 | 100 | mV |
| param2 | 0 | 65535 | 1000 | us |

**注意事项**：
- 运行中修改配置将在下一个控制周期生效
- 传入NULL指针将返回 `MODULE_ERR_PARAM`

---

### MODULE_Start

```c
/**
 * @brief   启动模块运行
 * @param   无
 * @retval  ModuleError_t: MODULE_OK=成功
 */
ModuleError_t MODULE_Start(void);
```

**功能描述**：启动模块进入运行状态。

**前置条件**：
- 已调用 `MODULE_Init()`
- 已调用 `MODULE_Config()` 设置有效参数

**注意事项**：
- 重复调用不会产生副作用（幂等操作）

---

### MODULE_Stop

```c
/**
 * @brief   停止模块运行
 * @param   无
 * @retval  ModuleError_t: MODULE_OK=成功
 * @warning 安全关键接口, 停止后会关闭相关输出
 */
ModuleError_t MODULE_Stop(void);
```

> **WARNING**: 安全关键接口！停止操作会立即关闭相关硬件输出。

**功能描述**：停止模块运行，将输出置于安全状态。

**注意事项**：
- 紧急停止时可在任何状态下调用
- 停止后需重新 `Start` 才能恢复运行

---

### MODULE_GetStatus

```c
/**
 * @brief   获取模块运行状态
 * @param   status: 状态结构体输出指针, 不可为NULL
 * @retval  ModuleError_t: MODULE_OK=成功
 */
ModuleError_t MODULE_GetStatus(ModuleStatus_t *status);
```

**功能描述**：读取模块当前运行状态和统计信息。

**参数说明**：

| 参数 | 类型 | 方向 | 说明 |
|------|------|------|------|
| status | `ModuleStatus_t *` | 输出 | 状态输出指针, 不可为NULL |

**注意事项**：
- 可在任意状态下调用
- 返回的是快照数据，非实时更新

## 调用时序

### 典型初始化时序

```
系统上电
  │
  ├─ 1. MODULE_Init()          // 初始化
  ├─ 2. MODULE_Config(&cfg)    // 配置参数
  ├─ 3. MODULE_Start()         // 启动运行
  │     ...运行中...
  ├─ 4. MODULE_GetStatus()     // 查询状态
  │     ...
  └─ 5. MODULE_Stop()          // 停止运行
```

### 调用约束

| 当前状态 | 允许调用的接口 |
|---------|--------------|
| 未初始化 | `Init` |
| IDLE | `Config`, `Start`, `GetStatus` |
| RUNNING | `Config`, `Stop`, `GetStatus` |
| ERROR | `Stop`, `GetStatus`, `Init`（复位） |

## 使用示例

### 基本使用流程

```c
#include "MODULE_NAME.h"

void example_basic_usage(void)
{
    // 1. 初始化
    MODULE_Init();

    // 2. 配置参数
    ModuleConfig_t cfg = {
        .param1 = 500,      // 500mV
        .param2 = 2000,     // 2000us
        .enable = true
    };

    ModuleError_t err = MODULE_Config(&cfg);
    if (err != MODULE_OK) {
        // 处理配置错误
        return;
    }

    // 3. 启动
    MODULE_Start();

    // 4. 运行中查询状态
    ModuleStatus_t status;
    MODULE_GetStatus(&status);
}
```

### 错误处理示例

```c
void example_error_handling(void)
{
    ModuleError_t err;

    err = MODULE_Start();
    switch (err) {
        case MODULE_OK:
            // 启动成功
            break;
        case MODULE_ERR_STATE:
            // 未初始化, 先执行初始化
            MODULE_Init();
            break;
        case MODULE_ERR_HW:
            // 硬件故障, 记录错误并上报
            break;
        default:
            break;
    }
}
```

## 线程/中断安全

| 接口 | 可在ISR中调用 | 可重入 | 说明 |
|------|:----------:|:-----:|------|
| `MODULE_Init()` | 否 | 否 | 仅在main中调用 |
| `MODULE_Config()` | 否 | 否 | 需互斥保护 |
| `MODULE_Start()` | 否 | 否 | 需互斥保护 |
| `MODULE_Stop()` | 是 | 是 | 紧急停止可在ISR中调用 |
| `MODULE_GetStatus()` | 是 | 是 | 只读操作 |

## 性能指标

| 指标 | 典型值 | 最大值 | 说明 |
|------|--------|--------|------|
| Init耗时 | Xus | Xus | 含外设初始化 |
| Config耗时 | Xus | Xus | 仅参数写入 |
| GetStatus耗时 | Xus | Xus | 结构体拷贝 |

## 版本历史

| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|---------|
| v1.0 | YYYY-MM-DD | Yarrow | 初始版本 |

## 相关文档

- [模块文档](../modules/module_name.md)
- [设计文档](../design/related_design.md)
- [硬件接口](../hardware/related_hw.md)