import re

with open('02_assembly.html', 'r') as f:
    asm_content = f.read()

with open('03_procedure.html', 'r') as f:
    proc_content = f.read()

# Extract from S10 to end of S12
# S10 starts at <!-- ══════════════ SEZIONE 10 ══════════════ -->
# S13 starts at <!-- ══════════════ SEZIONE 13 ══════════════ -->
s10_12 = asm_content.split('<!-- ══════════════ SEZIONE 10 ══════════════ -->')[1].split('<!-- ══════════════ SEZIONE 13 ══════════════ -->')[0]

# Fix the broken HTML in S10/S11
s10_12 = s10_12.replace('<p style="font-size:11px;color:var(--green);margin-top:8px  <section class="section" id="s11">', 
                        '<p style="font-size:11px;color:var(--green);margin-top:8px">✔ <strong>Vantaggio:</strong> Usa meno registri (0 salvataggi).</p>\n      </div>\n    </div>\n  </section>\n\n  <!-- ══════════════ SEZIONE 11 ══════════════ -->\n  <section class="section" id="s11">')

# Extract from S14 to end of S16
# S14 starts at <!-- ══════════════ SEZIONE 14 ══════════════ -->
# Ends at </main>
s14_16 = proc_content.split('<!-- ══════════════ SEZIONE 14 ══════════════ -->')[1].split('</main>')[0]

header = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RISC-V — Manuale Pratico Assembly</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="layout">

<!-- SIDEBAR -->
<nav class="sidebar">
  <a class="sidebar-title" href="index.html">
    RISC-V Fondamentali
    <span>Guida completa</span>
  </a>
  <a class="nav-item" href="09_manuale_assembly.html#s10">
    <div class="nav-dot"></div> Istruzioni aritmetiche
    <span class="nav-num">10</span>
  </a>
  <a class="nav-item" href="09_manuale_assembly.html#s11">
    <div class="nav-dot"></div> Accesso alla memoria
    <span class="nav-num">11</span>
  </a>
  <a class="nav-item" href="09_manuale_assembly.html#s12">
    <div class="nav-dot"></div> Operazioni logiche e shift
    <span class="nav-num">12</span>
  </a>
  <a class="nav-item" href="09_manuale_assembly.html#s14">
    <div class="nav-dot"></div> Salti e controllo flusso
    <span class="nav-num">14</span>
  </a>
  <a class="nav-item" href="09_manuale_assembly.html#s15">
    <div class="nav-dot"></div> Procedure e convenzioni
    <span class="nav-num">15</span>
  </a>
  <a class="nav-item" href="09_manuale_assembly.html#s16">
    <div class="nav-dot"></div> Le 7 fasi
    <span class="nav-num">16</span>
  </a>
</nav>

<!-- MAIN -->
<main class="main">

  <!-- HERO -->
  <div class="hero">
    <div class="hero-tag">CAPITOLO 09 — MANUALE PRATICO ASSEMBLY</div>
    <h1>Manuale Pratico Assembly<br><em>Istruzioni e Codice RISC-V</em></h1>
    <p>La guida di riferimento per tutte le istruzioni base, l'accesso alla memoria, i salti e le procedure pratiche.</p>
  </div>

  <!-- ══════════════ SEZIONE 10 ══════════════ -->
"""

footer = """</main>
</div>

<script src="shared.js"></script>
</body>
</html>
"""

with open('09_manuale_assembly.html', 'w') as f:
    f.write(header + s10_12 + '<!-- ══════════════ SEZIONE 14 ══════════════ -->\n' + s14_16 + footer)

# Modify 02_assembly.html to remove S10-S12
new_asm = asm_content.split('<!-- ══════════════ SEZIONE 10 ══════════════ -->')[0] + '<!-- ══════════════ SEZIONE 13 ══════════════ -->\n' + asm_content.split('<!-- ══════════════ SEZIONE 13 ══════════════ -->')[1]

# Also remove them from sidebar
new_asm = re.sub(r'  <a class="nav-item" href="02_assembly.html#s10">.*?</a>\n', '', new_asm, flags=re.DOTALL)
new_asm = re.sub(r'  <a class="nav-item" href="02_assembly.html#s11">.*?</a>\n', '', new_asm, flags=re.DOTALL)
new_asm = re.sub(r'  <a class="nav-item" href="02_assembly.html#s12">.*?</a>\n', '', new_asm, flags=re.DOTALL)

with open('02_assembly.html', 'w') as f:
    f.write(new_asm)

# Modify 03_procedure.html to remove S14-S16
new_proc = proc_content.split('<!-- ══════════════ SEZIONE 14 ══════════════ -->')[0] + '</main>\n</div>\n\n<script src="shared.js"></script>\n</body>\n</html>\n'
new_proc = re.sub(r'  <a class="nav-item" href="03_procedure.html#s14">.*?</a>\n', '', new_proc, flags=re.DOTALL)
new_proc = re.sub(r'  <a class="nav-item" href="03_procedure.html#s15">.*?</a>\n', '', new_proc, flags=re.DOTALL)
new_proc = re.sub(r'  <a class="nav-item" href="03_procedure.html#s16">.*?</a>\n', '', new_proc, flags=re.DOTALL)

with open('03_procedure.html', 'w') as f:
    f.write(new_proc)

print("Extraction complete!")
