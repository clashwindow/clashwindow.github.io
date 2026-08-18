#!/usr/bin/env python3
"""
IndexNow 提交脚本 - 仅提交最新更新的 URL，避免重复提交
"""
import os
import subprocess
import re
import json
import urllib.request
import urllib.error
import yaml

# 加载 _config.yml 获取 IndexNow 设置
with open('_config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

SITE_URL = config.get('url', 'https://clashwindow.github.io')
KEY = config.get('indexnow', {}).get('key', 'YOUR_INDEXNOW_KEY')
HOST = config.get('indexnow', {}).get('host', 'clashwindow.github.io')
KEY_LOCATION = SITE_URL + config.get('indexnow', {}).get('key_location', '/' + KEY + '.txt')

posts_dir = "_posts"
if not os.path.isdir(posts_dir):
    print("❌ 没有找到 _posts 目录")
    exit(0)

import subprocess

# 获取最近 10 次提交变更的文件列表（GitHub Actions checkout 后文件 mtime 统一为 checkout 时间，
# 无法按 mtime 过滤；通过 git log 获取实际变更的文章）
changed_fnames = set()
try:
    result = subprocess.run(
        ['git', 'log', '--name-only', '--pretty=format:', '-10'],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0:
        changed_files = set(result.stdout.strip().split('\n'))
        changed_fnames = {os.path.basename(f) for f in changed_files if f.startswith('_posts/') and f.endswith('.md')}
        print(f"📋 最近 10 次提交变更的文章: {len(changed_fnames)} 个")
    else:
        print(f"⚠️  git log 返回错误: {result.stderr[:200]}")
except Exception as e:
    changed_fnames = set()
    print(f"⚠️  获取变更列表失败: {e}")

print()

urls = []
for filename in sorted(changed_fnames):
    filepath = os.path.join(posts_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 尝试从 Front Matter 中提取 permalink
        match = re.search(r"^permalink:\s*(.+)$", content, re.MULTILINE)
        if match:
            permalink = match.group(1).strip().strip("\"'")
            url = SITE_URL + permalink
        else:
            # 从文件名生成 URL
            basename = filename.replace(".md", "")
            slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", basename)
            url = SITE_URL + "/" + slug + "/"
    except Exception as e:
        print(f"⚠️  处理 {filename} 时出错: {e}")
        basename = filename.replace(".md", "")
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", basename)
        url = SITE_URL + "/" + slug + "/"
    
    urls.append(url)

print(f"📝 找到 {len(urls)} 个需要提交的 URL（最近 24 小时内修改）")
print()

if not urls:
    print("✅ 没有新的 URL 需要提交")
    exit(0)

# 打印要提交的 URL
for i, url in enumerate(urls, 1):
    print(f"   {i}. {url}")

print()

# 分批提交 URL（IndexNow API 限制每批 100 个）
BATCH_SIZE = 100
total_submitted = 0

for i in range(0, len(urls), BATCH_SIZE):
    batch = urls[i:i+BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": batch
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        code = resp.getcode()
        print(f"✅ 批次 {batch_num}: {len(batch)} 个 URL -> HTTP {code}")
        total_submitted += len(batch)
        resp.close()
    except urllib.error.HTTPError as e:
        print(f"❌ 批次 {batch_num}: HTTP {e.code}")
        if e.code == 400:
            print(f"   错误: 请求格式错误，请检查 key 和 keyLocation 配置")
        elif e.code == 403:
            print(f"   错误: 认证失败，请检查 key 是否正确")
    except Exception as e:
        print(f"❌ 批次 {batch_num}: 错误 - {str(e)}")

print()
print(f"🎉 完成! {total_submitted}/{len(urls)} 个 URL 已提交到 Bing IndexNow")
print()
print("💡 提示:")
print("   - IndexNow 会在 24-48 小时内处理这些 URL")
print("   - 只有最近 24 小时内修改的文章会被提交")
print("   - 避免重复提交相同的 URL，节省配额")
