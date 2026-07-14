"""Rebuild MST EPUB from existing content, using same structure as working Codex Alera."""
import zipfile, io, os, shutil

FOLDER = r'g:\学习文件\小说\epub小说合集'
src = os.path.join(FOLDER, 'Memory, Sorrow, and Thorn - Complete Trilogy (Tad Williams).epub')
backup = src + '.bak'

# Backup
shutil.copy2(src, backup)
print('Backed up to .bak')

# Read everything
with zipfile.ZipFile(src, 'r') as z:
    all_entries = {}
    for item in z.infolist():
        all_entries[item.filename] = (item, z.read(item.filename))

# Rebuild with mimetype first
new_buf = io.BytesIO()
with zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
    # 1. mimetype first, STORED
    if 'mimetype' in all_entries:
        info, data = all_entries.pop('mimetype')
        zout.writestr(info, data, zipfile.ZIP_STORED)

    # 2. META-INF
    for name in sorted(all_entries):
        if name.startswith('META-INF'):
            info, data = all_entries.pop(name)
            zout.writestr(info, data, zipfile.ZIP_DEFLATED)

    # 3. OEBPS - CSS first, then text, then images
    for prefix in ['OEBPS/css/', 'OEBPS/text/', 'OEBPS/images/']:
        for name in sorted(all_entries):
            if name.startswith(prefix):
                info, data = all_entries.pop(name)
                zout.writestr(info, data, zipfile.ZIP_DEFLATED)

    # 4. OPF last
    for name in sorted(all_entries):
        if name.endswith('.opf'):
            info, data = all_entries.pop(name)
            zout.writestr(info, data, zipfile.ZIP_DEFLATED)

    # 5. Remaining
    for name in sorted(all_entries):
        info, data = all_entries.pop(name)
        zout.writestr(info, data, zipfile.ZIP_DEFLATED)

new_buf.seek(0)
with open(src, 'wb') as f:
    f.write(new_buf.read())

print(f'Rebuilt: {os.path.getsize(src)/1024/1024:.1f} MB')
# Remove backup if no issues
print('Try opening it now. If it works, I will remove the .bak backup.')
