import os
import re
import json
import urllib.request
import urllib.error

SITE_URL = "https://clashwindow.github.io"
KEY = "8575fe8139f14b2da85e40bbc8b86ce2"
HOST = "clashwindow.github.io"

posts_dir = "_posts"
if not os.path.isdir(posts_dir):
    print("No _posts directory found.")
    exit(0)

urls = []
for filename in sorted(os.listdir(posts_dir)):
    if not filename.endswith(".md"):
        continue
    filepath = os.path.join(posts_dir, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"^permalink:\s*(.+)$", content, re.MULTILINE)
        if match:
            permalink = match.group(1).strip().strip("\"'")
            url = SITE_URL + permalink
        else:
            basename = filename.replace(".md", "")
            slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", basename)
            url = SITE_URL + "/" + slug + "/"
    except Exception:
        basename = filename.replace(".md", "")
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", basename)
        url = SITE_URL + "/" + slug + "/"
    urls.append(url)

print("Total URLs: " + str(len(urls)))

if not urls:
    print("No URLs to submit.")
    exit(0)

BATCH = 100
total_ok = 0
for i in range(0, len(urls), BATCH):
    batch = urls[i:i+BATCH]
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": SITE_URL + "/" + KEY + ".txt",
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
        print("Batch " + str(i//BATCH+1) + ": " + str(len(batch)) + " URLs -> HTTP " + str(code) + " OK")
        total_ok += len(batch)
        resp.close()
    except urllib.error.HTTPError as e:
        print("Batch " + str(i//BATCH+1) + ": HTTP " + str(e.code))
    except Exception as e:
        print("Batch " + str(i//BATCH+1) + ": Error - " + str(e))

print("")
print("Done! " + str(total_ok) + "/" + str(len(urls)) + " URLs submitted to Bing IndexNow.")
