with open('06_circuiti.html', 'r') as f:
    content = f.read()

start_marker = '<!-- ══════════════ SEZIONE 24 ══════════════ -->'
start_idx = content.find(start_marker)

new_content = '''<!-- ══════════════ SEZIONE 24 ══════════════ -->
  <section class="section" id="s24">
    <div class="section-header">
      <div class="section-num">24</div>
      <h2>Gli Addizionatori <span class="accent">e ALU 1-bit</span></h2>
    </div>

    <p class="lead">L'obiettivo primario della CPU è calcolare. Ma come si costruisce un circuito in grado di sommare numeri binari usando solo le porte logiche di base (AND, OR, XOR)?</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--blue);margin:32px 0 16px">L'Half Adder (Mezzo Addizionatore)</h3>
    <p>Se vogliamo sommare due bit singoli (es. 1 + 1), abbiamo due risultati possibili: la Somma (che vale 0) e il Riporto (Carry, che vale 1). Il circuito più semplice per farlo è l'Half Adder, che usa esattamente due porte logiche in parallelo:</p>
    
    <div class="card" style="margin-bottom:24px">
      <ul style="font-size:14px;line-height:1.6;color:var(--text);margin:0;padding-left:20px">
        <li><strong>Porta XOR per la Somma:</strong> Ricordi? L'XOR vale 1 solo se gli ingressi sono diversi. Infatti: 0+0=0, 0+1=1, 1+0=1. E 1+1? Fa 0 col riporto di 1! L'XOR per 1 e 1 dà giustamente 0.</li>
        <li><strong>Porta AND per il Riporto (CarryOut):</strong> L'AND vale 1 solo se tutti gli ingressi sono 1. Infatti il riporto scatta a 1 <em>solo</em> quando sommiamo 1 e 1.</li>
      </ul>
    </div>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: Half Adder</div>
      <img src="assets/half-adder.png" alt="Half Adder" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--green);margin:40px 0 16px">Il Full Adder (Addizionatore Completo)</h3>
    <p>L'Half Adder va bene per il primo bit, ma per sommare i bit successivi di un numero lungo ci serve un circuito in grado di accettare un terzo ingresso: il <strong>CarryIn</strong> (il riporto generato dalla colonna precedente).</p>
    <p>Il <strong>Full Adder</strong> si costruisce mettendo in cascata due Half Adder e una porta OR. È in grado di sommare tre bit (A, B e CarryIn) e sputare fuori il Risultato e il CarryOut.</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: Full Adder</div>
      <img src="assets/full-adder.png" alt="Full Adder" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>
  </section>

  <!-- ══════════════ SEZIONE 25 ══════════════ -->
  <section class="section" id="s25">
    <div class="section-header">
      <div class="section-num">25</div>
      <h2>L'ALU <span class="accent">a 1 bit</span></h2>
    </div>

    <p class="lead">L'ALU non sa solo fare addizioni, ma anche operazioni logiche. Inoltre, per la Sottrazione, deve poter invertire i segnali. Vediamo come gli ingegneri hanno costruito la perfetta "fetta" da 1 bit.</p>

    <h3 style="font-size:18px;font-weight:600;color:var(--text);margin:32px 0 16px">Il trucco dei deviatori: A-invert e B-negate</h3>
    <p>Per poter eseguire le sottrazioni (grazie al complemento a 2) e operazioni logiche come il NOR, la CPU deve poter invertire i bit in ingresso. Come fa?</p>
    <p>All'ingresso di A e di B, gli ingegneri hanno piazzato due "deviatori ferroviari": due piccoli <strong>Multiplexer a 2 ingressi</strong>. Ognuno di essi riceve il segnale originale e il segnale passato attraverso una porta NOT. Un filo di controllo (chiamato <strong>A-invert</strong> per A, e <strong>B-negate</strong> per B) decide se far passare all'ALU il segnale normale oppure quello ribaltato!</p>
    <p><em>Nota fondamentale:</em> Quando B-negate viene acceso per fare una sottrazione, non si limita a invertire B: accende anche il <code>CarryIn</code> iniziale a 1, completando così il perfetto trucco matematico del complemento a 2 (inverti i bit e somma 1).</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--purple);margin:40px 0 16px">L'ALU per i primi 31 bit (da 0 a 30)</h3>
    <p>Ecco l'architettura base usata per i bit meno significativi del numero. Si notano chiaramente le porte AND, OR e l'Addizionatore messi in parallelo. Tutti i risultati finiscono in un grande Multiplexer finale a 4 vie, pilotato dal cavo `Operation`.</p>
    <p>In basso compare anche l'ingresso <strong>Less</strong>, che per ora entra nel MUX ma non sembra fare nulla (vedremo tra poco a cosa serve nell'istruzione slt).</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: ALU a 1 bit (Primi 31 bit)</div>
      <img src="assets/alu-31bit.png" alt="ALU per i primi 31 bit" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--red);margin:40px 0 16px">L'ALU per il 32esimo bit (Il Bit del Segno)</h3>
    <p>La primissima fetta a sinistra della CPU (l'ALU numero 31, che gestisce il 32esimo bit del numero, ovvero il segno) non è uguale alle altre. Ha due potenziamenti fisici cruciali:</p>
    <ol style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>Il cavo Set:</strong> Viene letteralmente saldato un nuovo filo all'uscita dell'addizionatore. Questo filo "ruba" il risultato della somma matematica prima che arrivi al MUX.</li>
      <li><strong>Il rilevatore di Overflow:</strong> C'è una speciale porta XOR collegata al <code>CarryIn</code> e al <code>CarryOut</code> di questo specifico bit. Se sono diversi, la porta sputa '1' sul nuovo cavo <strong>Overflow</strong>, indicando un errore catastrofico nel calcolo.</li>
    </ol>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Analisi Visiva: ALU del 32esimo bit (Bit del Segno)</div>
      <img src="assets/alu-32bit.png" alt="ALU del 32esimo bit" style="width:100%; max-width:600px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <h3 style="font-size:16px;font-weight:500;margin:32px 0 12px">Simulatore Interattivo: ALU a 1-bit</h3>
    <p style="font-size:14px;color:var(--text)">Gioca con gli ingressi (A, B, CarryIn) e osserva come l'Operation fa deviare i risultati matematici verso l'uscita!</p>
    
    <div class="widget-container">
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
      <h2>La Magia di SLT <span class="accent">a 32 bit</span></h2>
    </div>

    <p class="lead">Progettare un'enorme ALU nativa a 32 bit sarebbe folle. Gli ingegneri prendono l'ALU a 1 bit e la "fotocopiano" 32 volte sul silicio, collegando il <code>CarryOut</code> di una nel <code>CarryIn</code> della successiva. Ma come si implementa l'istruzione slt (Set Less Than)?</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--blue);margin:32px 0 16px">Set Less Than: La grande bugia</h3>
    <p>L'istruzione <code>slt</code> risponde a una domanda: "A è minore di B?". Se Sì, il risultato finale a 32 bit deve essere esattamente 1 (<code>000...0001</code>). Se No, esattamente 0 (<code>000...0000</code>).</p>
    <p>Ecco come la CPU "inganna" i circuiti per ottenere questo formato magico in un solo ciclo di clock:</p>
    
    <ol style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:32px">
      <li><strong>Il trucco di base:</strong> La CPU lancia una sottrazione ($A - B$). Se il risultato matematico è negativo, significa che A era minore. Ma dov'è l'informazione del segno? Esclusivamente nel 31esimo bit calcolato dall'ultimissima ALU in cima!</li>
      <li><strong>La soppressione:</strong> La CPU manda a tutte le 32 ALU il comando `Operation = 11` (fai passare l'ingresso Less). Dato che il pin Less delle prime 31 ALU è saldato fisicamente a Terra (il vuoto assoluto), le prime 31 ALU buttano fuori uno <code>0</code> spaccato. Abbiamo appena formato i primi 31 zeri del risultato!</li>
      <li><strong>Il teletrasporto (La cucitura Set ➔ Less):</strong> Mentre le altre ALU stanno sputando zeri, l'addizionatore dell'ultima ALU (la ALU del 32esimo bit) finisce di calcolare il segno. Questo bit di segno scivola fuori dal nuovo tubicino <strong>Set</strong>. Un lunghissimo filo di rame percorre tutta la scheda madre, prende questo bit dal Set in cima e lo infila brutalmente nell'ingresso <strong>Less</strong> della primissima ALU in basso (la ALU 0).</li>
      <li><strong>Il miracolo finale:</strong> Il MUX della ALU 0, che era in attesa sul canale Less, vede arrivare il bit del segno e lo lascia passare come suo risultato. Risultato complessivo: 31 zeri seguiti dall'unico 1 (o 0) del segno. <code>00000000000000000000000000000001</code>. Boom.</li>
    </ol>
  </section>

  <!-- ══════════════ SEZIONE 27 ══════════════ -->
  <section class="section" id="s27">
    <div class="section-header">
      <div class="section-num">27</div>
      <h2>La Centralina <span class="accent">e L'ALU Completa</span></h2>
    </div>

    <p class="lead">Per pilotare questo leviatano da 32 bit, l'Unità di Controllo usa un codice a 4 bit come "codice a barre" per dire ai vari MUX interni cosa devono fare.</p>

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
    
    <h3 style="font-size:20px;font-weight:600;color:var(--green);margin:40px 0 16px">L'Allarme "Zero" e l'ALU Completa</h3>
    <p>L'istruzione <code>beq</code> (Branch if Equal) salta se A e B sono uguali. L'hardware esegue A - B: se il risultato è zero, erano identici!
    Per intercettarlo in una frazione di secondo, i 32 fili del risultato vengono infilati in una gigantesca porta <strong>OR seguita da un NOT (NOR)</strong>. Se tutti i 32 bit sono 0, il NOR sputa fuori un '1', accendendo il filo d'allarme <strong>Zero</strong>!</p>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface);">
      <div class="widget-title" style="color:var(--text); font-size:16px;">L'ALU a 32 bit completa (1/2)</div>
      <img src="assets/alu-completa1.png" alt="ALU completa 1" style="width:100%; max-width:800px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
    </div>

    <div class="widget-container" style="position:relative;padding-left:10px; background:var(--surface); margin-top: 24px;">
      <div class="widget-title" style="color:var(--text); font-size:16px;">Il simbolo architetturale dell'ALU (2/2)</div>
      <img src="assets/alu-completa2.png" alt="ALU completa 2" style="width:100%; max-width:800px; border-radius:8px; border:1px solid var(--border); margin-top:10px;">
      
      <div class="callout green" style="margin-top:24px">
        <strong>La Scatola Nera</strong><br>
        Come vedi nell'immagine qui sopra, da questo momento in poi negli schemi della CPU smetteremo di disegnare MUX, XOR e cavi interni. Disegneremo solo questo simbolo a forma di "V": il Sacro Graal del calcolo binario, completo di pin per Operation, Zero, Result e Overflow.
      </div>
    </div>

  </section>

</main>
</div>

<script>
  // Logica per il Widget Interattivo dell'ALU a 1 bit
  const btnA = document.getElementById('btnA');
  const btnB = document.getElementById('btnB');
  const btnCin = document.getElementById('btnCin');
  const opSelect = document.getElementById('opSelect');
  const resOut = document.getElementById('resOut');
  const coutOut = document.getElementById('coutOut');

  let valA = 0;
  let valB = 0;
  let valCin = 0;

  function updateLogic() {
    if (!btnA) return; // Prevent errors se il simulatore manca
    const op = opSelect.value;
    let res = 0;
    let cout = 0;

    if (op === 'and') {
      res = valA & valB;
      cout = 0;
    } else if (op === 'or') {
      res = valA | valB;
      cout = 0;
    } else if (op === 'add') {
      const sum = valA + valB + valCin;
      res = sum % 2;
      cout = sum >= 2 ? 1 : 0;
    }

    resOut.textContent = res;
    coutOut.textContent = cout;

    if(res === 1) resOut.classList.add('active');
    else resOut.classList.remove('active');

    if(cout === 1) coutOut.classList.add('active');
    else coutOut.classList.remove('active');
  }

  function toggleBtn(btn, valSetter) {
    let current = parseInt(btn.textContent);
    let next = current === 0 ? 1 : 0;
    btn.textContent = next;
    if(next === 1) btn.classList.add('active');
    else btn.classList.remove('active');
    valSetter(next);
    updateLogic();
  }

  if (btnA) btnA.addEventListener('click', () => toggleBtn(btnA, v => valA = v));
  if (btnB) btnB.addEventListener('click', () => toggleBtn(btnB, v => valB = v));
  if (btnCin) btnCin.addEventListener('click', () => toggleBtn(btnCin, v => valCin = v));
  if (opSelect) opSelect.addEventListener('change', updateLogic);

  updateLogic();

</script>

<script src="shared.js"></script>
</body>
</html>
'''

content = content[:start_idx] + new_content

with open('06_circuiti.html', 'w') as f:
    f.write(content)

print("Immagini inserite e spiegazioni perfezionate!")
