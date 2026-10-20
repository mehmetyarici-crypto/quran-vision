import re
import urllib.request
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(r"c:\Users\YARICI AİLESİ\Desktop\DKAB 2026\GEM\quran-vision")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

files = sorted((ROOT / "docs" / "tr").glob("*-v6.1.1.md")) + sorted((ROOT / "docs" / "en").glob("*-en-v6.1.1.md"))

url_locations = defaultdict(list)
for f in files:
    if f.name.startswith("05-"):
        continue
    text = f.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"https://shamela\.ws/book/\d+/\d+(?:/\d+)?", line):
            url_locations[m.group(0)].append((f.name, line_no))

unique_urls = sorted(url_locations.keys())
print(f"Total unique Shamela URLs across 30 files: {len(unique_urls)}")

def verify_url(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            t_m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
            title = t_m.group(1).strip() if t_m else ""
            # Extract vol/page from title (e.g. ج3 - ص186 - كتاب ...)
            vp_m = re.match(r"^((?:ج\d+\s*-\s*)?ص\d+)\s*-\s*(.*?)\s*-\s*المكتبة الشاملة$", title)
            if vp_m:
                vol_page = vp_m.group(1).strip()
                book_and_sec = vp_m.group(2).strip()
            else:
                vol_page = "?"
                book_and_sec = title
            # Extract breadcrumb
            b_m = re.search(r"مسار الصفحة الحالية:.*?<div class=\"size-12\">(.*?)</div>", html, re.DOTALL)
            if b_m:
                crumbs = [re.sub(r"<[^>]+>", "", s).strip() for s in re.findall(r"<span class=\"text-black\">(.*?)</span>", b_m.group(1))]
                breadcrumb = " > ".join(crumbs)
            else:
                breadcrumb = ""
            return url, resp.status, vol_page, book_and_sec, breadcrumb
    except Exception as e:
        return url, f"ERR: {e}", "", "", ""

failures = 0
with ThreadPoolExecutor(max_workers=10) as ex:
    for url, status, vp, book_sec, crumb in ex.map(verify_url, unique_urls):
        locs = f"{len(url_locations[url])} refs (e.g. {url_locations[url][0][0]}:{url_locations[url][0][1]})"
        if status != 200:
            failures += 1
        print(f"[{status}] {url:36s} | {vp:12s} | {book_sec}\n      BREADCRUMB: {crumb} | [{locs}]")

print(f"\nSUMMARY: {len(unique_urls)} unique URLs checked, {failures} failures.")
