#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file    check_outdated.py
@brief   ProjWiki 文档新鲜度检查工具 - 扫描源码与文档的修改时间，找出需要更新的文档
@author  Yarrow
@date    2025-07-11
@attention 用于辅助"智能更新"流程
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def find_project_root():
    """从脚本位置向上查找项目根目录(包含.zed或.git目录)"""
    cur = Path(__file__).resolve().parent
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
    return Path(os.getcwd())


def get_source_mtime(root_dir, module_name):
    """获取模块源文件(.c/.h)的最近修改时间"""
    max_mtime = 0
    c_files = []

    # 简单的递归搜索 (为了更高效，实际应该只扫描一次并缓存，但这足够了)
    # 这里为了简单直接搜名字匹配的文件
    for root, dirs, files in os.walk(root_dir):
        # 忽略 build, .git 等目录
        if ".git" in dirs:
            dirs.remove(".git")
        if ".zed" in dirs:
            dirs.remove(".zed")
        if "build" in dirs:
            dirs.remove("build")
        if "Firmware" in dirs:
            dirs.remove("Firmware")

        for file in files:
            if file == f"{module_name}.c" or file == f"{module_name}.h":
                p = Path(root) / file
                mtime = p.stat().st_mtime
                if mtime > max_mtime:
                    max_mtime = mtime
                c_files.append(str(p.relative_to(root_dir)))

    return max_mtime, c_files


def scan_docs(wiki_dir):
    """扫描所有模块文档"""
    docs = {}
    modules_dir = wiki_dir / "modules"
    if not modules_dir.exists():
        return docs

    for md_file in modules_dir.rglob("*.md"):
        # 假设文件名就是模块名
        module_name = md_file.stem
        docs[module_name] = {"path": md_file, "mtime": md_file.stat().st_mtime}
    return docs


def main():
    root = find_project_root()
    wiki_dir = root / ".zed" / ".projwiki"

    if not wiki_dir.exists():
        print("[ERROR] Wiki directory not found. Please run initialization first.")
        return 1

    print(f"[INFO] Checking documentation freshness in {root}...")

    docs = scan_docs(wiki_dir)
    if not docs:
        print("[WARN] No module documentation found.")
        return 0

    outdated = []

    print(
        f"{'Module':<20} | {'Status':<10} | {'Last Doc Update':<19} | {'Last Source Update':<19}"
    )
    print("-" * 75)

    for module_name, info in docs.items():
        doc_mtime = info["mtime"]
        src_mtime, src_files = get_source_mtime(root, module_name)

        doc_time_str = datetime.fromtimestamp(doc_mtime).strftime("%Y-%m-%d %H:%M:%S")

        if src_mtime == 0:
            status = "Missing Src"
            src_time_str = "N/A"
        elif src_mtime > doc_mtime:
            status = "OUTDATED"
            src_time_str = datetime.fromtimestamp(src_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            outdated.append(
                {
                    "module": module_name,
                    "doc_path": str(info["path"].relative_to(root)),
                    "diff_sec": src_mtime - doc_mtime,
                }
            )
        else:
            status = "Fresh"
            src_time_str = datetime.fromtimestamp(src_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        print(
            f"{module_name:<20} | {status:<10} | {doc_time_str:<19} | {src_time_str:<19}"
        )

    print("-" * 75)

    if outdated:
        print(f"\n[ATTENTION] Found {len(outdated)} outdated documents:")
        print(f"{'Module':<20} | {'Doc Path':<40}")
        print("-" * 65)
        for item in outdated:
            print(f"{item['module']:<20} | {item['doc_path']:<40}")

        # Output strictly structured JSON-like line for parsing if needed
        # print(f"__OUTDATED_LIST__={json.dumps([x['module'] for x in outdated])}")
    else:
        print("\n[OK] All documentation is up to date!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
