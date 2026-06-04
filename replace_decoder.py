with open('06_circuiti.html', 'r') as f:
    content = f.read()

# 1. Replace Decoder HTML section
import re

# Find the start of the Decoder widget
start_str = '<div class="widget-title">Simulatore Interattivo: Decoder</div>'
start_idx = content.find(start_str)

# Find the end of the decoder SVG
end_str = '</svg>'
end_idx = content.find(end_str, start_idx) + len(end_str)

replacement_html = '''<div class="widget-title">Schema: Decoder 3 a 8</div>
      <p style="font-size:12px;color:var(--muted);margin-bottom:16px">L'indirizzo a 3 bit entra da A, B e C. Passando attraverso le porte NOT e AND, la corrente sbloccherà <strong>esattamente una sola linea</strong> (da D0 a D7) in uscita.</p>
      
      <img src="decoder.png" alt="Schema Decoder 3 a 8" style="width:100%; border-radius:8px; border:1px solid var(--border);">'''

content = content[:start_idx] + replacement_html + content[end_idx:]

# 2. Remove Decoder JS logic
js_start = content.find('// DECODER LOGIC')
js_end = content.find('// MULTIPLEXER LOGIC')

if js_start != -1 and js_end != -1:
    # Go back to the previous line of js_start to remove the comments cleanly
    js_start = content.rfind('  // ----------------------------------------------------', 0, js_start)
    js_end_exact = content.rfind('  // ----------------------------------------------------', 0, js_end)
    content = content[:js_start] + content[js_end_exact:]

with open('06_circuiti.html', 'w') as f:
    f.write(content)

print("Decoder replaced with image!")
