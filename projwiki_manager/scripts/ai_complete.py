#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file    ai_complete.py
@brief   AI自动补充工具 - 读取任务并生成AI补充内容
@author  Yarrow
@date    2025-01-10
@attention 处理文档AI填空任务，生成详细的补充提示
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

try:
    from ai_task_utils import (
        AIFillTask,
        extract_source_code_info,
        load_tasks_from_json,
        save_tasks_to_json,
    )

    AI_TASK_SUPPORT = True
except ImportError:
    print(
        "[ERROR] ai_task_utils.py not found. Please ensure it's in the same directory."
    )
    sys.exit(1)


def find_project_root():
    """从脚本位置向上查找项目根目录"""
    cur = Path(__file__).resolve().parent
    for _ in range(10):
        if (cur / ".zed").is_dir():
            return cur
        if (cur / ".git").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent

    cur = Path.cwd()
    if (cur / ".zed").is_dir() or (cur / ".git").is_dir():
        return cur

    print("[WARN] Cannot find project root. Using current directory.")
    return Path.cwd()


def build_ai_prompt(task: AIFillTask, source_info: Dict, project_root: Path) -> str:
    """
    为单个任务构建AI补充提示

    返回格式化的提示文本，包含任务要求和源码上下文
    """
    prompt = f"""
{"=" * 80}
AI填空任务 #{task.task_id}
{"=" * 80}

【任务信息】
- 文档文件: {task.file_path}
- 模块名称: {task.module_name}
- 任务标识: {task.identifier}
- 任务类型: {task.task_type}
- 优先级: {task.priority}
- 位置: 第 {task.start_line} 行 - 第 {task.end_line} 行

【补充要求】
{task.requirement}

【格式提示】
{task.format_hint if task.format_hint else "无特殊格式要求"}

【当前占位内容】
{"-" * 40}
{task.placeholder_content}
{"-" * 40}

"""

    # 添加源码上下文
    if task.context_type in ["source_analysis", "both"]:
        prompt += "【源码分析上下文】\n"
        prompt += f"源文件: {', '.join(task.source_files)}\n\n"

        # 添加函数信息
        if source_info.get("functions"):
            prompt += "## 函数列表\n"
            for func in source_info["functions"][:20]:  # 限制数量
                prompt += f"- {func['return_type']} {func['name']}({func['params']})\n"
            prompt += "\n"

        # 添加结构体信息
        if source_info.get("structs"):
            prompt += "## 结构体定义\n"
            for struct in source_info["structs"]:
                prompt += f"### {struct['name']}\n"
                prompt += f"```c\n{struct['body']}\n```\n\n"

        # 添加枚举信息
        if source_info.get("enums"):
            prompt += "## 枚举定义\n"
            for enum in source_info["enums"]:
                prompt += f"### {enum['name']}\n"
                prompt += f"```c\n{enum['body']}\n```\n\n"

        # 添加包含的头文件
        if source_info.get("includes"):
            prompt += "## 包含的头文件\n"
            for inc in source_info["includes"][:15]:
                prompt += f"- {inc}\n"
            prompt += "\n"

        # 添加重要注释
        if source_info.get("comments"):
            prompt += "## 关键注释\n"
            for comment in source_info["comments"][:5]:
                prompt += f"```\n{comment}\n```\n\n"

    prompt += f"\n{'=' * 80}\n"
    prompt += "【请根据以上信息生成补充内容】\n"
    prompt += f"{'=' * 80}\n\n"

    return prompt


def generate_prompt_file(
    tasks: List[AIFillTask], output_path: Path, project_root: Path
) -> None:
    """生成包含所有任务提示的文件"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# ProjWiki AI填空任务提示文件\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总任务数: {len(tasks)}\n\n")

        # 按优先级排序
        high_priority = [t for t in tasks if t.priority == "high"]
        medium_priority = [t for t in tasks if t.priority == "medium"]
        low_priority = [t for t in tasks if t.priority == "low"]

        sorted_tasks = high_priority + medium_priority + low_priority

        for idx, task in enumerate(sorted_tasks, 1):
            f.write(f"\n\n## 任务 {idx}/{len(tasks)}\n\n")

            # 收集源码信息
            source_info = {
                "functions": [],
                "structs": [],
                "enums": [],
                "includes": [],
                "comments": [],
            }

            for src_file_rel in task.source_files:
                # 清理源文件路径
                src_file_rel = src_file_rel.strip().lstrip("- `").rstrip("`")
                src_file_path = project_root / src_file_rel

                if src_file_path.exists():
                    file_info = extract_source_code_info(src_file_path)
                    # 合并信息
                    for key in source_info.keys():
                        source_info[key].extend(file_info[key])

            # 生成提示
            prompt = build_ai_prompt(task, source_info, project_root)
            f.write(prompt)


def interactive_complete(
    tasks: List[AIFillTask], project_root: Path, task_file_path: Path
) -> None:
    """交互式AI补充模式"""

    print("\n" + "=" * 80)
    print("AI补充交互模式")
    print("=" * 80)
    print(f"\n共有 {len(tasks)} 个待处理任务\n")

    # 按优先级分组显示
    by_priority = {"high": [], "medium": [], "low": []}
    for task in tasks:
        by_priority[task.priority].append(task)

    print("任务概览:")
    print(f"  高优先级: {len(by_priority['high'])} 个")
    print(f"  中优先级: {len(by_priority['medium'])} 个")
    print(f"  低优先级: {len(by_priority['low'])} 个")
    print()

    # 显示任务列表
    sorted_tasks = by_priority["high"] + by_priority["medium"] + by_priority["low"]

    for idx, task in enumerate(sorted_tasks, 1):
        priority_mark = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        print(
            f"{idx:3d}. {priority_mark[task.priority]} [{task.module_name}] {task.identifier}"
        )
        print(f"     文件: {task.file_path}")
        print(f"     类型: {task.task_type}")
        print()

    print("\n" + "=" * 80)
    print("使用说明:")
    print("1. 这些任务需要AI助手根据源码分析来补充内容")
    print("2. 每个任务包含详细的补充要求和格式说明")
    print("3. 源码上下文信息已自动提取")
    print("=" * 80)
    print()

    print("请选择操作:")
    print("  1. 生成详细的任务提示文件 (供AI参考)")
    print("  2. 查看单个任务详情")
    print("  3. 标记任务为已完成")
    print("  4. 退出")
    print()

    choice = input("请输入选项 (1-4): ").strip()

    if choice == "1":
        # 生成提示文件
        prompt_file = (
            task_file_path.parent
            / f"ai_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        print(f"\n正在生成提示文件: {prompt_file}")
        generate_prompt_file(sorted_tasks, prompt_file, project_root)
        print(f"✓ 提示文件已生成！")
        print(f"\n请将此文件提供给AI助手进行处理:")
        print(f"  {prompt_file}")

    elif choice == "2":
        # 查看单个任务
        task_num = input("\n请输入任务编号: ").strip()
        try:
            task_idx = int(task_num) - 1
            if 0 <= task_idx < len(sorted_tasks):
                task = sorted_tasks[task_idx]

                # 收集源码信息
                source_info = {
                    "functions": [],
                    "structs": [],
                    "enums": [],
                    "includes": [],
                    "comments": [],
                }
                for src_file_rel in task.source_files:
                    src_file_rel = src_file_rel.strip().lstrip("- `").rstrip("`")
                    src_file_path = project_root / src_file_rel
                    if src_file_path.exists():
                        file_info = extract_source_code_info(src_file_path)
                        for key in source_info.keys():
                            source_info[key].extend(file_info[key])

                prompt = build_ai_prompt(task, source_info, project_root)
                print("\n" + prompt)
            else:
                print("无效的任务编号")
        except ValueError:
            print("请输入有效的数字")

    elif choice == "3":
        print("\n[提示] 任务完成功能将在后续版本中实现")
        print("当前请直接编辑文档文件来完成任务")

    elif choice == "4":
        print("\n再见！")
        return

    else:
        print("\n无效的选项")


def main():
    parser = argparse.ArgumentParser(description="AI自动补充工具")
    parser.add_argument("task_file", help="任务JSON文件路径")
    parser.add_argument(
        "--generate-prompts",
        action="store_true",
        help="生成AI提示文件（非交互模式）",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="输出提示文件路径（配合--generate-prompts使用）",
    )

    args = parser.parse_args()

    # 查找项目根目录
    project_root = find_project_root()

    # 加载任务文件
    task_file = Path(args.task_file)
    if not task_file.exists():
        print(f"[ERROR] 任务文件不存在: {task_file}")
        return 1

    print(f"[INFO] 加载任务文件: {task_file}")
    tasks = load_tasks_from_json(task_file)

    if not tasks:
        print("[WARN] 没有找到待处理的任务")
        return 0

    print(f"[INFO] 找到 {len(tasks)} 个任务")

    # 根据模式执行
    if args.generate_prompts:
        # 非交互模式：直接生成提示文件
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = (
                task_file.parent
                / f"ai_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            )

        print(f"[INFO] 生成提示文件: {output_path}")
        generate_prompt_file(tasks, output_path, project_root)
        print(f"[SUCCESS] 提示文件已生成！")
        print(f"\n请将以下文件提供给AI助手:")
        print(f"  {output_path.absolute()}")

    else:
        # 交互模式
        interactive_complete(tasks, project_root, task_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
