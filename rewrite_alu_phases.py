import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

start_marker = '<!-- ══════════════ SEZIONE 25 ══════════════ -->'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("Errore: start_marker s25 non trovato")
    exit(1)

# Extract script block
script_idx = content.find('<script>', start_idx)
script_end_idx = content.find('</body>', script_idx)
original_script = content[script_idx:script_end_idx]

new_content = '''<!-- ══════════════ SEZIONE 25 ══════════════ -->
  <section class="section" id="s25">
    <div class="section-header">
      <div class="section-num">25</div>
      <h2>Fase 1: <span class="accent">L'ALU Base</span></h2>
    </div>

    <p class="lead">Iniziamo costruendo la versione primordiale dell'ALU: un circuito capace solo di eseguire le tre operazioni fondamentali su un singolo bit: AND, OR e l'Addizione matematica.</p>

    <p>Come abbiamo visto in precedenza, gli ingegneri piazzano semplicemente in parallelo una porta AND, una porta OR e il nostro Full Adder. Gli ingressi A e B entrano contemporaneamente in tutti e tre i componenti! A decidere quale risultato sopravvivrà ci pensa un <strong>Multiplexer a 3 ingressi</strong>, comandato dal filo <code>Operation</code>.</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: L'ALU "Neanderthal"</div>
      <img src="assets/alu/alu-1bit.png" alt="ALU 1 bit base" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:16px;font-weight:500;margin:32px 0 12px">Simulatore Interattivo: ALU Base</h3>
    <p style="font-size:14px;color:var(--text)">Prima di evolvere questo circuito, testalo tu stesso! Gioca con A, B e CarryIn e osserva come l'Operation fa "svegliare" il MUX per far passare l'uscita desiderata.</p>
    
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
      <h2>Fase 2: <span class="accent">Sottrazione e NOR</span></h2>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--text);margin:32px 0 16px">Il Problema delle Operazioni Inverse</h3>
    <p class="lead">L'ALU base è bloccata. Non sa calcolare il `NOR` logico e, soprattutto, non sa sottrarre! E gli ingegneri si rifiutano di costruire un hardware interamente nuovo (un "sottrattore") solo per fare A - B.</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--blue);margin:32px 0 16px">La Soluzione: I Deviatori in Ingresso</h3>
    <p>Sappiamo che per eseguire la sottrazione ci basta usare l'addizionatore già esistente applicando il <strong>Complemento a 2</strong>: capovolgere tutti i bit di B e aggiungere 1.</p>
    <p>Per poter "capovolgere" i bit a comando, all'ingresso dell'ALU vengono piazzati due <strong>Multiplexer a 2 ingressi</strong>. Ognuno funge da deviatore: riceve il segnale originale e quello passato in una porta <code>NOT</code>. Due fili di comando (<code>A-invert</code> e <code>B-negate</code>) scelgono se far entrare nell'ALU il segnale intatto o invertito.</p>

    <div class="card amber" style="margin-bottom:24px;">
      <div class="card-title">L'eleganza di B-negate</div>
      <p style="font-size:13px;margin:4px 0 0">Quando la CPU ordina una Sottrazione, accende il filo `B-negate`. Questo filo compie due miracoli simultanei: primo, inverte B passando per il NOT. Secondo, viaggia fino al primissimo <code>CarryIn</code> e lo accende forzatamente a 1, completando il calcolo matematico della sottrazione in un colpo solo!</p>
    </div>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: I deviatori A-invert e B-negate</div>
      <img src="assets/alu/alu-nor.png" alt="ALU con Invert e Negate" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>
  </section>

  <!-- ══════════════ SEZIONE 27 ══════════════ -->
  <section class="section" id="s27">
    <div class="section-header">
      <div class="section-num">27</div>
      <h2>Fase 3: <span class="accent">Il Problema SLT</span></h2>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--text);margin:32px 0 16px">Il Problema del "Minore di"</h3>
    <p class="lead">Vogliamo che l'hardware risponda all'istruzione <code>slt</code> (Set Less Than). Se $A < B$, deve rispondere 1 (ovvero <code>000...001</code>). Altrimenti 0. Ma l'ALU sa solo fare calcoli fisici!</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--green);margin:32px 0 16px">La Soluzione: Sdoppiare l'Hardware</h3>
    <p>L'unico modo che l'hardware ha per sapere se A è minore di B è lanciare una sottrazione cieca ($A - B$) e guardare se il risultato è negativo (se lo è, significa che A era più piccolo). Ma il "segno negativo" viene calcolato *soltanto* dall'ultima ALU, quella del bit 31. Dobbiamo quindi creare due versioni diverse della nostra ALU!</p>

    <div class="card-grid cols2" style="margin-bottom:32px;">
      <div class="card">
        <div class="card-title">Le Prime 31 ALU (Bit 0-30)</div>
        <p style="font-size:13px;margin:8px 0 16px;color:var(--text)">Al MUX finale si aggiunge il quarto canale: <strong>Less</strong>. Ma la cosa geniale è che nelle prime 31 ALU questo canale viene letteralmente saldato al vuoto (valore costante 0). Così, quando chiedi un <code>slt</code>, i primi 31 bit sputano all'istante uno zero!</p>
        <img src="assets/alu/alu-31bit.png" alt="ALU 31 bit" style="width:100%; border-radius:6px; border:1px solid var(--border);">
      </div>
      <div class="card">
        <div class="card-title">La 32esima ALU (Il Bit del Segno)</div>
        <p style="font-size:13px;margin:8px 0 16px;color:var(--text)">In cima, la 32esima fetta ha un "tubo di scappamento" speciale chiamato <strong>Set</strong>: ruba l'output direttamente dall'addizionatore, estraendo puro e crudo il bit del segno appena calcolato, prima ancora che arrivi al MUX.</p>
        <img src="assets/alu/alu-32bit.png" alt="ALU 32 bit" style="width:100%; border-radius:6px; border:1px solid var(--border);">
      </div>
    </div>

    <div class="callout blue" style="margin-bottom:24px;">
      <strong>La Cucitura Finale (Il teletrasporto da Set a Less)</strong><br>
      Ora la magia: si prende il bit estratto dal <strong>Set</strong> in cima (la 32esima ALU), lo si fa scivolare giù lungo tutta la scheda madre con un cavo lunghissimo, e lo si inietta nell'ingresso <strong>Less</strong> in fondo (la 1a ALU).<br>
      Risultato? 31 zeri generati dal vuoto + 1 bit del segno teleportato. Formato `000...001` perfetto!
    </div>
  </section>

  <!-- ══════════════ SEZIONE 28 ══════════════ -->
  <section class="section" id="s28">
    <div class="section-header">
      <div class="section-num">28</div>
      <h2>Fase 4: <span class="accent">Il Problema Overflow</span></h2>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--text);margin:32px 0 16px">Il Problema dello "Strabordamento"</h3>
    <p class="lead">Se sommiamo due numeri positivi titanici, il loro risultato potrebbe "bucare" la capacità dei 32 bit e invadere proprio il bit del segno. Il computer crederebbe di aver ottenuto un numero negativo! È l'<strong>Overflow</strong>.</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--red);margin:32px 0 16px">La Soluzione: Lo scudo XOR</h3>
    <p>Gli ingegneri hardware hanno scoperto un teorema affascinante: c'è Overflow <em>esclusivamente</em> quando il riporto che entra nell'ultimo bit (il <code>CarryIn</code> della 32esima ALU) è diverso dal riporto che ne esce (<code>CarryOut</code>).</p>
    <p>Come facciamo a lanciare un segnale "1" quando due fili sono diversi tra loro? Usando la gloriosa porta <strong>XOR</strong>!</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: L'Allarme Overflow sulla 32esima ALU</div>
      <img src="assets/alu/overflow.png" alt="XOR per Overflow" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>
    
    <p style="margin-top:24px">Come vedi nello schema, la 32esima ALU riceve il suo ultimo potenziamento definitivo: una porta XOR che confronta i due Carry e genera l'output di emergenza <code>Overflow</code>.</p>
  </section>

  <!-- ══════════════ SEZIONE 29 ══════════════ -->
  <section class="section" id="s29">
    <div class="section-header">
      <div class="section-num">29</div>
      <h2>Fase 5: <span class="accent">L'ALU Completa</span></h2>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--text);margin:32px 0 16px">Il Problema del Salto (BEQ)</h3>
    <p class="lead">C'è un ultimo pezzo del puzzle mancante. La CPU ha bisogno di sapere istantaneamente se il calcolo ha prodotto "Esattamente Zero" (fondamentale per capire se A = B nell'istruzione <code>beq</code>). Ma come lo sa l'hardware?</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--green);margin:32px 0 16px">La Soluzione: Il NOR Gigante</h3>
    <p>Tutti i 32 fili in uscita dalle ALU vengono catturati e fatti entrare in una titanica porta <strong>OR seguita da un NOT (NOR)</strong>. Se <em>anche solo uno</em> di quei 32 bit vale 1, l'OR scatta e il NOT lo annienta a 0. Solo quando esce una perfezione di 32 zeri continui, il NOR sputa fuori 1, accendendo il luminoso filo d'allarme <strong>Zero</strong>!</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface); margin-bottom: 32px;">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Il Traguardo: L'Architettura Definitiva (100% Completata)</div>
      <img src="assets/alu-completa.png" alt="ALU Completa" style="width:100%; max-width:800px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--purple);margin:40px 0 16px">La Centralina a 4 Bit</h3>
    <p>Tutte le 32 fette, i deviatori A-invert, B-negate, e il multiplexer finale, vengono manovrati in perfetta sincronia dall'Unità di Controllo. Quest'ultima invia un codice "a barre" di 4 fili:</p>
    
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
        <p style="font-size:13px;margin:4px 0 0">Attiva B-negate per sottrarre, ma fai uscire il risultato dal tubo LESS (11).</p>
      </div>
      <div class="card amber">
        <div class="card-title">NOR logico: 1100</div>
        <p style="font-size:13px;margin:4px 0 0">Inverti sia A che B (11) ed esegui AND (00). Magia di De Morgan!</p>
      </div>
    </div>

    <div class="callout green" style="margin-top:24px">
      <strong>Il Simbolo a "V"</strong><br>
      D'ora in poi, l'intero labirinto di MUX, XOR, AND, e il gigantesco cavo Set-Less spariranno dai diagrammi. Questa meraviglia dell'ingegneria diventerà un semplice simbolo a "V" contenente due ingressi a 32 bit, un cavo di Controllo, un Result, lo Zero e l'Overflow. Abbiamo letteralmente costruito un calcolatore da zero!
    </div>
  </section>

</main>
</div>
'''

content = content[:start_idx] + new_content + "\n" + original_script

# Riscriviamo la sidebar
def update_sidebar(html):
    start_sb = html.find('<a class="nav-item" href="06_circuiti.html#s25">')
    end_sb = html.find('</nav>')
    
    if start_sb != -1:
        new_sb = '''<a class="nav-item" href="06_circuiti.html#s25">
    <div class="nav-dot"></div> Fase 1: ALU Base
    <span class="nav-num">25</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s26">
    <div class="nav-dot"></div> Fase 2: NOR e SUB
    <span class="nav-num">26</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s27">
    <div class="nav-dot"></div> Fase 3: Il Problema SLT
    <span class="nav-num">27</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s28">
    <div class="nav-dot"></div> Fase 4: Overflow
    <span class="nav-num">28</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s29">
    <div class="nav-dot"></div> Fase 5: L'ALU Completa
    <span class="nav-num">29</span>
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

# Replace sections 25-28 and add 29 in index.html
# Need to find the block in index.html for Chapter 6.
# It currently has s24 up to s28.
idx_content = re.sub(
    r'\{ id: "s25", title: "L\'ALU a 1 bit", file: "06_circuiti.html" \},.*?\{ id: "s28", title: "L\'ALU a 32 bit Completa", file: "06_circuiti.html" \},',
    '''{ id: "s25", title: "Fase 1: ALU Base", file: "06_circuiti.html" },
      { id: "s26", title: "Fase 2: NOR e SUB", file: "06_circuiti.html" },
      { id: "s27", title: "Fase 3: Il Problema SLT", file: "06_circuiti.html" },
      { id: "s28", title: "Fase 4: Overflow", file: "06_circuiti.html" },
      { id: "s29", title: "Fase 5: L'ALU Completa", file: "06_circuiti.html" },''',
    idx_content, flags=re.DOTALL
)

with open('index.html', 'w') as f:
    f.write(idx_content)

print("Riscrittura evolutiva step-by-step completata!")
