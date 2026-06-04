import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

# Trova inizio sezione 25
start_marker = '<!-- ══════════════ SEZIONE 25 ══════════════ -->'
start_idx = content.find(start_marker)

if start_idx == -1:
    print("Errore: start_marker s25 non trovato")
    exit(1)

# Estrai il simulatore JS originale se serve. Actually we can just write the whole JS logic anew to be safe.
# Find where the script starts
script_idx = content.find('<script>', start_idx)
script_end_idx = content.find('</body>', script_idx)
original_script = content[script_idx:script_end_idx]

# Remove the old script tag to rewrite everything clearly.
content_before_script = content[:script_idx]

# Creiamo il CSS + HTML per il Carousel e le 5 fasi
new_content = '''<!-- ══════════════ SEZIONE 25: L'Evoluzione dell'ALU ══════════════ -->
  <section class="section" id="s25">
    <div class="section-header">
      <div class="section-num">25</div>
      <h2>L'Evoluzione <span class="accent">dell'ALU</span></h2>
    </div>

    <p class="lead">Non possiamo studiare un'ALU a 32 bit guardandola tutta intera: esploderebbe il cervello. Dobbiamo costruirla pezzo per pezzo, partendo da un singolo bit debole e potenziandolo ad ogni ostacolo. Esplora le fasi qui sotto!</p>

    <style>
      .carousel-wrapper {
        position: relative;
        overflow: hidden;
        border-radius: 12px;
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin: 40px 0;
      }
      .carousel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 32px;
        background: rgba(0,0,0,0.2);
        border-bottom: 1px solid var(--border);
      }
      .carousel-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--blue);
        margin: 0;
      }
      .carousel-controls {
        display: flex;
        gap: 16px;
        align-items: center;
      }
      .carousel-btn {
        background: var(--blue);
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .carousel-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
      }
      .carousel-btn:disabled {
        opacity: 0.3;
        cursor: not-allowed;
      }
      .carousel-indicator {
        font-size: 14px;
        color: var(--muted);
        font-weight: 500;
      }
      .carousel-slides-container {
        display: flex;
        transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
        width: 500%; /* 5 slides */
      }
      .carousel-slide {
        width: 20%; /* 100% / 5 */
        padding: 40px;
        box-sizing: border-box;
      }
      .slide-content img {
        width: 100%;
        max-width: 600px;
        border-radius: 8px;
        border: 1px solid var(--border);
        margin-top: 24px;
        display: block;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      }
      .slide-content h4 {
        font-size: 18px;
        font-weight: 600;
        margin: 0 0 16px 0;
        color: var(--text);
      }
      .slide-content p {
        font-size: 15px;
        line-height: 1.6;
        color: var(--text);
        margin-bottom: 16px;
      }
    </style>

    <div class="carousel-wrapper">
      <div class="carousel-header">
        <h3 class="carousel-title" id="carouselTitle">Fase 1: L'ALU "Neanderthal"</h3>
        <div class="carousel-controls">
          <button class="carousel-btn" id="prevBtn" disabled>&#8592; Indietro</button>
          <span class="carousel-indicator" id="carouselIndicator">1 / 5</span>
          <button class="carousel-btn" id="nextBtn">Avanti &#8594;</button>
        </div>
      </div>
      
      <div class="carousel-slides-container" id="slidesContainer">
        
        <!-- SLIDE 1 -->
        <div class="carousel-slide">
          <div class="slide-content">
            <p>Costruiamo la versione primordiale dell'ALU: un circuito capace solo di eseguire le tre operazioni fondamentali su un singolo bit: AND, OR e l'Addizione matematica.</p>
            <p>Gli ingegneri piazzano in parallelo una porta AND, una porta OR e il nostro Full Adder. A decidere quale risultato sopravvivrà ci pensa un <strong>Multiplexer a 3 ingressi</strong> comandato dal filo <code>Operation</code>.</p>
            <img src="assets/alu/alu-1bit.png" alt="ALU 1 bit base">
            
            <div style="margin-top:32px; background:rgba(0,0,0,0.1); padding:20px; border-radius:12px;">
              <h4>Testa l'ALU Base:</h4>
              <div class="alu-grid" style="max-width:400px; margin:0;">
                <div class="alu-inputs">
                  <div class="bit-row"><span class="bit-label">A</span><button id="btnA" class="bit-btn">0</button></div>
                  <div class="bit-row"><span class="bit-label">B</span><button id="btnB" class="bit-btn">0</button></div>
                  <div class="bit-row"><span class="bit-label" style="opacity:0.7">Cin</span><button id="btnCin" class="bit-btn" style="border-style:dashed">0</button></div>
                </div>
                <div class="alu-core">
                  <select id="opSelect" class="op-select">
                    <option value="and">AND (00)</option>
                    <option value="or">OR (01)</option>
                    <option value="add" selected>SUM (10)</option>
                  </select>
                </div>
                <div class="alu-outputs">
                  <div class="bit-row"><span class="bit-out" id="resOut">0</span><span class="bit-label">Res</span></div>
                  <div class="bit-row" style="margin-top:28px"><span class="bit-out" id="coutOut" style="border-style:dashed">0</span><span class="bit-label" style="opacity:0.7">Cout</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- SLIDE 2 -->
        <div class="carousel-slide">
          <div class="slide-content">
            <h4>Il Problema delle Operazioni Inverse</h4>
            <p>L'ALU base è bloccata. Non sa calcolare il <code>NOR</code> logico e non sa sottrarre! E gli ingegneri si rifiutano di costruire un hardware nuovo di zecca solo per fare A - B.</p>
            <p>Sappiamo che per sottrarre ci basta usare l'addizionatore col <strong>Complemento a 2</strong>: capovolgere tutti i bit di B e aggiungere 1. Per "capovolgere" a comando, vengono piazzati due <strong>Multiplexer a 2 ingressi</strong> (i deviatori). Ognuno riceve il segnale intatto e quello passato da una porta <code>NOT</code>.</p>
            <div class="card amber" style="margin-top:16px;">
              <div class="card-title">Il miracolo di B-negate</div>
              <p style="font-size:13px;margin:4px 0 0">Quando ordini una Sottrazione, accendi il filo `B-negate`. Esso devia B nel NOT, ma soprattutto viaggia per forzare a 1 anche il <code>CarryIn</code> iniziale dell'addizionatore! La magia del complemento a 2 è servita.</p>
            </div>
            <img src="assets/alu/alu-nor.png" alt="ALU con Invert e Negate">
          </div>
        </div>

        <!-- SLIDE 3 -->
        <div class="carousel-slide">
          <div class="slide-content">
            <h4>Il Problema "Set Less Than" (SLT)</h4>
            <p>Vogliamo che l'hardware risponda a $A < B$. Se è vero 1, altrimenti 0. L'unico modo è calcolare di nascosto $A - B$: se esce negativo, A era minore. Ma il "segno negativo" viene calcolato <em>soltanto</em> dall'ultima ALU, quella del bit 31. Dobbiamo sdoppiare l'hardware!</p>
            
            <div style="display:flex; gap:24px; flex-wrap:wrap; margin-top:24px;">
              <div style="flex:1; min-width:250px;">
                <strong style="color:var(--text)">1. Prime 31 ALU (Bit 0-30)</strong>
                <p style="font-size:13px; color:var(--text)">Il quarto canale <strong>Less</strong> viene saldato a Terra (valore 0). In slt, i primi 31 bit sputano istantaneamente zero!</p>
                <img src="assets/alu/alu-31bit.png" alt="ALU 31 bit" style="margin-top:8px;">
              </div>
              <div style="flex:1; min-width:250px;">
                <strong style="color:var(--text)">2. La 32esima ALU (Bit Segno)</strong>
                <p style="font-size:13px; color:var(--text)">Ha un tubo di scappamento speciale <strong>Set</strong>: ruba il bit del segno direttamente dall'addizionatore.</p>
                <img src="assets/alu/alu-32bit.png" alt="ALU 32 bit" style="margin-top:8px;">
              </div>
            </div>
            
            <div class="callout blue" style="margin-top:24px;">
              <strong>La Cucitura (Set ➔ Less)</strong><br>
              Un lunghissimo cavo di rame prende il bit dal <strong>Set</strong> in cima (la 32esima ALU) e lo inietta brutalmente nel <strong>Less</strong> della primissima ALU (la ALU 0) in basso. Risultato? 31 zeri + il bit del segno.
            </div>
          </div>
        </div>

        <!-- SLIDE 4 -->
        <div class="carousel-slide">
          <div class="slide-content">
            <h4>Il Problema dello "Strabordamento" (Overflow)</h4>
            <p>Se sommiamo due numeri positivi enormi, il loro risultato potrebbe "bucare" la capacità dei 32 bit e invadere proprio l'ultimo bit (il bit del segno). Il computer crederebbe erroneamente di aver ottenuto un numero negativo! È l'<strong>Overflow</strong>.</p>
            <p>Gli ingegneri hardware hanno dimostrato un teorema infallibile: c'è Overflow <em>esclusivamente</em> quando il riporto che entra nell'ultimo bit (<code>CarryIn</code> 31) è diverso dal riporto che ne esce (<code>CarryOut</code> 31).</p>
            <p>Soluzione? Per lanciare un segnale "1" quando due fili sono diversi tra loro, basta usare una magnifica porta <strong>XOR</strong>!</p>
            <img src="assets/alu/overflow.png" alt="XOR per Overflow">
          </div>
        </div>

        <!-- SLIDE 5 -->
        <div class="carousel-slide">
          <div class="slide-content">
            <h4>Il Problema del Salto (L'ALU Definitiva)</h4>
            <p>Per le istruzioni come <code>beq</code> (salta se uguali), la CPU deve sapere istantaneamente se il calcolo ha prodotto Esattamente Zero. Tutti i 32 fili del risultato vengono infilati in un titanico <strong>NOR a 32 vie</strong> (un OR gigante + NOT). Solo se sono tutti zeri, il NOR sputa '1', accendendo l'allarme <strong>Zero</strong>!</p>
            <img src="assets/alu-completa.png" alt="ALU Completa" style="max-width:800px;">
            <div class="callout green" style="margin-top:24px;">
              <strong>La Scatola Nera</strong><br>
              D'ora in poi, l'intero labirinto di circuiti sparirà, diventando quel glorioso simbolo a "V" completo dei pin <code>Control</code>, <code>Result</code>, <code>Zero</code> e <code>Overflow</code>.
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</main>
</div>
'''

js_content = '''
<script>
  // Logica per il Carousel
  const titles = [
    "Fase 1: L'ALU Base",
    "Fase 2: Sottrazione e NOR",
    "Fase 3: Il Problema SLT",
    "Fase 4: L'Allarme Overflow",
    "Fase 5: L'ALU a 32 bit Completa"
  ];
  
  let currentSlide = 0;
  const maxSlides = 5;
  const container = document.getElementById('slidesContainer');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const indicator = document.getElementById('carouselIndicator');
  const title = document.getElementById('carouselTitle');

  function updateCarousel() {
    container.style.transform = `translateX(-${currentSlide * 20}%)`;
    indicator.textContent = `${currentSlide + 1} / ${maxSlides}`;
    title.textContent = titles[currentSlide];
    
    prevBtn.disabled = currentSlide === 0;
    nextBtn.disabled = currentSlide === maxSlides - 1;
  }

  prevBtn.addEventListener('click', () => {
    if (currentSlide > 0) {
      currentSlide--;
      updateCarousel();
    }
  });

  nextBtn.addEventListener('click', () => {
    if (currentSlide < maxSlides - 1) {
      currentSlide++;
      updateCarousel();
    }
  });

  // Logica per il Simulatore Interattivo (nella Slide 1)
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
    if (!btnA) return;
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

content = content[:start_idx] + new_content + js_content

# Riscriviamo la sidebar per mostrare solo S25
def update_sidebar(html):
    start_sb = html.find('<a class="nav-item" href="06_circuiti.html#s25">')
    end_sb = html.find('</nav>')
    
    if start_sb != -1:
        new_sb = '''<a class="nav-item" href="06_circuiti.html#s25">
    <div class="nav-dot"></div> L'Evoluzione dell'ALU
    <span class="nav-num">25</span>
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

# Replace sections 25-29 with just 25
idx_content = re.sub(
    r'\{ id: "s25", title: "Fase 1: ALU Base", file: "06_circuiti.html" \},.*?\{ id: "s29", title: "Fase 5: L\'ALU Completa", file: "06_circuiti.html" \},',
    '''{ id: "s25", title: "L'Evoluzione dell'ALU", file: "06_circuiti.html" },''',
    idx_content, flags=re.DOTALL
)

with open('index.html', 'w') as f:
    f.write(idx_content)

print("Riscrittura con Slider JS completata!")
