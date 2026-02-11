#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file    scaffold_docs.py
@brief   ProjWiki 文档脚手架工具 - 扫描源码自动生成模块文档草稿（含AI填空任务生成）
@author  Yarrow
@date    2025-07-11
@attention 仅生成不存在的文档，不会覆盖已有文档
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# 导入AI任务工具
try:
    from ai_task_utils import (
        create_tasks_from_markers,
        extract_ai_fill_markers,
        generate_task_summary,
        save_tasks_to_json,
    )

    AI_TASK_SUPPORT = True
except ImportError:
    AI_TASK_SUPPORT = False
    print("[WARN] ai_task_utils not found. AI task generation disabled.")


def find_project_root():
    """从脚本位置向上查找项目根目录(包含.zed目录)"""
    cur = Path(__file__).resolve().parent
    # Check up to 10 levels up
    for _ in range(10):
        if (cur / ".zed").is_dir():
            return cur
        if (cur / ".git").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent

    # Fallback: check CWD
    cur = Path(os.getcwd())
    if (cur / ".zed").is_dir() or (cur / ".git").is_dir():
        return cur

    # Final fallback: assume CWD is root
    print(
        "[WARN] Cannot find project root marker (.zed or .git). Assuming CWD is root."
    )
    return Path(os.getcwd())


def find_template(use_ai_template=False):
    """查找模块文档模板文件"""
    # 脚本所在目录
    script_dir = Path(__file__).resolve().parent

    # 根据参数选择模板
    template_name = "module_doc_ai.md" if use_ai_template else "module_doc.md"

    # 尝试查找 ../templates/模板文件
    tpl_path = script_dir.parent / "templates" / template_name

    if not tpl_path.exists():
        # 尝试查找当前目录下的 templates (如果不按标准结构部署)
        tpl_path = script_dir / "templates" / template_name

    if not tpl_path.exists():
        # 如果AI模板不存在，回退到普通模板
        if use_ai_template:
            print(f"[WARN] AI template not found, falling back to standard template")
            return find_template(use_ai_template=False)
        print(f"[ERROR] Template not found at {tpl_path}")
        sys.exit(1)

    return tpl_path


def scan_sources(root_dir):
    """扫描项目源码，识别模块"""
    modules = {}

    # 定义需要忽略的目录
    ignore_dirs = {
        ".git",
        ".zed",
        ".vscode",
        ".idea",
        "build",
        "dist",
        "node_modules",
        "venv",
        "__pycache__",
        "Firmware",
    }

    print(f"[INFO] Scanning sources in {root_dir}...")

    for root, dirs, files in os.walk(root_dir):
        # 过滤忽略目录
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(".c"):
                name = file[:-2]  # remove .c
                if name not in modules:
                    modules[name] = {"c": [], "h": []}
                modules[name]["c"].append(os.path.join(root, file))
            elif file.endswith(".h"):
                name = file[:-2]  # remove .h
                if name not in modules:
                    modules[name] = {"c": [], "h": []}
                modules[name]["h"].append(os.path.join(root, file))

    return modules


def generate_doc(
    module_name, info, template_content, output_dir, project_root, collect_tasks=False
):
    """生成单个模块文档，可选生成AI填空任务"""
    md_path = output_dir / f"{module_name}.md"

    if md_path.exists():
        return None  # Skip existing

    # 准备替换内容
    c_files = [
        str(Path(p).relative_to(project_root)).replace("\\", "/") for p in info["c"]
    ]
    h_files = [
        str(Path(p).relative_to(project_root)).replace("\\", "/") for p in info["h"]
    ]

    source_list = ""
    for f in c_files:
        source_list += f"- `{f}`\n"
    for f in h_files:
        source_list += f"- `{f}`\n"

    # 简单的层级推断
    layer = "Application"
    lower_name = module_name.lower()
    if (
        "bsp" in lower_name
        or "driver" in lower_name
        or "hal" in lower_name
        or "hw" in lower_name
    ):
        layer = "Hardware"
    elif "mid" in lower_name or "os" in lower_name or "sys" in lower_name:
        layer = "Middleware"
    elif "calc" in lower_name or "alg" in lower_name or "math" in lower_name:
        layer = "Calculation"

    # 替换模板变量
    content = template_content
    content = content.replace("[模块名称]", module_name)
    content = content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))
    content = content.replace(
        "layer: Application | Middleware | Calculation | Hardware", f"layer: {layer}"
    )

    # 替换源文件部分
    # 模板中是:
    # - `<Layer>/<MODULE_NAME>.c`
    # - `<Layer>/<MODULE_NAME>.h`
    if "- `<Layer>/<MODULE_NAME>.c`" in content:
        content = content.replace(
            "- `<Layer>/<MODULE_NAME>.c`\n- `<Layer>/<MODULE_NAME>.h`",
            source_list.strip(),
        )
    else:
        # 如果模板格式变了，尝试找 "**源文件**：" 后面
        pass

    # 写入文件
    try:
        md_path.write_text(content, encoding="utf-8")

        # 如果启用AI任务收集，提取任务
        if collect_tasks and AI_TASK_SUPPORT:
            markers = extract_ai_fill_markers(content, str(md_path))
            if markers:
                tasks = create_tasks_from_markers(
                    markers,
                    str(md_path.relative_to(project_root)),
                    module_name,
                    source_list.strip().split("\n"),
                )
                return tasks

        return []  # 返回空任务列表表示成功但无任务
    except Exception as e:
        print(f"[ERROR] Failed to write {md_path}: {e}")
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(description="ProjWiki文档脚手架工具")
    parser.add_argument(
        "--ai-fill", action="store_true", help="使用AI填空模板并生成待补充任务"
    )
    args = parser.parse_args()

    try:
        root = find_project_root()
    except SystemExit:
        # 如果找不到 root，但只要能找到模板和有写权限，也许可以在当前目录工作？
        # 还是严格一点好
        return 1

    wiki_modules_dir = root / ".zed" / ".projwiki" / "modules"
    ai_tasks_dir = root / ".zed" / ".projwiki" / ".ai_tasks"

    # 确保输出目录存在
    wiki_modules_dir.mkdir(parents=True, exist_ok=True)
    if args.ai_fill:
        ai_tasks_dir.mkdir(parents=True, exist_ok=True)

    # 加载模板
    tpl_path = find_template(use_ai_template=args.ai_fill)
    try:
        tpl_content = tpl_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] Could not read template: {e}")
        return 1

    print(f"[INFO] Using template: {tpl_path.name}")
    if args.ai_fill:
        print("[INFO] AI填空模式已启用")

    # 扫描源码
    modules = scan_sources(root)
    print(f"[INFO] Found {len(modules)} potential modules.")

    created_count = 0
    skipped_count = 0
    all_tasks = []

    for name, info in modules.items():
        # 忽略只有头文件且看起来像公共定义的模块 (可选)
        if not info["c"] and len(info["h"]) == 1:
            continue

        result = generate_doc(
            name, info, tpl_content, wiki_modules_dir, root, collect_tasks=args.ai_fill
        )

        if result is None:
            # 跳过已存在的文档
            skipped_count += 1
        elif isinstance(result, list):
            # 成功创建，可能有任务
            print(f"[NEW] Created {name}.md")
            if result:
                print(f"      └─ 生成了 {len(result)} 个AI填空任务")
                all_tasks.extend(result)
            created_count += 1

    print("-" * 40)
    print(f"[SUMMARY] Created: {created_count}, Skipped (Existing): {skipped_count}")

    # 保存AI任务
    if args.ai_fill and all_tasks and AI_TASK_SUPPORT:
        task_file = (
            ai_tasks_dir
            / f"pending_tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        save_tasks_to_json(all_tasks, task_file)
        print(f"\n[AI TASKS] 生成了 {len(all_tasks)} 个待补充任务")
        print(f"[AI TASKS] 任务文件: {task_file}")
        print("\n" + generate_task_summary(all_tasks))
        print(
            f"\n[NEXT] 运行 'python scripts/ai_complete.py {task_file}' 来处理AI填空任务"
        )

    print(
        f"[NEXT] Run 'python .claude/skills/projwiki_manager/scripts/build_wiki.py' to update HTML."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
