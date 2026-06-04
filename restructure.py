import re

with open('/Users/max/Desktop/architettura/12_livello_assembly.html', 'r') as f:
    content = f.read()

# Trova ELF (da <!-- SEZIONE 5: IL FORMATO ELF --> a </section>\n\n  <!-- SEZIONE 5: IL LOADER -->)
elf_match = re.search(r'(<!-- SEZIONE 5: IL FORMATO ELF -->.*?)(?=\n\s*<!-- SEZIONE 5: IL LOADER -->)', content, re.DOTALL)
if not elf_match:
    print("ELF non trovato")
    exit(1)
elf_code = elf_match.group(1)

# Trova Loader (da <!-- SEZIONE 5: IL LOADER --> a </section>\n\n  <!-- EXTRA: BINDING E DLL -->)
loader_match = re.search(r'(<!-- SEZIONE 5: IL LOADER -->.*?)(?=\n\s*<!-- EXTRA: BINDING E DLL -->)', content, re.DOTALL)
if not loader_match:
    print("Loader non trovato")
    exit(1)
loader_code = loader_match.group(1)

# Togliamo il vecchio blocco
new_content = content.replace(elf_code, '')
new_content = new_content.replace(loader_code, '')

# Modifichiamo la fine del loader per aggiungere il link DDL
loader_links = """
        <div style="display:flex; flex-direction:column; gap:16px;">
          <div style="padding:16px; background:rgba(156, 39, 176, 0.05); border-left:4px solid var(--purple); border-radius:8px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
            <span style="font-size:14px; color:var(--text); line-height:1.5;">Il file che il Loader legge dal disco e carica in memoria è strutturato secondo il modello <strong>ELF</strong>.</span>
            <a href="#s5-elf" onclick="document.getElementById('s5-elf').open = true;" style="color:var(--purple); font-size:14px; font-weight:bold; text-decoration:none; white-space:nowrap; background:rgba(156, 39, 176, 0.1); padding:8px 16px; border-radius:6px;">Ripassa il formato ELF &rarr;</a>
          </div>
          <div style="padding:16px; background:rgba(255, 152, 0, 0.05); border-left:4px solid #FF9800; border-radius:8px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
            <span style="font-size:14px; color:var(--text); line-height:1.5;">Le funzioni di libreria possono essere caricate al momento dell'esecuzione tramite il <strong>Lazy Linking</strong>.</span>
            <a href="#extra-binding" onclick="document.getElementById('extra-binding').open = true;" style="color:#FF9800; font-size:14px; font-weight:bold; text-decoration:none; white-space:nowrap; background:rgba(255, 152, 0, 0.1); padding:8px 16px; border-radius:6px;">Scopri le Librerie Dinamiche (DLL) &rarr;</a>
          </div>
        </div>
"""

# Sostituisco il vecchio link ELF con il nuovo contenitore doppio
loader_code = re.sub(
    r'<div style="margin-top:8px; padding:16px; background:rgba\(156, 39, 176, 0\.05\).*?</div>',
    loader_links,
    loader_code,
    flags=re.DOTALL
)

extra_header = """
  <!-- SEZIONE EXTRA -->
  <div style="margin: 64px 0 32px 0; border-bottom: 2px solid var(--border); padding-bottom: 16px;">
    <h2 style="font-size:28px; color:var(--text); margin:0;">Sezioni EXTRA</h2>
    <p style="font-size:15px; color:var(--muted); margin-top:8px;">Approfondimenti tecnici per completare il quadro generale.</p>
  </div>
"""

# Il punto di inserimento è dove prima iniziava ELF: subito dopo la fine del Linker
# Cioè prima di "<!-- EXTRA: BINDING E DLL -->" ma noi avevamo rimosso ELF e Loader, 
# quindi ora dobbiamo reinserire al posto giusto.

insertion_string = loader_code + "\n\n" + extra_header + "\n" + elf_code

new_content = new_content.replace('  <!-- EXTRA: BINDING E DLL -->', insertion_string + '\n\n  <!-- EXTRA: BINDING E DLL -->')

with open('/Users/max/Desktop/architettura/12_livello_assembly.html', 'w') as f:
    f.write(new_content)

print("Restrutturazione completata!")
