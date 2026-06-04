import os
import shutil

os.chdir('/Users/max/Desktop/architettura')

archive_dir = 'archive'
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

old_files_to_archive = [
    '00_introduzione.html',
    '02_assembly.html',
    '03_procedure.html',
    '04_compilazione.html',
    '05_simulatore.html'
]

for f in old_files_to_archive:
    if os.path.exists(f):
        shutil.move(f, os.path.join(archive_dir, f))

renames = {
    '06_circuiti.html': '02_circuiti.html',
    '07_costruzione_riscv.html': '03_costruzione_riscv.html',
    '08_bus.html': '04_bus.html',
    '09_cache.html': '05_cache.html',
    '10_io.html': '06_io.html',
    '12_livello_assembly.html': '07_livello_assembly.html',
    '11_manuale_assembly.html': '08_manuale_assembly.html',
    '13_prestazioni.html': '09_prestazioni.html'
}

# Fix references in all files (html, js)
files = [f for f in os.listdir('.') if f.endswith('.html') or f == 'shared.js']

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    modified = False
    for old_name, new_name in renames.items():
        if old_name in content:
            content = content.replace(old_name, new_name)
            modified = True
            
    if modified:
        with open(f, 'w') as file:
            file.write(content)

# Rename the actual files
for old_name, new_name in renames.items():
    if os.path.exists(old_name):
        os.rename(old_name, new_name)

print("Done")
