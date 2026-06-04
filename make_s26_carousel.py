import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

start_s26 = content.find('<!-- ══════════════ SEZIONE 26: Latch SR ══════════════ -->')
end_main = content.find('</main>')
if start_s26 == -1:
    print("S26 non trovata")
    exit(1)

svg_latch_html = '''
    <!-- SIMULATORE SVG -->
    <style>
      .latch-simulator { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 32px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); margin: 32px 0; text-align: center; }
      .latch-controls { display: flex; justify-content: center; gap: 16px; margin-bottom: 40px; }
      .latch-btn { padding: 10px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: transform 0.2s, filter 0.2s; color: #fff; }
      .latch-btn:hover { filter: brightness(1.2); transform: translateY(-2px); }
      .set-btn { background: #3b82f6; }
      .reset-btn { background: #ef4444; }
      .hold-btn { background: #8b5cf6; }
      .nor-gate { width: 140px; height: 70px; border: 3px solid var(--text); border-radius: 0 50px 50px 0; display: flex; align-items: center; justify-content: center; position: absolute; font-weight: 900; font-size: 20px; letter-spacing: 2px; background: var(--bg); z-index: 2; color: var(--text); }
      .nor-gate::after { content: ''; position: absolute; right: -12px; top: 26px; width: 12px; height: 12px; border: 3px solid var(--text); border-radius: 50%; background: var(--bg); }
      .latch-status { margin-top: 20px; font-size: 20px; font-weight: 800; color: var(--text); letter-spacing: 1px; }
      @keyframes flashRed { 0% { stroke: #ef4444; fill: #ef4444; } 50% { stroke: var(--text); fill: var(--text); } 100% { stroke: #ef4444; fill: #ef4444; } }
      .chaos-mode .wire-path, .chaos-mode .wire-text { animation: flashRed 0.1s infinite; }
      .chaos-btn { background: transparent; border: 2px dashed #ef4444; color: #ef4444; padding: 12px 24px; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; transition: all 0.3s; }
      .chaos-btn:hover { background: #ef4444; color: #fff; }
      .wire-active { stroke: #ef4444 !important; }
      .text-active { fill: #ef4444 !important; }
    </style>

    <div class="latch-simulator" id="latchSim">
      <div class="latch-controls">
        <button id="btnSet" class="latch-btn set-btn">1. SET (S=1, R=0)</button>
        <button id="btnHold" class="latch-btn hold-btn">2. HOLD (S=0, R=0)</button>
        <button id="btnReset" class="latch-btn reset-btn">3. RESET (S=0, R=1)</button>
      </div>
      <div style="position: relative; width: 400px; height: 300px; margin: 0 auto;">
        <div class="nor-gate" style="left: 100px; top: 45px;">NOR</div>
        <div class="nor-gate" style="left: 100px; top: 185px;">NOR</div>
        <svg width="400" height="300" style="position:absolute; top:0; left:0; z-index:1; pointer-events:none;">
           <line id="lineS" class="wire-path" x1="20" y1="60" x2="100" y2="60" stroke="var(--text)" stroke-width="3" />
           <text x="5" y="66" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">S</text>
           <text id="valS" x="60" y="50" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
           <line id="lineR" class="wire-path" x1="20" y1="240" x2="100" y2="240" stroke="var(--text)" stroke-width="3" />
           <text x="5" y="246" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">R</text>
           <text id="valR" x="60" y="230" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
           <line id="lineQbar" class="wire-path" x1="255" y1="80" x2="350" y2="80" stroke="var(--text)" stroke-width="3" />
           <text x="360" y="86" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text"><tspan text-decoration="overline">Q</tspan></text>
           <text id="valQbar" x="310" y="70" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">1</text>
           <circle cx="280" cy="80" r="4" fill="var(--text)" class="wire-text"/>
           <line id="lineQ" class="wire-path" x1="255" y1="220" x2="350" y2="220" stroke="var(--text)" stroke-width="3" />
           <text x="360" y="226" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">Q</text>
           <text id="valQ" x="310" y="245" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
           <circle cx="260" cy="220" r="4" fill="var(--text)" class="wire-text"/>
           <polyline id="lineCrossTB" class="wire-path" points="280,80 280,105 80,200 80,200 100,200" stroke="var(--text)" stroke-width="3" fill="none" />
           <text id="valCrossTB" x="85" y="190" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">1</text>
           <polyline id="lineCrossBT" class="wire-path" points="260,220 260,195 80,100 80,100 100,100" stroke="var(--text)" stroke-width="3" fill="none" />
           <text id="valCrossBT" x="85" y="90" font-size="20" font-weight="bold" fill="var(--text)" class="wire-text">0</text>
        </svg>
      </div>
      <div class="latch-status" id="lStatus">Stato: SPENTO (Q=0)</div>
    </div>
'''

new_s26 = f'''
  <!-- ══════════════ SEZIONE 26: Latch SR ══════════════ -->
  <section class="section" id="s26">
    <div class="section-header">
      <div class="section-num">26</div>
      <h2>L'Evoluzione <span class="accent">della Memoria</span></h2>
    </div>

    <p class="lead">L'ALU calcola ma non ricorda. Seguiamo l'evoluzione dei circuiti di memoria (Circuiti Sequenziali): dalla forma più elementare instabile fino al sofisticato Flip-Flop utilizzato nelle CPU vere.</p>

    <style>
      .carousel-slides-container-6 {{
        display: flex;
        transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
        width: 600%; /* 6 slides */
      }}
      .carousel-slide-6 {{
        width: 16.6666%; /* 100% / 6 */
        padding: 40px;
        box-sizing: border-box;
      }}
    </style>

    <div class="carousel-wrapper">
      <div class="carousel-header">
        <h3 class="carousel-title" id="carouselTitle2">Fase 1: Il Latch SR</h3>
        <div class="carousel-controls">
          <button class="carousel-btn" id="prevBtn2" disabled>&#8592; Indietro</button>
          <span class="carousel-indicator" id="carouselIndicator2">1 / 6</span>
          <button class="carousel-btn" id="nextBtn2">Avanti &#8594;</button>
        </div>
      </div>
      
      <div class="carousel-slides-container-6" id="slidesContainer2">
        
        <!-- SLIDE 1 -->
        <div class="carousel-slide-6">
          <div class="slide-content">
            <ul style="font-size:15px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:0;">
              <li>Il <strong>Latch SR</strong> è formato da due porte NOR incrociate (l'uscita di una è l'ingresso dell'altra).</li>
              <li><strong>Set (S=1)</strong> accende la memoria a 1. <strong>Reset (R=1)</strong> la spegne a 0.</li>
              <li><strong>Hold (S=0, R=0)</strong> chiude gli ingressi, mantenendo il segnale intrappolato nel loop.</li>
            </ul>
            {svg_latch_html}
            <div style="text-align:center; margin-bottom:16px;">
              <button id="btnChaos" class="chaos-btn">⚠️ INNESCA OSCILLAZIONE ⚠️</button>
            </div>
            <p style="font-size:14px; text-align:center; color:var(--text);">Se si innesca S=1 e R=1 e si rilasciano assieme, si ottiene un loop infinito (Oscillazione).</p>
          </div>
        </div>

        <!-- SLIDE 2 -->
        <div class="carousel-slide-6">
          <div class="slide-content">
            <h4>Latch SR Sincronizzato</h4>
            <ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>Il Problema:</strong> Il Latch base cambia stato <em>in qualsiasi momento</em> se un filo sbalza (rumore). È instabile per una CPU.</li>
              <li><strong>La Soluzione:</strong> Aggiungiamo un interruttore generale, il <strong>Clock (C)</strong>. I comandi S e R vengono mascherati da porte AND con il Clock.</li>
              <li><strong>Risultato:</strong> La memoria può cambiare stato <em>solo ed esclusivamente</em> quando C = 1 (finestra temporale aperta).</li>
            </ul>
            <img src="assets/latch/latch-SR-sincronizzato.png" alt="Latch SR Sincronizzato">
          </div>
        </div>

        <!-- SLIDE 3 -->
        <div class="carousel-slide-6">
          <div class="slide-content">
            <h4>Latch D Sincronizzato</h4>
            <ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>Il Problema:</strong> L'utente può ancora sbagliare e premere S=1 e R=1, mandando il Latch in oscillazione.</li>
              <li><strong>La Soluzione:</strong> Eliminiamo il doppio comando! Creiamo un solo ingresso <strong>Data (D)</strong>. Il segnale D entra diretto nel Set, e invertito (tramite un NOT) nel Reset.</li>
              <li><strong>Risultato:</strong> È matematicamente impossibile che Set e Reset valgano 1 contemporaneamente. Assicurazione totale.</li>
            </ul>
            <img src="assets/latch/latch-D-sincronizzato.png" alt="Latch D Sincronizzato">
          </div>
        </div>

        <!-- SLIDE 4 -->
        <div class="carousel-slide-6">
          <div class="slide-content">
            <h4>Il Problema della Trasparenza</h4>
            <ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>Il Problema:</strong> Il Latch D è "aperto" <em>per tutto il tempo</em> in cui il Clock vale 1 (level-triggered).</li>
              <li><strong>Il Disastro:</strong> Se il dato (D) oscilla o cambia a metà strada mentre la finestra è ancora aperta, l'uscita (Q) lo rincorre e si modifica subito!</li>
              <li><strong>L'Effetto Trasparenza:</strong> Il segnale "scivola" dritto attraverso la memoria, distruggendo il rigoroso tempismo della CPU.</li>
            </ul>
            <img src="assets/diagramma-temporale-latchD.png" alt="Diagramma temporale Trasparenza" style="max-width:500px">
          </div>
        </div>

        <!-- SLIDE 5 -->
        <div class="carousel-slide-6">
          <div class="slide-content">
            <h4>Il Flip-Flop D (Master-Slave)</h4>
            <ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>La Soluzione (Edge-Triggered):</strong> Non salvare il dato per <em>tutto il tempo</em>, ma <strong>esattamente nell'istante</strong> in cui il Clock scatta da 0 a 1 (fronte di salita).</li>
              <li><strong>Architettura:</strong> Mettiamo in serie due Latch D. Il Master copia il dato quando Clock=0. Lo Slave aggiorna l'uscita finale solo appena il clock diventa 1 e il Master si blinda.</li>
              <li><strong>Risultato:</strong> Nessuna trasparenza. La memoria cattura un fotogramma istantaneo del dato!</li>
            </ul>
            <img src="assets/latch/flipflop-tipoD.png" alt="Flip Flop Tipo D">
          </div>
        </div>

        <!-- SLIDE 6 -->
        <div class="carousel-slide-6">
          <div class="slide-content">
            <h4>Flip-Flop D (Fronte di Discesa)</h4>
            <ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>Variante:</strong> Invertendo il clock nei latch Master-Slave, catturiamo il dato esattamente quando il clock <strong>scende</strong> da 1 a 0 (fronte di discesa).</li>
              <li><strong>Perché è vitale:</strong> Durante la metà alta del clock (C=1) le ALU fanno calcoli selvaggi, generando rumore. Registrare il dato in discesa assicura che il segnale elettrico si sia perfettamente stabilizzato!</li>
            </ul>
            <img src="assets/latch/flipflop-tipoD-fronteDiscesa.png" alt="Flip Flop Tipo D Fronte Discesa">
            <div style="display:flex; justify-content:center; margin-top:24px;">
                <img src="assets/latch/flipFlop-ritardo.png" alt="Flip Flop Ritardo" style="max-width:300px; margin-top:0;">
            </div>
            <p style="text-align:center; font-size:13px; margin-top:8px;"><em>Il piccolo ritardo fisiologico (delay) prima che Q si aggiorni.</em></p>
          </div>
        </div>

      </div>
    </div>
  </section>
'''

content_no_s26 = content[:start_s26] + content[end_main:]
insert_pos = content_no_s26.rfind('</main>')
content_html = content_no_s26[:insert_pos] + new_s26 + "\n  " + content_no_s26[insert_pos:]

script_end = content_html.rfind('</script>')
if script_end == -1:
    print("Script end non trovato")
    exit(1)

js_carousel_2 = '''
  // Logica per il Carousel 2 (Memoria)
  const titles2 = [
    "Fase 1: Il Latch SR",
    "Fase 2: Latch SR Sincronizzato",
    "Fase 3: Latch D Sincronizzato",
    "Fase 4: Il Problema Trasparenza",
    "Fase 5: Il Flip-Flop D",
    "Fase 6: Flip-Flop D (Discesa)"
  ];
  
  let currentSlide2 = 0;
  const maxSlides2 = 6;
  const container2 = document.getElementById('slidesContainer2');
  const prevBtn2 = document.getElementById('prevBtn2');
  const nextBtn2 = document.getElementById('nextBtn2');
  const indicator2 = document.getElementById('carouselIndicator2');
  const title2 = document.getElementById('carouselTitle2');

  function updateCarousel2() {
    container2.style.transform = `translateX(-${currentSlide2 * 16.6666}%)`;
    indicator2.textContent = `${currentSlide2 + 1} / ${maxSlides2}`;
    title2.textContent = titles2[currentSlide2];
    
    prevBtn2.disabled = currentSlide2 === 0;
    nextBtn2.disabled = currentSlide2 === maxSlides2 - 1;
  }

  prevBtn2.addEventListener('click', () => {
    if (currentSlide2 > 0) {
      currentSlide2--;
      updateCarousel2();
    }
  });

  nextBtn2.addEventListener('click', () => {
    if (currentSlide2 < maxSlides2 - 1) {
      currentSlide2++;
      updateCarousel2();
    }
  });
'''

content_html = content_html[:script_end] + js_carousel_2 + "\n" + content_html[script_end:]

content_html = content_html.replace('<div class="nav-dot"></div> Il Latch SR', '<div class="nav-dot"></div> Evoluzione Memoria')

with open('06_circuiti.html', 'w') as f:
    f.write(content_html)

with open('index.html', 'r') as f:
    idx_content = f.read()

idx_content = idx_content.replace('{ id: "s26", title: "Circuiti Sequenziali (Latch SR)"', '{ id: "s26", title: "L\'Evoluzione della Memoria"')

with open('index.html', 'w') as f:
    f.write(idx_content)

print("Riscrittura Carousel 6-Fasi completata!")
