import re

html_content = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RISC-V — Laboratorio ALU e Circuiti</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <style>
    /* Stili per i widget interattivi */
    .widget-container {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin: 24px 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .widget-title {
      font-family: 'DM Mono', monospace;
      font-size: 14px;
      font-weight: 600;
      color: var(--blue);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 20px;
    }
    .alu-grid {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 20px;
      width: 100%;
      align-items: center;
    }
    .alu-inputs, .alu-outputs {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .alu-core {
      position: relative;
      background: rgba(91, 156, 246, 0.1);
      border: 2px solid var(--blue);
      border-radius: 8px;
      padding: 40px 20px;
      text-align: center;
      min-width: 150px;
    }
    .alu-core::before {
      content: 'ALU 1-BIT';
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      font-family: 'DM Mono', monospace;
      font-size: 12px;
      color: var(--blue);
      font-weight: bold;
    }
    .bit-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .bit-label {
      font-size: 13px;
      color: var(--text);
      font-weight: 500;
      min-width: 60px;
    }
    .bit-btn {
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text);
      font-family: 'DM Mono', monospace;
      font-size: 16px;
      width: 40px;
      height: 40px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .bit-btn.active {
      background: var(--green);
      color: #000;
      border-color: var(--green);
    }
    .bit-btn:hover {
      border-color: var(--blue);
    }
    .bit-out {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: rgba(255,255,255,0.05);
      border: 1px dashed var(--border);
      font-family: 'DM Mono', monospace;
      font-size: 16px;
      width: 40px;
      height: 40px;
      border-radius: 8px;
      color: var(--text);
    }
    .bit-out.active {
      background: rgba(234, 179, 8, 0.2);
      border-color: var(--amber);
      color: var(--amber);
      font-weight: bold;
    }
    .op-select {
      background: var(--surface);
      border: 1px solid var(--blue);
      color: var(--blue);
      padding: 8px 12px;
      border-radius: 6px;
      font-family: 'DM Mono', monospace;
      font-size: 13px;
      cursor: pointer;
      outline: none;
    }
    
    .slt-diagram {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 30px;
      margin: 24px 0;
      position: relative;
    }
    .alu-box {
      border: 2px solid var(--border);
      padding: 10px;
      text-align: center;
      font-family: 'DM Mono', monospace;
      border-radius: 6px;
      background: var(--surface);
      width: 100px;
      margin: 10px auto;
      z-index: 2;
      position: relative;
    }
    .alu-box.highlight {
      border-color: var(--purple);
      color: var(--purple);
    }
    .wire-line {
      position: absolute;
      width: 2px;
      background: var(--purple);
      top: 60px;
      bottom: 60px;
      left: calc(50% + 70px);
      z-index: 1;
    }
    .wire-line::after {
      content: 'Set ➔ Less';
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--purple);
      font-family: 'DM Mono', monospace;
      font-size: 12px;
      white-space: nowrap;
    }
  </style>
</head>
<body>

<div class="layout">

<!-- SIDEBAR -->
<nav class="sidebar">
  <a class="sidebar-title" href="index.html">
    RISC-V Fondamentali
    <span>Guida completa</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s23">
    <div class="nav-dot"></div> I Mattoni Logici
    <span class="nav-num">23</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s24">
    <div class="nav-dot"></div> Laboratorio ALU
    <span class="nav-num">24</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s25">
    <div class="nav-dot"></div> Sottrazione e B-negate
    <span class="nav-num">25</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s26">
    <div class="nav-dot"></div> Il Magico slt e Overflow
    <span class="nav-num">26</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s27">
    <div class="nav-dot"></div> La Centralina a 4 bit
    <span class="nav-num">27</span>
  </a>
</nav>

<!-- MAIN -->
<main class="main">

  <!-- HERO -->
  <div class="hero">
    <div class="hero-tag">CAPITOLO 06 — CIRCUITI E ALU</div>
    <h1>Dentro la Calcolatrice<br><em>Costruire l'ALU da zero</em></h1>
    <p>Come l'hardware si trasforma in intelligenza logica: porte logiche, MUX, il complemento a 2 implementato fisicamente, e la genialità dietro l'istruzione <code>slt</code> e l'Overflow.</p>
  </div>

  <!-- ══════════════ SEZIONE 23 ══════════════ -->
  <section class="section" id="s23">
    <div class="section-header">
      <div class="section-num">23</div>
      <h2>I Mattoni <span class="accent">Logici</span></h2>
    </div>
    
    <p class="lead">Siamo scesi al Livello 0: qui il computer è solo un intricato sistema di tubature elettriche (a 0 Volt o 5 Volt). La matematica si costruisce "dirottando" questa elettricità tramite le Porte Logiche.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Porte Logiche, Decoder e MUX</h3>
    <div class="card-grid cols3">
      <div class="card blue">
        <div class="card-title">Porte Logiche</div>
        <p style="font-size:13px;margin:4px 0 0">Costruite con transistor, elaborano i segnali. AND (1 se entrambi veri), OR (1 se almeno uno vero), XOR (1 se diversi), NOT (inverte).</p>
      </div>
      <div class="card green">
        <div class="card-title">Decoder (Il cecchino)</div>
        <p style="font-size:13px;margin:4px 0 0">Riceve un numero (es. l'indirizzo a 32 bit) e accende esattamente <strong>una sola</strong> linea in uscita (quella corrispondente al numero).</p>
      </div>
      <div class="card teal">
        <div class="card-title">Multiplexer (MUX)</div>
        <p style="font-size:13px;margin:4px 0 0">Il "deviatore ferroviario". Ha tanti ingressi, un solo tubo di uscita e un filo di Controllo che decide quale ingresso far passare.</p>
      </div>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 24 ══════════════ -->
  <section class="section" id="s24">
    <div class="section-header">
      <div class="section-num">24</div>
      <h2>Laboratorio <span class="accent">ALU</span></h2>
    </div>

    <p class="lead">L'ALU a 32 bit è un mostro da milioni di transistor. Ma gli ingegneri sono pigri: progettano un'unica e perfetta ALU a 1-bit, e poi la fanno copiare 32 volte sul silicio collegandole a catena.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Simulatore ALU 1-bit</h3>
    <p style="font-size:14px;color:var(--text)">Clicca sui bottoni <strong>A, B e CarryIn</strong> per cambiare i bit in ingresso. Seleziona l'operazione desiderata e osserva come l'ALU sputa fuori il Risultato e l'eventuale riporto (CarryOut).</p>
    
    <div class="widget-container">
      <div class="widget-title">Interactive 1-Bit ALU Simulator</div>
      <div class="alu-grid">
        <!-- Ingressi -->
        <div class="alu-inputs">
          <div class="bit-row">
            <span class="bit-label">Input A</span>
            <button id="btnA" class="bit-btn">0</button>
          </div>
          <div class="bit-row">
            <span class="bit-label">Input B</span>
            <button id="btnB" class="bit-btn">0</button>
          </div>
          <div class="bit-row">
            <span class="bit-label" style="opacity:0.7">CarryIn</span>
            <button id="btnCin" class="bit-btn" style="border-style:dashed">0</button>
          </div>
        </div>
        
        <!-- Core ALU -->
        <div class="alu-core">
          <select id="opSelect" class="op-select">
            <option value="and">AND (00)</option>
            <option value="or">OR (01)</option>
            <option value="add" selected>SUM (10)</option>
          </select>
        </div>
        
        <!-- Uscite -->
        <div class="alu-outputs">
          <div class="bit-row">
            <span class="bit-out" id="resOut">0</span>
            <span class="bit-label">Result</span>
          </div>
          <div class="bit-row" style="margin-top:28px">
            <span class="bit-out" id="coutOut" style="border-style:dashed">0</span>
            <span class="bit-label" style="opacity:0.7">CarryOut</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="callout blue">
      <strong>La Catena del Riporto (CarryOut ➔ CarryIn)</strong><br>
      L'ALU a 32 bit si costruisce collegando il filo <code>CarryOut</code> della prima ALU direttamente nell'ingresso <code>CarryIn</code> della seconda ALU, e così via come un nastro trasportatore!
    </div>
  </section>

  <!-- ══════════════ SEZIONE 25 ══════════════ -->
  <section class="section" id="s25">
    <div class="section-header">
      <div class="section-num">25</div>
      <h2>Sottrazione <span class="accent">e B-negate</span></h2>
    </div>

    <p class="lead">Per fare una sottrazione (A - B), la CPU non ha un circuito apposito. Usa l'addizionatore (SUM) già costruito, ma applicando il trucco matematico del Complemento a 2.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">I due comandi hardware</h3>
    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>Aggiungere una porta NOT per l'ingresso B:</strong> Un MUX sceglie se mandare ad A il filo di B normale, oppure B negato.</li>
      <li><strong>Il trucco del "+1":</strong> Dato che il complemento a 2 richiede di ribaltare i bit e aggiungere 1, l'ingegnere accende il <code>CarryIn</code> iniziale della prima ALU 0 portandolo a 1.</li>
    </ul>

    <div class="card amber">
      <div class="card-title">Il Comando B-negate</div>
      <p style="font-size:13px;margin:4px 0 0">Dato che queste due operazioni vanno sempre fatte insieme per sottrarre, la CPU le unisce in un unico filo di comando chiamato <strong>B-negate</strong>. Quando B-negate è 1, il MUX inverte B e il CarryIn iniziale della ALU 0 viene automaticamente impostato a 1. La Sottrazione è servita!</p>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 26 ══════════════ -->
  <section class="section" id="s26">
    <div class="section-header">
      <div class="section-num">26</div>
      <h2>Il magico slt <span class="accent">e l'Overflow</span></h2>
    </div>

    <p class="lead">L'istruzione <code>slt</code> (Set Less Than) risponde a una domanda: "A è minore di B?". Se Sì, il risultato a 32 bit deve essere 1 (<code>00...01</code>). Se No, 0 (<code>00...00</code>). Come fa l'hardware a creare questi formati così precisi?</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">La Genialità del filo "Set" ➔ "Less"</h3>
    <p style="font-size:14px;color:var(--text);margin-bottom:20px">Per capire se A è minore di B, la CPU lancia di nascosto una sottrazione (A - B). Se il risultato matematico è negativo, vuol dire che A era più piccolo! Ma dove vediamo se il numero è negativo? Nel 31esimo bit (il bit del segno), che viene calcolato dall'<strong>ultima ALU in cima</strong>.</p>
    
    <div class="slt-diagram">
      <div class="alu-box highlight">ALU 31<br><span style="font-size:11px">Calcola il Segno</span></div>
      <div class="alu-box" style="opacity:0.3">ALU 30</div>
      <div class="alu-box" style="opacity:0.3">...</div>
      <div class="alu-box" style="opacity:0.3">ALU 1</div>
      <div class="alu-box highlight">ALU 0<br><span style="font-size:11px">Risultato Finale (1 o 0)</span></div>
      <div class="wire-line"></div>
    </div>
    
    <ol style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li>La CPU manda il comando: "Tutte le ALU da 1 a 31 sparino fuori 0 come risultato (così abbiamo 31 zeri)".</li>
      <li>L'ALU 31 calcola la matematica, scopre se il risultato è negativo (es. 1), e spara questo '1' su un tubicino speciale detto <strong>Set</strong>.</li>
      <li>Un cavo fisico lunghissimo prende questo '1' da Set e lo porta giù fino al tubicino <strong>Less</strong> dell'ALU 0.</li>
      <li>L'ALU 0 fa passare questo '1' nel suo Risultato. Ecco apparire magicamente <code>000...01</code> !</li>
    </ol>

    <h3 style="font-size:16px;font-weight:500;margin:24px 0 12px">Il problema dell'Overflow</h3>
    <p>Quando sommiamo due numeri positivi enormi e, matematicamente, esce un numero negativo, il risultato ha "strabordato" i 32 bit e non è valido. È un Overflow.
    L'hardware lo intercetta applicando una porta <strong>XOR</strong> tra il <code>CarryIn</code> e il <code>CarryOut</code> del 31esimo bit. Se sono diversi, la ALU fa scattare l'allarme e invia un segnale speciale alla CPU per bloccare tutto.</p>
  </section>

  <!-- ══════════════ SEZIONE 27 ══════════════ -->
  <section class="section" id="s27">
    <div class="section-header">
      <div class="section-num">27</div>
      <h2>La Centralina <span class="accent">a 4 Bit</span></h2>
    </div>

    <p class="lead">L'ALU è un mostro potente. Per pilotarla, l'Unità di Controllo manda 4 fili specifici che agiscono da "codice a barre" per dire ai vari MUX interni cosa devono fare.</p>

    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>1 Filo:</strong> A-invert (inverte A)</li>
      <li><strong>1 Filo:</strong> B-negate (inverte B e setta CarryIn = 1)</li>
      <li><strong>2 Fili:</strong> Operation (Sceglie se il MUX finale della ALU lascia uscire AND (00), OR (01), SUM (10) o LESS (11))</li>
    </ul>

    <div class="card-grid cols2">
      <div class="card purple">
        <div class="card-title">Addizione: 0010</div>
        <p style="font-size:13px;margin:4px 0 0">Niente inversioni (00), accendi SUM (10).</p>
      </div>
      <div class="card red">
        <div class="card-title">Sottrazione: 0110</div>
        <p style="font-size:13px;margin:4px 0 0">Attiva B-negate (01), accendi SUM (10).</p>
      </div>
      <div class="card teal">
        <div class="card-title">Set Less Than: 0111</div>
        <p style="font-size:13px;margin:4px 0 0">Attiva B-negate per sottrarre, ma fai uscire dal MUX finale il risultato proveniente dal filo LESS (11).</p>
      </div>
      <div class="card amber">
        <div class="card-title">NOR: 1100</div>
        <p style="font-size:13px;margin:4px 0 0">Inverti A e B (11), poi fai AND (00). Per la legge di De Morgan, NOT(A) AND NOT(B) equivale a NOR(A, B)!</p>
      </div>
    </div>
    
    <div class="callout green" style="margin-top:24px">
      <strong>Il simbolo a V</strong><br>
      Da questo momento, negli schemi grandi della CPU, tutta questa magia sparisce dietro a un unico blocco a forma di "V". Ha i due grossi ingressi A e B a sinistra, l'ingresso a 4 bit del Controllo sopra, e spara a destra il Risultato a 32 bit, oltre al filo d'allarme Zero (che si accende a 1 solo se tutti e 32 i bit del risultato sono 0, utilissimo per l'istruzione beq).
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
    const op = opSelect.value;
    let res = 0;
    let cout = 0;

    if (op === 'and') {
      res = valA & valB;
      cout = 0; // Carry doesn't make sense in AND, usually ignored or 0
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

  btnA.addEventListener('click', () => toggleBtn(btnA, v => valA = v));
  btnB.addEventListener('click', () => toggleBtn(btnB, v => valB = v));
  btnCin.addEventListener('click', () => toggleBtn(btnCin, v => valCin = v));
  opSelect.addEventListener('change', updateLogic);

  // Initialize
  updateLogic();
</script>

<script src="shared.js"></script>
</body>
</html>
"""

with open('06_circuiti.html', 'w') as f:
    f.write(html_content)

print("Generated 06_circuiti.html successfully!")
