import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

# Trova inizio sezione 26
start_s26 = content.find('<!-- ══════════════ SEZIONE 26: Latch SR ══════════════ -->')
end_s26 = content.find('</main>')

if start_s26 == -1 or end_s26 == -1:
    print("Errore: start_s26 o </main> non trovati")
    exit(1)

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

    <!-- SIMULATORE ANIMATO CSS -->
    <style>
      .latch-simulator {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        margin: 32px 0;
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
      
      .latch-diagram {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 60px;
        position: relative;
        padding: 20px 0;
      }
      .nor-gate {
        width: 140px;
        height: 60px;
        border: 3px solid var(--text);
        border-radius: 0 40px 40px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        font-weight: 900;
        letter-spacing: 2px;
        background: var(--bg);
        transition: all 0.3s;
      }
      .nor-gate::after {
        content: '';
        position: absolute;
        right: -10px;
        top: 25px;
        width: 10px;
        height: 10px;
        border: 3px solid var(--text);
        border-radius: 50%;
        background: var(--bg);
      }
      .latch-wire {
        position: absolute;
        height: 4px;
        background: #555;
        transition: background 0.3s, box-shadow 0.3s;
      }
      .wire-active {
        background: #ef4444 !important;
        box-shadow: 0 0 10px #ef4444;
      }
      .wire-r { left: -100px; top: 15px; width: 100px; }
      .wire-s { left: -100px; bottom: 15px; width: 100px; }
      .wire-qbar { right: -120px; top: 28px; width: 110px; }
      .wire-q { right: -120px; bottom: 28px; width: 110px; }
      
      .cross-wire {
        position: absolute;
        width: 4px;
        background: #555;
        transition: all 0.3s;
      }
      .cross-r-to-s { right: -80px; top: 28px; height: 90px; border-radius: 0 0 0 10px; }
      .cross-r-to-s-h { right: -80px; bottom: 42px; width: 220px; }
      
      .cross-s-to-r { right: -40px; bottom: 28px; height: 90px; border-radius: 10px 0 0 0; }
      .cross-s-to-r-h { right: -40px; top: 42px; width: 180px; }

      .wire-label {
        position: absolute;
        font-size: 16px;
        font-weight: bold;
        color: var(--text);
      }
      .lbl-r { left: -120px; top: 8px; }
      .lbl-s { left: -120px; bottom: 8px; }
      .lbl-qbar { right: -140px; top: 20px; }
      .lbl-q { right: -140px; bottom: 20px; }

      .latch-status {
        text-align: center;
        margin-top: 40px;
        font-size: 20px;
        font-weight: 800;
        color: var(--text);
        letter-spacing: 1px;
      }

      /* CHAOS ANIMATION */
      @keyframes chaosColors {
        0% { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
        50% { background: #555; box-shadow: none; }
        100% { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
      }
      .chaos-mode .latch-wire, .chaos-mode .cross-wire {
        animation: chaosColors 0.1s infinite !important;
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
    </style>

    <div class="latch-simulator" id="latchSim">
      <div class="latch-controls">
        <button id="btnSet" class="latch-btn set-btn">1. SET (Accendi)</button>
        <button id="btnHold" class="latch-btn hold-btn">2. HOLD (Ricorda)</button>
        <button id="btnReset" class="latch-btn reset-btn">3. RESET (Spegni)</button>
      </div>
      
      <div class="latch-diagram">
        <!-- R Wire -->
        <div class="wire-label lbl-r">R</div>
        <div class="latch-wire wire-r" id="wR"></div>
        
        <!-- S Wire -->
        <div class="wire-label lbl-s">S</div>
        <div class="latch-wire wire-s" id="wS"></div>
        
        <!-- NOR TOP -->
        <div class="nor-gate">NOR</div>
        
        <!-- NOR BOTTOM -->
        <div class="nor-gate">NOR</div>
        
        <!-- QBar Wire -->
        <div class="latch-wire wire-qbar" id="wQbar"></div>
        <div class="wire-label lbl-qbar">!Q</div>
        
        <!-- Q Wire -->
        <div class="latch-wire wire-q" id="wQ"></div>
        <div class="wire-label lbl-q">Q</div>

        <!-- Cross from Top to Bottom -->
        <div class="cross-wire cross-r-to-s" id="cRtoS_v"></div>
        <div class="latch-wire cross-r-to-s-h" id="cRtoS_h"></div>
        
        <!-- Cross from Bottom to Top -->
        <div class="cross-wire cross-s-to-r" id="cStoR_v"></div>
        <div class="latch-wire cross-s-to-r-h" id="cStoR_h"></div>
      </div>
      
      <div class="latch-status" id="lStatus">Stato: SPENTO (Q=0)</div>
    </div>

    <div class="card blue" style="margin-top:16px;">
      <div class="card-title">Il Trucco Umano</div>
      <p style="font-size:14px;margin:4px 0 0">Guarda i fili rossi: <strong>l'1 comanda la NOR</strong> costringendola a sputare 0. Quello 0 scorre nei fili incrociati costringendo l'altra NOR a sputare un 1 a conferma! È un loop magico.</p>
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
  // Latch SR Logic
  const wR = document.getElementById('wR');
  const wS = document.getElementById('wS');
  const wQ = document.getElementById('wQ');
  const wQbar = document.getElementById('wQbar');
  
  const cRtoS_v = document.getElementById('cRtoS_v');
  const cRtoS_h = document.getElementById('cRtoS_h');
  const cStoR_v = document.getElementById('cStoR_v');
  const cStoR_h = document.getElementById('cStoR_h');
  
  const lStatus = document.getElementById('lStatus');
  const latchSim = document.getElementById('latchSim');

  let stateQ = 0; // 0 o 1

  function renderLatch(s, r) {
    latchSim.classList.remove('chaos-mode');
    
    // Inputs
    wS.classList.toggle('wire-active', s === 1);
    wR.classList.toggle('wire-active', r === 1);

    // Outputs
    if (s === 1 && r === 0) stateQ = 1;
    if (s === 0 && r === 1) stateQ = 0;
    // se 0,0 -> mantieni stateQ
    
    let q = stateQ;
    let qbar = stateQ === 1 ? 0 : 1;
    
    // CASO ASSURDO 1,1 non permessso normalmente, ma la porta logicamente darebbe 0,0
    if (s===1 && r===1) { q = 0; qbar = 0; }

    wQ.classList.toggle('wire-active', q === 1);
    wQbar.classList.toggle('wire-active', qbar === 1);

    // Cross wires
    // il cross dall'alto (Qbar) al basso
    cRtoS_v.classList.toggle('wire-active', qbar === 1);
    cRtoS_h.classList.toggle('wire-active', qbar === 1);
    
    // il cross dal basso (Q) all'alto
    cStoR_v.classList.toggle('wire-active', q === 1);
    cStoR_h.classList.toggle('wire-active', q === 1);

    if (q===1 && qbar===0) lStatus.textContent = "Stato: ACCESO (Q = 1)";
    else if (q===0 && qbar===1) lStatus.textContent = "Stato: SPENTO (Q = 0)";
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

# The previous script might have already added `shared.js` and `</body>`.
# We need to inject the HTML before </main> and the JS before </body>.
content_html = content[:start_s26] + new_s26 + "\n  " + content[end_s26:]

# Add JS logic before </body>
body_end = content_html.rfind('</body>')
if body_end != -1:
    content_final = content_html[:body_end] + js_logic + content_html[body_end:]
else:
    content_final = content_html + js_logic

with open('06_circuiti.html', 'w') as f:
    f.write(content_final)

print("Riscrittura interattiva completata!")
