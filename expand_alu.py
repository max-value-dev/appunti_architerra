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

    <div style="margin: 24px 0; padding: 40px; border: 2px dashed var(--blue); border-radius: 8px; text-align: center; background: rgba(59,130,246,0.05);">
      <p style="color: var(--blue); font-weight: 600; font-size: 16px;">[ Placeholder Screenshot: L'Half Adder ]</p>
      <p style="font-size: 13px; color: var(--muted); margin-top: 8px;">(Mostra il circuito con XOR e AND in parallelo)</p>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--green);margin:40px 0 16px">Il Full Adder (Addizionatore Completo)</h3>
    <p>L'Half Adder va bene per il primo bit, ma per sommare i bit successivi di un numero lungo ci serve un circuito in grado di accettare un terzo ingresso: il <strong>CarryIn</strong> (il riporto generato dalla colonna precedente).</p>
    <p>Il <strong>Full Adder</strong> si costruisce mettendo in cascata due Half Adder e una porta OR. È in grado di sommare tre bit (A, B e CarryIn) e sputare fuori il Risultato e il CarryOut.</p>

    <div style="margin: 24px 0; padding: 40px; border: 2px dashed var(--green); border-radius: 8px; text-align: center; background: rgba(34,197,94,0.05);">
      <p style="color: var(--green); font-weight: 600; font-size: 16px;">[ Placeholder Screenshot: Il Full Adder ]</p>
      <p style="font-size: 13px; color: var(--muted); margin-top: 8px;">(Mostra i due Half Adder e la porta OR finale)</p>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--purple);margin:40px 0 16px">Costruire l'ALU a 1 bit</h3>
    <p>L'ALU non sa solo fare addizioni, ma anche operazioni logiche come AND e OR. Per fare questo, l'ingegnere piazza in parallelo una porta AND, una porta OR e il Full Adder appena creato.</p>
    <p>Gli ingressi A e B entrano in tutti e tre i componenti contemporaneamente! Sarà poi un <strong>Multiplexer a 4 ingressi</strong>, controllato dal filo `Operation`, a decidere quale dei tre risultati far uscire verso il computer.</p>

    <div style="margin: 24px 0; padding: 40px; border: 2px dashed var(--purple); border-radius: 8px; text-align: center; background: rgba(168,85,247,0.05);">
      <p style="color: var(--purple); font-weight: 600; font-size: 16px;">[ Placeholder Screenshot: L'ALU a 1-bit ]</p>
      <p style="font-size: 13px; color: var(--muted); margin-top: 8px;">(Mostra le porte logiche parallele e il MUX controllato da Operation)</p>
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

  <!-- ══════════════ SEZIONE 25 ══════════════ -->
  <section class="section" id="s25">
    <div class="section-header">
      <div class="section-num">25</div>
      <h2>ALU a 32 bit <span class="accent">e Sottrazione</span></h2>
    </div>

    <p class="lead">Progettare un'enorme ALU nativa a 32 bit sarebbe folle. Gli ingegneri prendono l'ALU a 1 bit appena costruita e la "fotocopiano" 32 volte sul silicio, collegandole in catena.</p>

    <div class="callout blue" style="margin-bottom:24px">
      <strong>La Catena del Riporto (CarryOut ➔ CarryIn)</strong><br>
      L'ALU a 32 bit si costruisce collegando il filo <code>CarryOut</code> della prima ALU direttamente nell'ingresso <code>CarryIn</code> della seconda ALU, e così via come un nastro trasportatore! Ogni ALU gestisce un singolo bit del grande numero.
    </div>

    <div style="margin: 24px 0; padding: 40px; border: 2px dashed var(--amber); border-radius: 8px; text-align: center; background: rgba(245,158,11,0.05);">
      <p style="color: var(--amber); font-weight: 600; font-size: 16px;">[ Placeholder Screenshot: La catena delle 32 ALU ]</p>
      <p style="font-size: 13px; color: var(--muted); margin-top: 8px;">(Mostra i blocchi ALU 0 ... ALU 31 collegati dal Carry)</p>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--text);margin:40px 0 16px">La Sottrazione (B-negate)</h3>
    <p>Come facciamo A - B se abbiamo solo un circuito per sommare? Usiamo il <strong>Complemento a Due</strong> (capovolgere i bit e aggiungere 1).</p>
    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>Aggiungere una porta NOT per l'ingresso B:</strong> Un MUX interno sceglie se mandare ad A il filo di B normale, oppure B negato.</li>
      <li><strong>Il trucco del "+1":</strong> L'ingegnere accende forzatamente il <code>CarryIn</code> iniziale della primissima ALU 0, portandolo a 1.</li>
    </ul>

    <div class="card amber">
      <div class="card-title">Il Comando B-negate</div>
      <p style="font-size:13px;margin:4px 0 0">Dato che queste due operazioni vanno sempre fatte insieme per sottrarre, la CPU le unisce in un unico filo di comando chiamato <strong>B-negate</strong>. Quando B-negate è acceso, il MUX inverte B e il CarryIn iniziale viene impostato a 1. La Sottrazione è servita senza aver costruito alcun circuito "sottrattore"!</p>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 26 ══════════════ -->
  <section class="section" id="s26">
    <div class="section-header">
      <div class="section-num">26</div>
      <h2>Condizioni Avanzate <span class="accent">(SLT e Overflow)</span></h2>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--blue);margin:32px 0 16px">Set Less Than (La genialità del cavo Set-Less)</h3>
    <p>L'istruzione <code>slt</code> risponde a una domanda: "A è minore di B?". Se Sì, il risultato a 32 bit deve essere 1 (<code>00...01</code>). Se No, 0 (<code>00...00</code>).</p>
    <p>Per scoprire se A è minore di B, l'ALU lancia una sottrazione. Se il risultato è negativo, A era minore. L'informazione "il numero è negativo" è contenuta solo nel <strong>bit del segno (il 31esimo bit)</strong>, calcolato dall'ultimissima ALU (ALU 31).</p>
    
    <div style="margin: 24px 0; padding: 40px; border: 2px dashed var(--blue); border-radius: 8px; text-align: center; background: rgba(59,130,246,0.05);">
      <p style="color: var(--blue); font-weight: 600; font-size: 16px;">[ Placeholder Screenshot: La cucitura Set ➔ Less ]</p>
      <p style="font-size: 13px; color: var(--muted); margin-top: 8px;">(Mostra il cavo che parte dalla ALU 31 e scende nella ALU 0)</p>
    </div>
    
    <ol style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:32px">
      <li>La CPU forza tutte le ALU da 1 a 31 a ignorare la somma e buttare fuori uno 0 fisso sul canale Result.</li>
      <li>L'ALU 31 esegue la matematica. Scopre che il risultato è negativo e spara questo '1' su un tubicino di scarico speciale detto <strong>Set</strong>.</li>
      <li>Un cavo fisico letteralmente "teletrasporta" questo '1' lungo tutta la scheda per infilarlo nell'ingresso <strong>Less</strong> della primissima ALU (ALU 0).</li>
      <li>Il MUX dell'ALU 0 fa passare questo '1' nel suo Risultato. Ecco apparire perfettamente <code>000...01</code>!</li>
    </ol>

    <h3 style="font-size:20px;font-weight:600;color:var(--red);margin:40px 0 16px">Il problema dell'Overflow</h3>
    <p>Quando sommi due numeri positivi enormi e strabordi lo spazio di 32 bit, il risultato impazzisce diventando negativo. È un <strong>Overflow</strong>.
    Gli ingegneri hanno scoperto che questo accade <em>solo e soltanto</em> se il CarryIn del 31esimo bit è diverso dal CarryOut del 31esimo bit!</p>
    
    <div style="margin: 24px 0; padding: 40px; border: 2px dashed var(--red); border-radius: 8px; text-align: center; background: rgba(239,68,68,0.05);">
      <p style="color: var(--red); font-weight: 600; font-size: 16px;">[ Placeholder Screenshot: La porta XOR per l'Overflow ]</p>
      <p style="font-size: 13px; color: var(--muted); margin-top: 8px;">(Mostra l'XOR applicato ai riporti della ALU 31)</p>
    </div>

    <p>Aggiungendo una semplice porta <strong>XOR</strong> che confronta i due riporti dell'ultima ALU, si accenderà automaticamente un allarme a 1 ogni volta che c'è overflow!</p>
  </section>

  <!-- ══════════════ SEZIONE 27 ══════════════ -->
  <section class="section" id="s27">
    <div class="section-header">
      <div class="section-num">27</div>
      <h2>La Centralina <span class="accent">a 4 Bit</span></h2>
    </div>

    <p class="lead">Ora che abbiamo costruito l'ALU completa, come fa la CPU a dirle cosa fare? Usa un codice "segreto" di 4 bit inviato su 4 fili speciali.</p>

    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>1 Filo:</strong> A-invert (inverte i bit di A)</li>
      <li><strong>1 Filo:</strong> B-negate (inverte B e setta il CarryIn iniziale a 1)</li>
      <li><strong>2 Fili:</strong> Operation (Sceglie cosa far uscire dal MUX finale: 00 per AND, 01 per OR, 10 per SUM, 11 per LESS)</li>
    </ul>

    <div class="card-grid cols2">
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
    
    <h3 style="font-size:20px;font-weight:600;color:var(--green);margin:40px 0 16px">L'Allarme "Zero" (Il NOR Gigante)</h3>
    <p>L'istruzione <code>beq</code> (Branch if Equal) salta se A e B sono uguali. L'hardware lo fa eseguendo A - B: se il risultato è zero, erano identici!
    Per intercettare lo zero assoluto in una frazione di secondo, tutti i 32 fili del risultato vengono infilati in una gigantesca porta <strong>OR seguita da un NOT (NOR)</strong>. Se anche un solo bit è 1, l'OR scatta e il NOT lo azzera. Ma se tutti i 32 bit sono 0, il NOR sputa fuori un '1', accendendo il filo d'allarme <strong>Zero</strong>!</p>

    <div style="margin: 24px 0; padding: 40px; border: 2px dashed var(--green); border-radius: 8px; text-align: center; background: rgba(34,197,94,0.05);">
      <p style="color: var(--green); font-weight: 600; font-size: 16px;">[ Placeholder Screenshot: Il Simbolo finale a "V" dell'ALU ]</p>
      <p style="font-size: 13px; color: var(--muted); margin-top: 8px;">(Mostra l'enorme V con i segnali di Controllo, Zero, e Result)</p>
    </div>

    <div class="callout green" style="margin-top:24px">
      <strong>La Scatola Nera</strong><br>
      Da questo momento in poi, nei diagrammi della CPU, smetteremo di disegnare MUX, XOR e cavi interni. Disegneremo solo questo simbolo a forma di "V": il Sacro Graal del calcolo binario!
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
    if (!btnA) return; // Prevent errors if simulator removed
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

# Aggiorniamo la sidebar in 06_circuiti.html
import re
def update_sidebar_text(match):
    html = match.group(0)
    html = html.replace('Laboratorio ALU', 'Gli Addizionatori')
    html = html.replace('Sottrazione e B-negate', 'ALU a 32 bit')
    html = html.replace('Il Magico slt e Overflow', 'Condizioni Avanzate')
    return html

content = re.sub(r'<nav class="sidebar">.*?</nav>', update_sidebar_text, content, flags=re.DOTALL)

with open('06_circuiti.html', 'w') as f:
    f.write(content)

# Aggiorniamo anche index.html
with open('index.html', 'r') as f:
    idx_content = f.read()

idx_content = idx_content.replace('title: "Laboratorio ALU", file: "06_circuiti.html"', 'title: "Gli Addizionatori", file: "06_circuiti.html"')
idx_content = idx_content.replace('title: "Sottrazione e B-negate"', 'title: "ALU a 32 bit e Sottrazione"')
idx_content = idx_content.replace('title: "Il Magico slt e Overflow"', 'title: "Condizioni Avanzate"')

with open('index.html', 'w') as f:
    f.write(idx_content)

print("Espansione ALU completata con placeholders!")
