"""Check why epub.js can't read NCX - compare with a working EPUB."""
import zipfile, re, os

FOLDER = r'g:\学习文件\小说\epub小说合集'

# Check a publisher EPUB (has working NCX) vs our merged EPUB
samples = [
    ('Mistborn 01-03 - Complete Trilogy (Brandon Sanderson).epub', 'PUBLISHER'),
    ('Lightbringer - Complete Series 1-5 (Brent Weeks).epub', 'OUR MERGE'),
]

for fname, tag in samples:
    path = os.path.join(FOLDER, fname)
    with zipfile.ZipFile(path, 'r') as z:
        # Find OPF
        opf = [f for f in z.namelist() if f.endswith('.opf')][0]
        c = z.read(opf).decode('utf-8', errors='ignore')

        # Check package version
        ver = re.search(r'version="([^"]*)"', c)
        print(f'\n=== {tag}: {fname[:40]} ===')
        print(f'  OPF version: {ver.group(1) if ver else "?"}')

        # Check spine toc attr
        spine = re.search(r'<spine([^>]*)>', c)
        if spine:
            toc_attr = re.search(r'toc="([^"]*)"', spine.group(1))
            print(f'  Spine toc: {toc_attr.group(1) if toc_attr else "NONE"}')

        # Check NCX
        ncx_files = [f for f in z.namelist() if f.endswith('.ncx')]
        if ncx_files:
            ncx = z.read(ncx_files[0]).decode('utf-8', errors='ignore')
            nav = ncx.count('<navPoint ')
            has_doctype = '<!DOCTYPE' in ncx[:50]
            has_ncx_tag = '<ncx' in ncx[:200]
            print(f'  NCX: {ncx_files[0]} ({len(ncx)} bytes, {nav} navPoints)')
            print(f'  NCX doctype: {has_doctype}, ncx tag: {has_ncx_tag}')

            # Show first 2 navPoints
            first_nav = re.search(r'<navPoint[^>]*>.*?<text>(.*?)</text>.*?</navPoint>', ncx, re.DOTALL)
            if first_nav:
                print(f'  First nav: {first_nav.group(1)[:60]}')

        # Check manifest for NCX entry
        ncx_manifest = re.search(r'media-type="application/x-dtbncx\+xml"', c)
        print(f'  NCX in manifest: {bool(ncx_manifest)}')

        # Check if NCX id matches spine toc
        if ncx_manifest:
            ncx_id = re.search(r'id="([^"]*)"[^>]*application/x-dtbncx\+xml', c)
            if ncx_id and spine:
                toc_match = re.search(r'toc="([^"]*)"', spine.group(1))
                print(f'  NCX manifest id: {ncx_id.group(1)}')
                print(f'  Spine toc ref: {toc_match.group(1) if toc_match else "NONE"}')
                if toc_match and ncx_id:
                    print(f'  IDs MATCH: {ncx_id.group(1) == toc_match.group(1)}')
