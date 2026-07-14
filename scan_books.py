# -*- coding: utf-8 -*-
"""扫描 epub小说合集 目录，重新生成 books.json。
   以后添加新 EPUB 到 epub小说合集/ 后，运行此脚本即可。
   用法：python scan_books.py"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
EPUB_DIR = os.path.join(BASE, 'epub小说合集')

books = []
for fname in sorted(os.listdir(EPUB_DIR)):
    if fname.endswith('.epub'):
        books.append({
            "name": fname,
            "url": "epub小说合集/" + fname
        })

json_path = os.path.join(EPUB_DIR, 'books.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f'Done! {len(books)} books written to books.json')
for b in books:
    print(f'  {b["name"]}')
