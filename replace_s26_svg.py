import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

start_s26 = content.find('<!-- ══════════════ SEZIONE 26: Latch SR ══════════════ -->')
end_s26 = content.find('</main>')

new_s26 = '''
  <!-- ══════════════ SEZIONE 26: Latch SR ══════════════ -->
  <section class="section" id="s26">
    <div class="section-header">
      <div class="section-num">26</div>
      <h2>Circuiti Sequenziali: <span class="accent">Il Latch SR Animato</span></h2>
    </div>

    <ul style="font-size:15px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:24px;">
      <li>L'ALU calcola ma <em>non ricorda</em>. Il <strong>Latch SR</strong> intrappola il segnale elettrico, creando la memoria.</li>
      <li>È formato da due porte <strong>NOR incrociate</strong> (l'uscita di una è l'ingresso dell'altra).</li>
      <li><strong>I Comandi:</strong>
         <ul style="margin-top:8px;">
           <li><strong>Set (S=1)</strong>: Salva e accende la memoria a 1.</li>
           <li><strong>Reset (R=1)</strong>: Azzera e spegne la memoria a 0.</li>
           <li><strong>Hold (S=0, R=0)</strong>: Chiude gli ingressi. Ricorda l'ultimo valore per sempre.</li>
         </ul>
      </li>
    </ul>

    <!-- SIMULATORE SVG -->
    <style>
      .latch-simulator {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        margin: 32px 0;
        text-align: center;
      }
      .latch-controls {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-bottom: 40px;
      }
      .latch-btn {
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s, filter 0.2s;
        color: #fff;
      }
      .latch-btn:hover { filter: brightness(1.2); transform: translateY(-2px); }
      .set-btn { background: #3b82f6; }
      .reset-btn { background: #ef4444; }
      .hold-btn { background: #8b5cf6; }
      
      .nor-gate {
        width: 140px;
        height: 70px;
        border: 3px solid var(--text);
        border-radius: 0 50px 50px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        position: absolute;
        font-weight: 900;
        font-size: 20px;
        letter-spacing: 2px;
        background: var(--bg);
        z-index: 2;
        color: var(--text);
      }
      .nor-gate::after {
        content: '';
        position: absolute;
        right: -12px;
        top: 26px;
        width: 12px;
        height: 12px;
        border: 3px solid var(--text);
        border-radius: 50%;
        background: var(--bg);
      }

      .latch-status {
        margin-top: 20px;
        font-size: 20px;
        font-weight: 800;
        color: var(--text);
        letter-spacing: 1px;
      }

      @keyframes flashRed {
        0% { stroke: #ef4444; fill: #ef4444; }
        50% { stroke: var(--text); fill: var(--text); }
        100% { stroke: #ef4444; fill: #ef4444; }
      }
      .chaos-mode .wire-path, .chaos-mode .wire-text {
        animation: flashRed 0.1s infinite;
      }
      .chaos-btn {
        background: transparent;
        border: 2px dashed #ef4444;
        color: #ef4444;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s;
      }
      .chaos-btn:hover {
        background: #ef4444;
        color: #fff;
      }
      .wire-active {
        stroke: #ef4444 !important;
      }
      .text-active {
        fill: #ef4444 !important;
      }
    </style>

    <div class="latch-simulator" id="latchSim">
      <div class="latch-controls">
        <button id="btnSet" class="latch-btn set-btn">1. SET (S=1, R=0)</button>
        <button id="btnHold" class="latch-btn hold-btn">2. HOLD (S=0, R=0)</button>
        <button id="btnReset" class="latch-btn reset-btn">3. RESET (S=0, R=1)</button>
      </div>
      
      <div style="position: relative; width: 400px; height: 300px; margin: 0 auto;">
        
        <!-- NOR TOP -->
        <div class="nor-gate" style="left: 100px; top: 45px;">NOR</div>
        
        <!-- NOR BOTTOM -->
        <div class="nor-gate" style="left: 100px; top: 185px;">NOR</div>
        
        <svg width="400" height="300" style="position:absolute; top:0; left:0; z-index:1; pointer-events:none;">
           
           <!-- S Wire (Top Left) -->
           <line id="lineS" class="wire-path" x1="20" y1="60" x2="100" y2="60" stroke="var(--text)" stroke-width="3" />
           <text x="5" y="66" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">S</text>
           <text id="valS" x="60" y="50" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
           
           <!-- R Wire (Bottom Left) -->
           <line id="lineR" class="wire-path" x1="20" y1="240" x2="100" y2="240" stroke="var(--text)" stroke-width="3" />
           <text x="5" y="246" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">R</text>
           <text id="valR" x="60" y="230" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
           
           <!-- Qbar Wire (Top Right) -->
           <line id="lineQbar" class="wire-path" x1="255" y1="80" x2="350" y2="80" stroke="var(--text)" stroke-width="3" />
           <text x="360" y="86" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text"><tspan text-decoration="overline">Q</tspan></text>
           <text id="valQbar" x="310" y="70" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">1</text>
           <circle cx="280" cy="80" r="4" fill="var(--text)" class="wire-text"/>
           
           <!-- Q Wire (Bottom Right) -->
           <line id="lineQ" class="wire-path" x1="255" y1="220" x2="350" y2="220" stroke="var(--text)" stroke-width="3" />
           <text x="360" y="226" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">Q</text>
           <text id="valQ" x="310" y="245" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
           <circle cx="260" cy="220" r="4" fill="var(--text)" class="wire-text"/>
           
           <!-- CROSS TOP TO BOTTOM (!Q -> Bottom NOR) -->
           <polyline id="lineCrossTB" class="wire-path" points="280,80 280,105 80,200 80,200 100,200" stroke="var(--text)" stroke-width="3" fill="none" />
           <text id="valCrossTB" x="85" y="190" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">1</text>
           
           <!-- CROSS BOTTOM TO TOP (Q -> Top NOR) -->
           <polyline id="lineCrossBT" class="wire-path" points="260,220 260,195 80,100 80,100 100,100" stroke="var(--text)" stroke-width="3" fill="none" />
           <text id="valCrossBT" x="85" y="90" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
        </svg>

      </div>
      <div class="latch-status" id="lStatus">Stato: SPENTO (Q=0)</div>
    </div>

    <div class="card blue" style="margin-top:16px;">
      <div class="card-title">Il Trucco Umano</div>
      <p style="font-size:14px;margin:4px 0 0">Guarda i fili rossi: <strong>l'1 comanda la NOR</strong> costringendola a sputare 0. Quello 0 scorre nei fili incrociati costringendo l'altra NOR a sputare un 1 a conferma! È un loop perfetto.</p>
    </div>

    <h3 style="font-size:18px;font-weight:600;color:var(--red);margin:40px 0 16px">L'Oscillazione (Il disastro S=1, R=1)</h3>
    <ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:24px;">
      <li>Se premi Set e Reset assieme, entrambe le NOR sputano 0 (un assurdo logico).</li>
      <li>Se li <strong>rilasci simultaneamente</strong> (Hold), le porte si rincorrono: sputano 1, poi vedono l'1 e sputano 0, in un <strong>loop infinito e imprevedibile</strong>. Provalo!</li>
    </ul>

    <div style="text-align:center; margin-bottom:32px;">
      <button id="btnChaos" class="chaos-btn">⚠️ INNESCA OSCILLAZIONE ⚠️</button>
    </div>
  </section>
'''

js_logic = '''
<script>
  // LATCH SVG LOGIC
  const valS = document.getElementById('valS');
  const valR = document.getElementById('valR');
  const valQbar = document.getElementById('valQbar');
  const valQ = document.getElementById('valQ');
  const valCrossTB = document.getElementById('valCrossTB'); // !Q feeding into Bottom NOR
  const valCrossBT = document.getElementById('valCrossBT'); // Q feeding into Top NOR

  const lineS = document.getElementById('lineS');
  const lineR = document.getElementById('lineR');
  const lineQbar = document.getElementById('lineQbar');
  const lineQ = document.getElementById('lineQ');
  const lineCrossTB = document.getElementById('lineCrossTB');
  const lineCrossBT = document.getElementById('lineCrossBT');

  const lStatus = document.getElementById('lStatus');
  const latchSim = document.getElementById('latchSim');

  let stateQ = 0;

  function renderLatch(s, r) {
    latchSim.classList.remove('chaos-mode');
    
    // Compute Logic
    if (s === 1 && r === 0) stateQ = 1;
    if (s === 0 && r === 1) stateQ = 0;
    
    let q = stateQ;
    let qbar = stateQ === 1 ? 0 : 1;
    
    // Invalid state
    if (s === 1 && r === 1) { q = 0; qbar = 0; }

    // Update Texts
    valS.textContent = s;
    valR.textContent = r;
    valQ.textContent = q;
    valQbar.textContent = qbar;
    
    // The cross from Top (!Q) feeds Bottom NOR
    valCrossTB.textContent = qbar;
    // The cross from Bottom (Q) feeds Top NOR
    valCrossBT.textContent = q;

    // Update Colors (1 = active/red, 0 = inactive)
    const activeClass = 'text-active';
    const wireClass = 'wire-active';
    
    valS.classList.toggle(activeClass, s === 1);
    lineS.classList.toggle(wireClass, s === 1);
    
    valR.classList.toggle(activeClass, r === 1);
    lineR.classList.toggle(wireClass, r === 1);
    
    valQbar.classList.toggle(activeClass, qbar === 1);
    lineQbar.classList.toggle(wireClass, qbar === 1);
    
    valQ.classList.toggle(activeClass, q === 1);
    lineQ.classList.toggle(wireClass, q === 1);
    
    valCrossTB.classList.toggle(activeClass, qbar === 1);
    lineCrossTB.classList.toggle(wireClass, qbar === 1);
    
    valCrossBT.classList.toggle(activeClass, q === 1);
    lineCrossBT.classList.toggle(wireClass, q === 1);

    // Status Message
    if (q === 1 && qbar === 0) lStatus.textContent = "Stato: ACCESO (Q = 1)";
    else if (q === 0 && qbar === 1) lStatus.textContent = "Stato: SPENTO (Q = 0)";
    else lStatus.textContent = "Stato: ASSURDO (Q=0, !Q=0)";
  }

  document.getElementById('btnSet').addEventListener('click', () => renderLatch(1, 0));
  document.getElementById('btnReset').addEventListener('click', () => renderLatch(0, 1));
  document.getElementById('btnHold').addEventListener('click', () => renderLatch(0, 0));

  document.getElementById('btnChaos').addEventListener('click', () => {
    lStatus.textContent = "OSCILLAZIONE CRITICA!!";
    latchSim.classList.add('chaos-mode');
  });

  // Init
  renderLatch(0, 1);
</script>
'''

content_without_s26 = content[:start_s26] + content[end_s26:]

# Insert the new section right before </main>
insert_pos = content_without_s26.rfind('</main>')
content_html = content_without_s26[:insert_pos] + new_s26 + "\n  " + content_without_s26[insert_pos:]

# Trova dove si trovano i precedenti script js_logic e eliminali se presenti.
# Dato che lo script vecchio faceva uso di `valA` (nel file shared o s25) potrei solo appendere.
# Troviamo l'ultimo </script> e inseriamo lì.
script_end = content_html.rfind('</body>')
content_final = content_html[:script_end] + js_logic + content_html[script_end:]

with open('06_circuiti.html', 'w') as f:
    f.write(content_final)

print("Riscrittura SVG Layout Esatto completata!")
