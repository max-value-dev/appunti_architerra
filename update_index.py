import re

with open('/Users/max/Desktop/architettura/index.html', 'r') as f:
    content = f.read()

# 1. Update Grid
grid_match = re.search(r'(<!-- CHAPTERS GRID -->(.*?)\n\s*)</div>\n\s*</div>\n\s*<script>', content, re.DOTALL)
grid_content = grid_match.group(2)

card_pattern = r'(<!-- CAPITOLO \d+ -->\n\s*<a href="([^"]+)" .*?</a>)'
cards = re.findall(card_pattern, grid_content, re.DOTALL)

cards_dict = {filename: full_card_html for full_card_html, filename in cards}

keep_files = [
    '01_fondamenti.html',
    '06_circuiti.html',
    '07_costruzione_riscv.html',
    '08_bus.html',
    '09_cache.html',
    '10_io.html',
    '12_livello_assembly.html',
    '11_manuale_assembly.html'
]

new_grid_content = '\n    <!-- CHAPTERS GRID -->\n'

for idx, filename in enumerate(keep_files):
    if filename in cards_dict:
        html = cards_dict[filename]
        html = re.sub(r'<!-- CAPITOLO \d+ -->', f'<!-- CAPITOLO {idx+1} -->', html)
        html = re.sub(r'<div class="cat-icon">\d+</div>', f'<div class="cat-icon">{idx+1:02d}</div>', html)
        # Update colors if we want to keep them sequential, but leaving them as is fine (c1, c2, c3 etc.)
        new_grid_content += '\n    ' + html.strip() + '\n'

new_grid_content = new_grid_content + '\n\n  '

content = content.replace(grid_match.group(1), new_grid_content)

# 2. Update JS Array
sections_match = re.search(r'(const SECTIONS = \[\n(.*?)\n\];)', content, re.DOTALL)
if sections_match:
    full_array = sections_match.group(1)
    inner_lines = sections_match.group(2).split('\n')
    
    new_lines = []
    for line in inner_lines:
        keep = False
        for kf in keep_files:
            if kf in line:
                keep = True
                break
        if keep:
            new_lines.append(line)
            
    # Fix commas (the last item shouldn't have a comma, though JS permits trailing commas)
    if new_lines and new_lines[-1].endswith(','):
        new_lines[-1] = new_lines[-1][:-1]
        
    new_array = "const SECTIONS = [\n" + '\n'.join(new_lines) + "\n];"
    content = content.replace(full_array, new_array)

with open('/Users/max/Desktop/architettura/index.html', 'w') as f:
    f.write(content)

print("Index updated successfully!")
