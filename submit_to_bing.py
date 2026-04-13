#!/usr/bin/env python3
"""
IndexNow 手动提交脚本
使用方法：python3 submit_to_bing.py
功能：自动扫描 _posts/ 目录下所有文章，提交到 Bing IndexNow
"""

import os
import re
import json
import urllib.request
import urllib.error

# ========== 配置区域（根据你的网站修改） ==========
SITE_URL = "https://clashwindow.github.io"
KEY = "1fe0058fde854846b6dbf42dcfc38a20"
HOST = "clashwindow.github.io"
POSTS_DIR = "_posts"
# ==================================================

def get_urls():
    """扫描 _posts 目录，生成所有文章 URL"""
    urls = []
    if not os.path.isdir(POSTS_DIR):
        print(f"错误：找不到 {POSTS_DIR} 目录，请在仓库根目录下运行此脚本")
        return urls

    for filename in sorted(os.listdir(POSTS_DIR)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(POSTS_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r'^permalink:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
            if match:
                permalink = match.group(1).strip()
                url = f"{SITE_URL}{permalink}"
            else:
                basename = filename.replace(".md", "")
                slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', basename)
                url = f"{SITE_URL}/{slug}/"
        except Exception:
            basename = filename.replace(".md", "")
            slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', basename)
            url = f"{SITE_URL}/{slug}/"
        urls.append(url)
    return urls

def submit_urls(urls):
    """提交 URL 到 Bing IndexNow"""
    BATCH = 100
    total_ok = 0
    for i in range(0, len(urls), BATCH):
        batch = urls[i:i+BATCH]
        payload = json.dumps({
            "host": HOST,
            "key": KEY,
            "keyLocation": f"{SITE_URL}/{KEY}.txt",
            "urlList": batch
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                code = resp.getcode()
                print(f"  第 {i//BATCH+1} 批（{len(batch)} 个URL）: HTTP {code} ✅")
                total_ok += len(batch)
        except urllib.error.HTTPError as e:
            print(f"  第 {i//BATCH+1} 批: HTTP {e.code} ❌ - {e.read().decode()[:200]}")
        except Exception as e:
            print(f"  第 {i//BATCH+1} 批: 错误 ❌ - {e}")
    return total_ok

if __name__ == "__main__":
    print("=" * 50)
    print("  IndexNow 手动提交工具")
    print("=" * 50)
    print(f"网站: {SITE_URL}")
    print(f"Key:  {KEY}")
    print()

    urls = get_urls()
    if not urls:
        print("没有找到文章，退出。")
        exit(0)

    print(f"共找到 {len(urls)} 篇文章：")
    for url in urls:
        print(f"  {url}")

    print(f"\n开始提交到 Bing IndexNow...")
    ok = submit_urls(urls)
    print(f"\n{'=' * 50}")
    print(f"完成！{ok}/{len(urls)} 个 URL 提交成功")
    print(f"{'=' * 50}")
