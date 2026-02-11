#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file    build_wiki.py
@brief   ProjWiki HTML站点构建脚本 - 扫描MD文件生成可浏览HTML文档查看器
@author  Yarrow
@date    2025-07-11
@attention 生成的HTML为自包含文件, 可直接在浏览器中打开
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def find_project_root():
    """从脚本位置向上查找项目根目录(包含.zed目录)"""
    cur = Path(__file__).resolve().parent
    for _ in range(10):
        if (cur / ".zed").is_dir():
            return cur
        cur = cur.parent
    print("[ERROR] Cannot find project root (.zed directory not found)")
    sys.exit(1)


def parse_frontmatter(content):
    """解析Markdown YAML frontmatter元数据

    @param   content: Markdown文件完整内容
    @retval  (meta_dict, body_string) 元组
    """
    meta = {}
    body = content
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if m:
        body = content[m.end() :]
        for line in m.group(1).strip().split("\n"):
            line = line.strip()
            if ":" in line:
                k, _, v = line.partition(":")
                k = k.strip()
                v = v.strip()
                # 解析数组
                if v.startswith("[") and v.endswith("]"):
                    v = [
                        x.strip().strip("'").strip('"')
                        for x in v[1:-1].split(",")
                        if x.strip()
                    ]
                # 解析引号字符串
                elif (v.startswith('"') and v.endswith('"')) or (
                    v.startswith("'") and v.endswith("'")
                ):
                    v = v[1:-1]
                meta[k] = v
    return meta, body


def extract_headings(body):
    """从Markdown正文中提取标题结构(用于目录生成)

    @param   body: 去除frontmatter后的Markdown内容
    @retval  标题列表 [{level, text, anchor}, ...]
    """
    headings = []
    in_code = False
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.+)$", s)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            anchor = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", text)
            anchor = re.sub(r"\s+", "-", anchor).lower()
            headings.append({"level": level, "text": text, "anchor": anchor})
    return headings


def scan_wiki(wiki_dir):
    """扫描.projwiki目录, 收集所有MD文件信息

    @param   wiki_dir: .projwiki目录的Path对象
    @retval  文档信息列表
    """
    docs = []
    wp = Path(wiki_dir)
    if not wp.exists():
        print(f"[WARN] Wiki directory not found: {wiki_dir}")
        return docs

    for md_file in sorted(wp.rglob("*.md")):
        rel = str(md_file.relative_to(wp)).replace("\\", "/")

        # 跳过_site目录下的文件
        if rel.startswith("_site/"):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[WARN] Cannot read {md_file}: {e}")
            continue

        meta, body = parse_frontmatter(content)
        headings = extract_headings(body)

        # 从路径推断分类
        parts = rel.split("/")
        cat = parts[0] if len(parts) > 1 else "root"

        # 确定文档标题
        title = meta.get("title", "")
        if not title:
            if headings:
                title = headings[0]["text"]
            else:
                title = md_file.stem.replace("_", " ").title()

        docs.append(
            {
                "path": rel,
                "title": title,
                "category": meta.get("category", cat),
                "date": meta.get("date", ""),
                "author": meta.get("author", "Unknown"),
                "tags": meta.get("tags", []),
                "status": meta.get("status", "draft"),
                "content": content,
                "body": body,
                "headings": headings,
                "modified": datetime.fromtimestamp(md_file.stat().st_mtime).strftime(
                    "%Y-%m-%d %H:%M"
                ),
            }
        )

    return docs


def build_tree(docs):
    """构建文档分类树结构

    @param   docs: scan_wiki返回的文档列表
    @retval  分类树字典 {category: {name, docs: [...]}}
    """
    category_names = {
        "root": "项目总览",
        "modules": "模块文档",
        "api": "API接口",
        "design": "设计文档",
        "hardware": "硬件接口",
        "changelog": "变更日志",
    }

    tree = {}
    for d in docs:
        c = d["category"]
        if c not in tree:
            tree[c] = {"name": category_names.get(c, c.title()), "docs": []}
        tree[c]["docs"].append(
            {
                "path": d["path"],
                "title": d["title"],
                "status": d["status"],
                "date": d["date"],
            }
        )

    return tree


def generate_html(docs, tree, project_name="YTC2400W"):
    """加载HTML模板并注入文档数据生成完整HTML

    @param   docs: 文档列表
    @param   tree: 分类树
    @param   project_name: 项目名称
    @retval  完整的HTML字符串
    """
    # 序列化文档数据(去除body字段, 减小体积)
    docs_json = json.dumps(
        [
            {
                "path": d["path"],
                "title": d["title"],
                "category": d["category"],
                "date": d["date"],
                "author": d["author"],
                "tags": d["tags"] if isinstance(d["tags"], list) else [],
                "status": d["status"],
                "content": d["content"],
                "headings": d["headings"],
                "modified": d["modified"],
            }
            for d in docs
        ],
        ensure_ascii=False,
    )

    tree_json = json.dumps(tree, ensure_ascii=False)
    build_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc_count = len(docs)

    # 查找HTML模板文件
    tpl_path = Path(__file__).resolve().parent / "viewer_template.html"
    if not tpl_path.exists():
        print(f"[ERROR] HTML template not found: {tpl_path}")
        print(
            "[HINT] viewer_template.html should be in the same directory as build_wiki.py"
        )
        sys.exit(1)

    html = tpl_path.read_text(encoding="utf-8")

    # 注入数据到模板占位符
    html = html.replace("/*__DOCS_DATA__*/", docs_json)
    html = html.replace("/*__TREE_DATA__*/", tree_json)
    html = html.replace("__BUILD_TIME__", build_time)
    html = html.replace("__DOC_COUNT__", str(doc_count))
    html = html.replace("__PROJECT_NAME__", project_name)

    return html


def main():
    """主入口函数"""
    root = find_project_root()
    wiki_dir = root / ".zed" / ".projwiki"
    site_dir = wiki_dir / "_site"

    # 确保输出目录存在
    site_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Project root : {root}")
    print(f"[INFO] Wiki directory: {wiki_dir}")
    print(f"[INFO] Output dir    : {site_dir}")
    print()

    # 扫描文档
    docs = scan_wiki(wiki_dir)
    print(f"[INFO] Found {len(docs)} document(s)")

    if not docs:
        print("[WARN] No documents found in .zed/.projwiki/")
        print(
            "[HINT] Create .md files in subdirectories: modules/, api/, design/, hardware/, changelog/"
        )

    # 构建分类树
    tree = build_tree(docs)
    cat_names = [f"{k}({len(v['docs'])})" for k, v in tree.items()]
    print(f"[INFO] Categories: {', '.join(cat_names) if cat_names else '(none)'}")

    # 生成HTML
    html = generate_html(docs, tree)

    # 写入输出文件
    out_path = site_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")

    file_size_kb = out_path.stat().st_size / 1024
    print()
    print(f"[OK] Generated: {out_path}")
    print(f"[OK] File size: {file_size_kb:.1f} KB")
    print(f"[OK] Open in browser to view documentation")

    return 0


if __name__ == "__main__":
    sys.exit(main())
