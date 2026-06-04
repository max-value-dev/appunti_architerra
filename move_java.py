import re

with open('/Users/max/Desktop/architettura/12_livello_assembly.html', 'r') as f:
    content = f.read()

# Trova la sezione EXTRA: JAVA (da <!-- EXTRA: JAVA --> a </section>)
java_match = re.search(r'(<!-- EXTRA: JAVA -->.*?</section>)', content, re.DOTALL)
if not java_match:
    print("Java section not found")
    exit(1)

java_code = java_match.group(1)

# Rimuovi la sezione Java dal punto originale
content = content.replace(java_code, '')

# Trova il marker in cui inserire (subito dopo l'intestazione EXTRA)
header_match = re.search(r'(<!-- SEZIONE EXTRA -->.*?</div>\n)', content, re.DOTALL)
if not header_match:
    print("Extra header not found")
    exit(1)

header_code = header_match.group(1)

# Inserisci Java subito dopo l'intestazione
new_content = content.replace(header_code, header_code + '\n' + java_code + '\n')

with open('/Users/max/Desktop/architettura/12_livello_assembly.html', 'w') as f:
    f.write(new_content)

print("Java moved successfully!")
