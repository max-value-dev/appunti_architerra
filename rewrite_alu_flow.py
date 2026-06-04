import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

start_marker = '<!-- ══════════════ SEZIONE 25 ══════════════ -->'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("Errore: start_marker s25 non trovato")
    exit(1)

# Extract the script block at the end so we can append it afterwards
script_marker = '<script>'
script_idx = content.find(script_marker, start_idx)
script_end_idx = content.find('</body>', script_idx)
original_script = content[script_idx:script_end_idx]

# Remove the interactive simulator from section 24 if it's there
s24_marker = '<!-- ══════════════ SEZIONE 24 ══════════════ -->'
s24_idx = content.find(s24_marker)
sim_start = content.find('<h3 style="font-size:16px;font-weight:500;margin:32px 0 12px">Simulatore Interattivo: ALU a 1-bit</h3>', s24_idx, start_idx)

if sim_start != -1:
    sim_end = content.find('</section>', sim_start)
    content = content[:sim_start] + content[sim_end:]
    # Recalculate start_idx since string length changed
    start_idx = content.find(start_marker)


new_content = '''<!-- ══════════════ SEZIONE 25 ══════════════ -->
  <section class="section" id="s25">
    <div class="section-header">
      <div class="section-num">25</div>
      <h2>L'ALU a 1 bit <span class="accent">(La Base)</span></h2>
    </div>

    <p class="lead">Iniziamo costruendo la versione primordiale dell'ALU: un circuito capace solo di eseguire AND, OR e l'Addizione su un singolo bit.</p>

    <p>Come abbiamo visto, per fare questo gli ingegneri piazzano in parallelo una porta AND, una porta OR e un Full Adder. Gli ingressi A e B entrano in tutti e tre i componenti contemporaneamente! Sarà poi un <strong>Multiplexer a 3 ingressi</strong>, controllato dal filo `Operation`, a decidere quale dei tre risultati far uscire.</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: L'ALU a 1-bit base</div>
      <img src="assets/alu-1bit.png" alt="ALU 1 bit base" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:16px;font-weight:500;margin:32px 0 12px">Simulatore Interattivo: ALU a 1-bit Base</h3>
    <p style="font-size:14px;color:var(--text)">Gioca con gli ingressi (A, B, CarryIn) e osserva come l'Operation fa deviare i risultati matematici verso l'uscita!</p>
    
    <div class="widget-container" style="margin-bottom:32px">
      <div class="alu-grid">
        <div class="alu-inputs">
          <div class="bit-row"><span class="bit-label">Input A</span><button id="btnA" class="bit-btn">0</button></div>
          <div class="bit-row"><span class="bit-label">Input B</span><button id="btnB" class="bit-btn">0</button></div>
          <div class="bit-row"><span class="bit-label" style="opacity:0.7">CarryIn</span><button id="btnCin" class="bit-btn" style="border-style:dashed">0</button></div>
        </div>
        
        <div class="alu-core">
          <select id="opSelect" class="op-select">
            <option value="and">AND (00)</option>
            <option value="or">OR (01)</option>
            <option value="add" selected>SUM (10)</option>
          </select>
        </div>
        
        <div class="alu-outputs">
          <div class="bit-row"><span class="bit-out" id="resOut">0</span><span class="bit-label">Result</span></div>
          <div class="bit-row" style="margin-top:28px"><span class="bit-out" id="coutOut" style="border-style:dashed">0</span><span class="bit-label" style="opacity:0.7">CarryOut</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 26 ══════════════ -->
  <section class="section" id="s26">
    <div class="section-header">
      <div class="section-num">26</div>
      <h2>Sottrazione <span class="accent">e NOR</span></h2>
    </div>

    <p class="lead">Il circuito precedente è fantastico, ma ha un grave problema: non sa fare le sottrazioni né l'operazione NOR. Come risolviamo?</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--blue);margin:32px 0 16px">Il trucco dei deviatori in ingresso</h3>
    <p>Per poter eseguire le sottrazioni (usando la regola matematica del <em>Complemento a 2</em>) la CPU deve poter invertire i bit in ingresso. </p>
    <p>All'ingresso di A e di B, gli ingegneri piazzano due "deviatori ferroviari": dei piccoli <strong>Multiplexer a 2 ingressi</strong>. Ognuno di essi riceve il segnale originale e il segnale passato attraverso una porta NOT. Due nuovi fili di controllo (chiamati <strong>A-invert</strong> e <strong>B-negate</strong>) decidono se far passare all'interno dell'ALU il segnale intatto oppure quello ribaltato!</p>

    <div class="card amber" style="margin-bottom:24px;">
      <div class="card-title">Il Comando B-negate fa il miracolo</div>
      <p style="font-size:13px;margin:4px 0 0">Quando la CPU vuole fare una Sottrazione ($A - B$), accende il filo `B-negate`. Questo filo non solo inverte la B, ma viaggia per accendere a 1 anche il <code>CarryIn</code> iniziale dell'addizionatore, completando in un millisecondo il trucco del complemento a 2 (inverti i bit + somma 1).</p>
    </div>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: ALU con A-invert e B-negate</div>
      <img src="assets/alu-nor.png" alt="ALU con Invert" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>
  </section>

  <!-- ══════════════ SEZIONE 27 ══════════════ -->
  <section class="section" id="s27">
    <div class="section-header">
      <div class="section-num">27</div>
      <h2>Il problema <span class="accent">Set Less Than (SLT)</span></h2>
    </div>

    <p class="lead">Vogliamo istruire la CPU a rispondere a una domanda logica: "A è minore di B?". Se è vero, il risultato deve essere 1. Se è falso, 0. Ma l'ALU fa solo matematica e operazioni bit a bit!</p>

    <p>Per risolvere questo enigma, l'ALU deve letteralmente "sdoppiarsi" in due tipologie fisiche diverse: una standard per i primi 31 bit, e una speciale per l'ultimo bit.</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--green);margin:32px 0 16px">L'ALU per i primi 31 bit (da 0 a 30)</h3>
    <p>Per supportare l'istruzione <code>slt</code>, al grande Multiplexer finale viene aggiunta una quarta via: il canale <strong>Less</strong> (Operation = 11).</p>
    <p>La cosa sconvolgente è che <strong>nelle prime 31 ALU, questo ingresso Less viene letteralmente saldato al vuoto (la Terra, cioè il valore costante 0).</strong> In questo modo, quando esegui <code>slt</code>, i primi 31 bit del risultato formano immediatamente una sequenza di zeri perfetti (<code>000...</code>).</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: ALU Standard (Primi 31 bit)</div>
      <img src="assets/alu-31bit.png" alt="ALU per i primi 31 bit" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--red);margin:40px 0 16px">L'ALU per il 32esimo bit (Il Bit del Segno)</h3>
    <p>La CPU scopre se $A < B$ eseguendo di nascosto una sottrazione: se $A - B$ è negativo, allora A era minore! Ma l'informazione "è negativo" si trova <em>solo</em> nel risultato del 32esimo addizionatore (il bit del segno).</p>
    <p>Per questo motivo, la 32esima ALU ha una modifica fisica strutturale: viene saldato un "tubicino di scolo" direttamente all'uscita dell'addizionatore matematico. Questo nuovo filo viene chiamato <strong>Set</strong>.</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: L'ALU del 32esimo bit</div>
      <img src="assets/alu-32bit.png" alt="ALU del 32esimo bit" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <div class="callout blue" style="margin-top:24px">
      <strong>La Cucitura Finale (Il teletrasporto da Set a Less)</strong><br>
      Un lunghissimo filo di rame percorre tutta la scheda madre: preleva l'1 o lo 0 uscito dal pin <strong>Set</strong> dell'ALU in cima (la 31esima), e lo infila brutalmente nell'ingresso <strong>Less</strong> della primissima ALU in basso (la ALU 0).<br>
      In questo modo, il risultato intero di un <code>slt</code> sarà composto da trentuno zeri (generati dalle ALU 1-31 saldate a terra) seguiti dal bit del segno (posizionato magicamente nella ALU 0).
    </div>
  </section>

  <!-- ══════════════ SEZIONE 28 ══════════════ -->
  <section class="section" id="s28">
    <div class="section-header">
      <div class="section-num">28</div>
      <h2>L'ALU a 32 bit <span class="accent">Completa</span></h2>
    </div>

    <p class="lead">Ora che abbiamo progettato i due blocchi base, assembliamo il "leviatano" incollandoli 32 volte sul silicio e collegando i `CarryOut` in `CarryIn`.</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Assemblaggio Base della Catena</div>
      <img src="assets/alu-completa1.png" alt="ALU completa 1" style="width:100%; max-width:800px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--text);margin:40px 0 16px">I Problemi Finali: Sicurezza e Salti Condizionati</h3>
    <p>La catena appena assemblata funziona, ma non ci avverte se un calcolo è sballato, né è in grado di avvisare la CPU se due numeri sono perfettamente uguali (cosa fondamentale per l'istruzione <code>beq</code>, Branch if Equal).</p>
    
    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:24px">
      <li><strong>Overflow (Errore di strabordamento):</strong> Quando si sommano numeri enormi, il risultato potrebbe diventare negativo per errore. L'hardware lo rileva inserendo una semplice <strong>porta XOR</strong> tra il `CarryIn` e il `CarryOut` della 32esima ALU. Se differiscono, sputa '1' accendendo l'allarme di Overflow!</li>
      <li><strong>Zero (Per il Branch if Equal):</strong> Per scoprire se $A = B$, la CPU lancia $A - B$. Se esce $000...000$, i due numeri erano uguali! Per capire istantaneamente se tutti i 32 bit sono nulli, vengono tutti infilati in un gigantesco <strong>NOR a 32 vie</strong> (un OR enorme seguito da un NOT). Se anche solo un bit è a 1, l'OR scatta e il NOT lo annulla. Solo se tutti i 32 bit sono a zero, il NOR restituisce '1', accendendo la bandierina <code>Zero</code>.</li>
    </ul>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">L'Architettura Finale Definitiva</div>
      <img src="assets/alu-completa2.png" alt="ALU completa 2" style="width:100%; max-width:800px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--purple);margin:40px 0 16px">La Centralina a 4 Bit</h3>
    <p>Per pilotare questo leviatano da 32 bit, l'Unità di Controllo manda 4 fili specifici che fungono da "codice a barre":</p>
    
    <div class="card-grid cols2" style="margin-bottom: 32px;">
      <div class="card purple">
        <div class="card-title">Addizione: 0010</div>
        <p style="font-size:13px;margin:4px 0 0">Nessuna inversione (00), uscita SUM (10).</p>
      </div>
      <div class="card red">
        <div class="card-title">Sottrazione: 0110</div>
        <p style="font-size:13px;margin:4px 0 0">Attiva B-negate (01), uscita SUM (10).</p>
      </div>
      <div class="card blue">
        <div class="card-title">Set Less Than: 0111</div>
        <p style="font-size:13px;margin:4px 0 0">Attiva B-negate per forzare la sottrazione, ma fai uscire il risultato dal tubo LESS (11).</p>
      </div>
      <div class="card amber">
        <div class="card-title">NOR logico: 1100</div>
        <p style="font-size:13px;margin:4px 0 0">Inverti sia A che B (11), ed esegui AND (00). Per la legge di De Morgan, NOT(A) AND NOT(B) crea un perfetto NOR!</p>
      </div>
    </div>

    <div class="callout green" style="margin-top:24px">
      <strong>La Scatola Nera (Il Simbolo a V)</strong><br>
      Come vedi nell'immagine qui sopra, da questo momento in poi negli schemi della CPU smetteremo di disegnare MUX, XOR e cavi interni. Disegneremo solo quel glorioso simbolo a forma di "V", il Sacro Graal del calcolo binario, completo dei pin per `ALU Operation`, `Zero`, `Result` e `Overflow`.
    </div>
  </section>

</main>
</div>
'''

content = content[:start_idx] + new_content + "\n" + original_script

# Update sidebar
def update_sidebar(html):
    # Dobbiamo far combaciare:
    # 24: Gli Addizionatori
    # 25: L'ALU a 1 bit
    # 26: Sottrazione e NOR
    # 27: Il problema SLT
    # 28: L'ALU a 32 bit Completa
    
    # Rimuoviamo vecchi item 25, 26, 27 e li riscriviamo
    start_sb = html.find('<a class="nav-item" href="06_circuiti.html#s25">')
    end_sb = html.find('</nav>')
    
    if start_sb != -1:
        new_sb = '''<a class="nav-item" href="06_circuiti.html#s25">
    <div class="nav-dot"></div> L'ALU a 1 bit
    <span class="nav-num">25</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s26">
    <div class="nav-dot"></div> Sottrazione e NOR
    <span class="nav-num">26</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s27">
    <div class="nav-dot"></div> Il problema SLT
    <span class="nav-num">27</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s28">
    <div class="nav-dot"></div> ALU a 32 bit Completa
    <span class="nav-num">28</span>
  </a>
'''
        html = html[:start_sb] + new_sb + html[end_sb:]
    return html

content = update_sidebar(content)

with open('06_circuiti.html', 'w') as f:
    f.write(content)

# Update index.html arrays
with open('index.html', 'r') as f:
    idx_content = f.read()

# We need to replace the items in the SECTIONS array for Chapter 6
# From:
# { id: "s24", title: "Gli Addizionatori", file: "06_circuiti.html" },
# { id: "s25", title: "ALU a 32 bit e Sottrazione", file: "06_circuiti.html" },
# { id: "s26", title: "Condizioni Avanzate", file: "06_circuiti.html" },
# { id: "s27", title: "La Centralina a 4 bit", file: "06_circuiti.html" },
# To:
# { id: "s24", title: "Gli Addizionatori", file: "06_circuiti.html" },
# { id: "s25", title: "L'ALU a 1 bit", file: "06_circuiti.html" },
# { id: "s26", title: "Sottrazione e NOR", file: "06_circuiti.html" },
# { id: "s27", title: "Il problema SLT", file: "06_circuiti.html" },
# { id: "s28", title: "L'ALU a 32 bit Completa", file: "06_circuiti.html" },

idx_content = re.sub(
    r'\{ id: "s24", title: "Gli Addizionatori", file: "06_circuiti.html" \},.*?\{ id: "s27", title: "La Centralina a 4 bit", file: "06_circuiti.html" \},',
    '''{ id: "s24", title: "Gli Addizionatori", file: "06_circuiti.html" },
      { id: "s25", title: "L'ALU a 1 bit", file: "06_circuiti.html" },
      { id: "s26", title: "Sottrazione e NOR", file: "06_circuiti.html" },
      { id: "s27", title: "Il problema SLT", file: "06_circuiti.html" },
      { id: "s28", title: "L'ALU a 32 bit Completa", file: "06_circuiti.html" },''',
    idx_content, flags=re.DOTALL
)

with open('index.html', 'w') as f:
    f.write(idx_content)

print("Riscrittura sequenziale completata!")
