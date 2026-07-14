"""Fix: NCX file path mismatch - move toc.ncx into OEBPS/ where OPF expects it."""
import zipfile, io, os

FOLDER = r'g:\学习文件\小说\epub小说合集'

FILES = [
    'Codex Alera - Complete Series 1-6 (Jim Butcher).epub',
    'Lightbringer - Complete Series 1-5 (Brent Weeks).epub',
    'Memory, Sorrow, and Thorn - Complete Trilogy (Tad Williams).epub',
    "Kushiel's Legacy 01 - Kushiel's Dart (Jacqueline Carey).epub",
]

for fname in FILES:
    path = os.path.join(FOLDER, fname)
    print(f'\nFixing: {fname[:50]}...')

    new_buf = io.BytesIO()
    with zipfile.ZipFile(path, 'r') as zin:
        with zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)

                # Fix: if NCX is at root but OPF is in OEBPS/, move NCX into OEBPS/
                new_name = item.filename
                if item.filename == 'toc.ncx':
                    new_name = 'OEBPS/toc.ncx'
                    print(f'  Moving toc.ncx -> OEBPS/toc.ncx')

                info = zipfile.ZipInfo(new_name)
                info.date_time = item.date_time

                if new_name == 'mimetype':
                    zout.writestr(info, data, zipfile.ZIP_STORED)
                else:
                    zout.writestr(info, data, zipfile.ZIP_DEFLATED)

    new_buf.seek(0)
    with open(path, 'wb') as f:
        f.write(new_buf.read())

print('\nDone!')
