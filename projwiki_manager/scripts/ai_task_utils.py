#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file    ai_task_utils.py
@brief   AI填空任务处理工具库 - 提取、生成、管理AI补充任务
@author  Yarrow
@date    2025-01-10
@attention 用于支持文档AI自动补充功能
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


class AIFillTask:
    """AI填空任务数据类"""

    def __init__(
        self,
        task_id: str,
        file_path: str,
        identifier: str,
        task_type: str,
        priority: str,
        requirement: str,
        context_type: str,
        format_hint: str = "",
        start_line: int = 0,
        end_line: int = 0,
        placeholder_content: str = "",
        source_files: List[str] | None = None,
        module_name: str = "",
    ):
        self.task_id = task_id
        self.file_path = file_path
        self.identifier = identifier
        self.task_type = task_type
        self.priority = priority
        self.requirement = requirement
        self.context_type = context_type
        self.format_hint = format_hint
        self.start_line = start_line
        self.end_line = end_line
        self.placeholder_content = placeholder_content
        self.source_files = source_files or []
        self.module_name = module_name
        self.status = "pending"
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
        self.ai_response = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "task_id": self.task_id,
            "file_path": self.file_path,
            "identifier": self.identifier,
            "task_type": self.task_type,
            "priority": self.priority,
            "requirement": self.requirement,
            "context_type": self.context_type,
            "format_hint": self.format_hint,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "placeholder_content": self.placeholder_content,
            "source_files": self.source_files,
            "module_name": self.module_name,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "ai_response": self.ai_response,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AIFillTask":
        """从字典创建任务对象"""
        task = cls(
            task_id=data["task_id"],
            file_path=data["file_path"],
            identifier=data["identifier"],
            task_type=data["task_type"],
            priority=data["priority"],
            requirement=data["requirement"],
            context_type=data["context_type"],
            format_hint=data.get("format_hint", ""),
            start_line=data.get("start_line", 0),
            end_line=data.get("end_line", 0),
            placeholder_content=data.get("placeholder_content", ""),
            source_files=data.get("source_files", []),
            module_name=data.get("module_name", ""),
        )
        task.status = data.get("status", "pending")
        task.created_at = data.get("created_at", datetime.now().isoformat())
        task.completed_at = data.get("completed_at")
        task.ai_response = data.get("ai_response")
        return task


def extract_ai_fill_markers(
    md_content: str, file_path: str
) -> List[Tuple[str, Dict[str, Any], int, int, str]]:
    """
    从Markdown内容中提取AI填空标记

    返回: List[(identifier, metadata, start_line, end_line, placeholder_content)]
    """
    pattern = re.compile(
        r"<!-- AI_FILL_START:(\w+)\n"
        r"(.*?)"
        r"-->\n"
        r"(.*?)\n"
        r"<!-- AI_FILL_END:\1 -->",
        re.DOTALL,
    )

    results = []
    lines = md_content.split("\n")

    for match in pattern.finditer(md_content):
        identifier = match.group(1)
        metadata_text = match.group(2)
        placeholder = match.group(3)

        # 解析元数据
        metadata = {}
        for line in metadata_text.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        # 计算行号
        start_pos = match.start()
        end_pos = match.end()
        start_line = md_content[:start_pos].count("\n") + 1
        end_line = md_content[:end_pos].count("\n") + 1

        results.append((identifier, metadata, start_line, end_line, placeholder))

    return results


def create_tasks_from_markers(
    markers: List[Tuple[str, Dict[str, Any], int, int, str]],
    file_path: str,
    module_name: str,
    source_files: List[str],
) -> List[AIFillTask]:
    """从提取的标记创建任务列表"""
    tasks = []

    for idx, (identifier, metadata, start_line, end_line, placeholder) in enumerate(
        markers
    ):
        task_id = f"{module_name}_{identifier}_{idx:03d}"

        task = AIFillTask(
            task_id=task_id,
            file_path=file_path,
            identifier=identifier,
            task_type=metadata.get("Type", "unknown"),
            priority=metadata.get("Priority", "medium"),
            requirement=metadata.get("Requirement", ""),
            context_type=metadata.get("Context", "source_analysis"),
            format_hint=metadata.get("Format", ""),
            start_line=start_line,
            end_line=end_line,
            placeholder_content=placeholder.strip(),
            source_files=source_files,
            module_name=module_name,
        )

        tasks.append(task)

    return tasks


def save_tasks_to_json(tasks: List[AIFillTask], output_path: Path) -> None:
    """保存任务列表到JSON文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    tasks_dict = {
        "generated_at": datetime.now().isoformat(),
        "total_tasks": len(tasks),
        "tasks": [task.to_dict() for task in tasks],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tasks_dict, f, ensure_ascii=False, indent=2)


def load_tasks_from_json(json_path: Path) -> List[AIFillTask]:
    """从JSON文件加载任务列表"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [AIFillTask.from_dict(task_data) for task_data in data["tasks"]]


def extract_source_code_info(source_file: Path) -> Dict[str, Any]:
    """
    从源文件中提取关键信息

    返回: {
        'functions': List[Dict],  # 函数列表
        'structs': List[Dict],    # 结构体列表
        'enums': List[Dict],      # 枚举列表
        'includes': List[str],    # 包含的头文件
        'comments': List[str],    # 关键注释
    }
    """
    if not source_file.exists():
        return {
            "functions": [],
            "structs": [],
            "enums": [],
            "includes": [],
            "comments": [],
        }

    try:
        content = source_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {
            "functions": [],
            "structs": [],
            "enums": [],
            "includes": [],
            "comments": [],
        }

    info = {
        "functions": extract_functions(content),
        "structs": extract_structs(content),
        "enums": extract_enums(content),
        "includes": extract_includes(content),
        "comments": extract_important_comments(content),
    }

    return info


def extract_functions(content: str) -> List[Dict[str, str]]:
    """提取函数签名"""
    # 简化版：匹配函数声明
    pattern = re.compile(
        r"^\s*([\w\*]+)\s+([\w]+)\s*\((.*?)\)\s*[;{]",
        re.MULTILINE,
    )

    functions = []
    for match in pattern.finditer(content):
        return_type = match.group(1).strip()
        func_name = match.group(2).strip()
        params = match.group(3).strip()

        functions.append(
            {
                "name": func_name,
                "return_type": return_type,
                "params": params,
            }
        )

    return functions


def extract_structs(content: str) -> List[Dict[str, str]]:
    """提取结构体定义"""
    pattern = re.compile(
        r"typedef\s+struct\s*\{(.*?)\}\s*(\w+);",
        re.DOTALL,
    )

    structs = []
    for match in pattern.finditer(content):
        body = match.group(1).strip()
        name = match.group(2).strip()

        structs.append(
            {
                "name": name,
                "body": body,
            }
        )

    return structs


def extract_enums(content: str) -> List[Dict[str, str]]:
    """提取枚举定义"""
    pattern = re.compile(
        r"typedef\s+enum\s*\{(.*?)\}\s*(\w+);",
        re.DOTALL,
    )

    enums = []
    for match in pattern.finditer(content):
        body = match.group(1).strip()
        name = match.group(2).strip()

        enums.append(
            {
                "name": name,
                "body": body,
            }
        )

    return enums


def extract_includes(content: str) -> List[str]:
    """提取包含的头文件"""
    pattern = re.compile(r'#include\s+[<"]([^>"]+)[>"]')
    return pattern.findall(content)


def extract_important_comments(content: str) -> List[str]:
    """提取重要注释（包含特殊标记）"""
    important_markers = ["WARNING", "FIXME", "TODO", "NOTE", "HACK", "ATTENTION"]

    comments = []
    # 提取/** ... */ 和 /* ... */ 注释
    pattern = re.compile(r"/\*\*?(.*?)\*/", re.DOTALL)

    for match in pattern.finditer(content):
        comment_text = match.group(1).strip()
        # 检查是否包含重要标记
        if any(marker in comment_text for marker in important_markers):
            comments.append(comment_text)
        # 或者是否是文件头/函数头注释
        elif "@brief" in comment_text or "@file" in comment_text:
            comments.append(comment_text)

    return comments[:10]  # 限制数量


def generate_task_summary(tasks: List[AIFillTask]) -> str:
    """生成任务摘要报告"""
    total = len(tasks)
    by_priority = {"high": 0, "medium": 0, "low": 0}
    by_type = {}

    for task in tasks:
        by_priority[task.priority] = by_priority.get(task.priority, 0) + 1
        by_type[task.task_type] = by_type.get(task.task_type, 0) + 1

    summary = f"""
AI填空任务摘要
{"=" * 60}
总任务数: {total}

按优先级分类:
  - 高优先级 (high):   {by_priority.get("high", 0)}
  - 中优先级 (medium): {by_priority.get("medium", 0)}
  - 低优先级 (low):    {by_priority.get("low", 0)}

按类型分类:
"""

    for task_type, count in sorted(by_type.items()):
        summary += f"  - {task_type}: {count}\n"

    summary += "\n任务列表:\n"
    summary += "-" * 60 + "\n"

    for task in tasks:
        summary += f"[{task.priority.upper()}] {task.task_id}\n"
        summary += f"  文件: {task.file_path}\n"
        summary += f"  类型: {task.task_type}\n"
        summary += f"  要求: {task.requirement[:80]}...\n"
        summary += "\n"

    return summary
