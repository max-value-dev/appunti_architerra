with open('06_circuiti.html', 'r') as f:
    content = f.read()

import re

# 1. Update Decoder image path
content = content.replace('src="decoder.png"', 'src="assets/decoder.png"')

# 2. Replace Multiplexer HTML section
start_str = '<div class="widget-title">Simulatore Interattivo: Multiplexer</div>'
start_idx = content.find(start_str)

end_str = '</svg>'
end_idx = content.find(end_str, start_idx) + len(end_str)

replacement_html = '''<div class="card green" style="margin-bottom: 24px;">
      <div class="card-title">Come funziona il circuito:</div>
      <ol style="font-size:14px; margin-top:8px; padding-left:20px; line-height:1.6; color:var(--text)">
        <li><strong>I Dati (D0-D7):</strong> A sinistra entrano gli 8 cavi che trasportano i vari dati possibili. Ognuno finisce direttamente in una porta AND.</li>
        <li><strong>I Selettori (A, B, C):</strong> In basso entrano i 3 fili di controllo. Anche in questo caso si sdoppiano in linee verticali normali e negate (passando per i <code>NOT</code>).</li>
        <li><strong>La "Serratura" AND:</strong> Ogni porta AND riceve 4 fili: 1 cavo dati e 3 cavi di controllo. Solo <strong>una</strong> porta AND alla volta riceverà dai cavi di controllo la combinazione magica <code>1-1-1</code>. </li>
        <li><strong>Il passaggio del Dato:</strong> La singola porta AND "sbloccata" lascerà passare il segnale del suo cavo dati. Tutte le altre porte AND resteranno sbarrate a 0.</li>
        <li><strong>La grande porta OR:</strong> Raccoglie i risultati di tutte le 8 porte AND. Poiché 7 porte emettono 0 e solo 1 emette il segnale del dato, l'uscita finale `F` sarà esattamente uguale al dato selezionato!</li>
      </ol>
    </div>
    
    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: Schema del Multiplexer</div>
      <img src="assets/multiplexer.png" alt="Schema Multiplexer 8 a 1" style="width:100%; border-radius:8px; border:1px solid var(--border); margin-top:10px;">'''

content = content[:start_idx] + replacement_html + content[end_idx:]

# 3. Remove Multiplexer JS logic
js_start = content.find('// MULTIPLEXER LOGIC')
if js_start != -1:
    js_start = content.rfind('  // ----------------------------------------------------', 0, js_start)
    # The end of the script block
    js_end = content.find('</script>', js_start)
    content = content[:js_start] + content[js_end:]

with open('06_circuiti.html', 'w') as f:
    f.write(content)

with open('01_fondamenti.html', 'r') as f:
    f_content = f.read()

f_content = f_content.replace('src="ciclo_cpu.png"', 'src="assets/ciclo_cpu.png"')

with open('01_fondamenti.html', 'w') as f:
    f.write(f_content)

print("Multiplexer replaced with image and assets updated!")
