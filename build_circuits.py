import re

def create_decoder_svg():
    svg = ['<svg id="decoder-svg" viewBox="0 0 600 400" width="100%" height="400">']
    # Define SVG elements (gates, etc.)
    svg.append('''
    <defs>
      <g id="and-gate">
        <path d="M0,0 L15,0 A15,15 0 0,1 15,30 L0,30 Z" fill="var(--surface)" stroke="var(--blue)" stroke-width="2"/>
      </g>
      <g id="not-gate">
        <polygon points="0,0 20,10 0,20" fill="var(--surface)" stroke="var(--purple)" stroke-width="2"/>
        <circle cx="24" cy="10" r="4" fill="var(--surface)" stroke="var(--purple)" stroke-width="2"/>
      </g>
      <g id="dot">
        <circle cx="0" cy="0" r="4" fill="var(--text)"/>
      </g>
    </defs>
    ''')

    # Vertical line X coordinates
    vx = {'A': 100, '!A': 140, 'B': 180, '!B': 220, 'C': 260, '!C': 300}
    
    # Input labels and buttons will be HTML overlaid, but we draw wires.
    # Wires from buttons (x=40) to vertical lines
    svg.append(f'<path class="wire-A" d="M40,30 L100,30 L100,380" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<path class="wire-A" d="M100,30 L110,30" fill="none" stroke="var(--border)" stroke-width="2"/>') # To NOT gate
    svg.append(f'<use href="#not-gate" x="110" y="20"/>')
    svg.append(f'<path class="wire-!A" d="M138,30 L140,30 L140,380" fill="none" stroke="var(--border)" stroke-width="2"/>')
    
    svg.append(f'<path class="wire-B" d="M40,60 L180,60 L180,380" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<path class="wire-B" d="M180,60 L190,60" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate" x="190" y="50"/>')
    svg.append(f'<path class="wire-!B" d="M218,60 L220,60 L220,380" fill="none" stroke="var(--border)" stroke-width="2"/>')
    
    svg.append(f'<path class="wire-C" d="M40,90 L260,90 L260,380" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<path class="wire-C" d="M260,90 L270,90" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate" x="270" y="80"/>')
    svg.append(f'<path class="wire-!C" d="M298,90 L300,90 L300,380" fill="none" stroke="var(--border)" stroke-width="2"/>')
    
    # Dots for input splits
    svg.append(f'<use href="#dot" x="100" y="30"/>')
    svg.append(f'<use href="#dot" x="180" y="60"/>')
    svg.append(f'<use href="#dot" x="260" y="90"/>')
    
    # The 8 AND gates
    gate_y_start = 50
    spacing = 40
    
    # Truth table mapping D0-D7 to !A,!B,!C etc
    # 0 = !A!B!C, 1 = !A!BC, 2 = !A B !C, 3 = !A B C
    connections = [
        ['!A', '!B', '!C'], # D0
        ['!A', '!B', 'C'],  # D1
        ['!A', 'B', '!C'],  # D2
        ['!A', 'B', 'C'],   # D3
        ['A', '!B', '!C'],  # D4
        ['A', '!B', 'C'],   # D5
        ['A', 'B', '!C'],   # D6
        ['A', 'B', 'C']     # D7
    ]
    
    for i, conn in enumerate(connections):
        gy = gate_y_start + i * spacing
        # Draw the AND gate
        svg.append(f'<use href="#and-gate" class="gate-d{i}" x="400" y="{gy-15}"/>')
        # Output wire
        svg.append(f'<path class="wire-d{i}" d="M430,{gy} L480,{gy}" fill="none" stroke="var(--border)" stroke-width="2"/>')
        svg.append(f'<text class="text-d{i}" x="490" y="{gy+5}" fill="var(--text)" font-family="monospace">D{i}</text>')
        
        # Draw horizontal connections
        pin_y_offsets = [-8, 0, 8]
        for j, c in enumerate(conn):
            px = vx[c]
            py = gy + pin_y_offsets[j]
            # connection wire from vertical line to AND gate
            svg.append(f'<path class="wire-{c} wire-conn" d="M{px},{py} L400,{py}" fill="none" stroke="var(--border)" stroke-width="2"/>')
            # dot
            svg.append(f'<use href="#dot" x="{px}" y="{py}"/>')

    svg.append('</svg>')
    return '\n'.join(svg)

def create_mux_svg():
    svg = ['<svg id="mux-svg" viewBox="0 0 600 500" width="100%" height="500">']
    svg.append('''
    <defs>
      <g id="and-gate-mux">
        <path d="M0,0 L15,0 A15,15 0 0,1 15,30 L0,30 Z" fill="var(--surface)" stroke="var(--blue)" stroke-width="2"/>
      </g>
      <g id="or-gate-big">
        <!-- A very large OR gate to accept 8 inputs. We draw a custom path -->
        <path d="M0,0 Q20,100 0,200 L10,200 Q50,100 80,100 Q50,100 10,0 Z" fill="var(--surface)" stroke="var(--green)" stroke-width="2"/>
      </g>
      <g id="not-gate-mux">
        <polygon points="0,0 16,8 0,16" fill="var(--surface)" stroke="var(--purple)" stroke-width="2"/>
        <circle cx="19" cy="8" r="3" fill="var(--surface)" stroke="var(--purple)" stroke-width="2"/>
      </g>
      <g id="dot-mux">
        <circle cx="0" cy="0" r="3" fill="var(--text)"/>
      </g>
    </defs>
    ''')

    # Selectors A, B, C at bottom, but vertical lines go UP
    vx = {'A': 200, '!A': 230, 'B': 260, '!B': 290, 'C': 320, '!C': 350}
    
    # Wires from bottom (y=450)
    svg.append(f'<path class="wire-A-mux" d="M200,450 L200,30" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<path class="wire-A-mux" d="M200,430 L210,430" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate-mux" x="210" y="422"/>')
    svg.append(f'<path class="wire-!A-mux" d="M228,430 L230,430 L230,30" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot-mux" x="200" y="430"/>')

    svg.append(f'<path class="wire-B-mux" d="M260,450 L260,30" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<path class="wire-B-mux" d="M260,410 L270,410" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate-mux" x="270" y="402"/>')
    svg.append(f'<path class="wire-!B-mux" d="M288,410 L290,410 L290,30" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot-mux" x="260" y="410"/>')

    svg.append(f'<path class="wire-C-mux" d="M320,450 L320,30" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<path class="wire-C-mux" d="M320,390 L330,390" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate-mux" x="330" y="382"/>')
    svg.append(f'<path class="wire-!C-mux" d="M348,390 L350,390 L350,30" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot-mux" x="320" y="390"/>')

    # The 8 AND gates
    gate_y_start = 50
    spacing = 40
    
    connections = [
        ['!A', '!B', '!C'], # D0
        ['!A', '!B', 'C'],  # D1
        ['!A', 'B', '!C'],  # D2
        ['!A', 'B', 'C'],   # D3
        ['A', '!B', '!C'],  # D4
        ['A', '!B', 'C'],   # D5
        ['A', 'B', '!C'],   # D6
        ['A', 'B', 'C']     # D7
    ]
    
    # OR gate position
    or_x = 480
    or_y = 120
    
    svg.append(f'<use href="#or-gate-big" class="gate-or-mux" x="{or_x}" y="{or_y}"/>')
    # Final output
    svg.append(f'<path class="wire-out-mux" d="M560,220 L580,220" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<text class="text-out-mux" x="585" y="225" fill="var(--text)" font-family="monospace">F</text>')

    for i, conn in enumerate(connections):
        gy = gate_y_start + i * spacing
        # Draw the AND gate
        svg.append(f'<use href="#and-gate-mux" class="gate-and-m{i}" x="400" y="{gy-15}"/>')
        
        # D_i input wire
        svg.append(f'<path class="wire-din-{i}" d="M40,{gy-10} L400,{gy-10}" fill="none" stroke="var(--border)" stroke-width="2"/>')
        
        # Selectors connections
        pin_y_offsets = [-2, 6, 12]
        for j, c in enumerate(conn):
            px = vx[c]
            py = gy + pin_y_offsets[j]
            svg.append(f'<path class="wire-{c}-mux wire-conn" d="M{px},{py} L400,{py}" fill="none" stroke="var(--border)" stroke-width="2"/>')
            svg.append(f'<use href="#dot-mux" x="{px}" y="{py}"/>')

        # Connect AND output to OR gate
        # OR gate accepts inputs from y = 140 to y = 300 approximately
        or_pin_y = or_y + 20 + i * 22
        svg.append(f'<path class="wire-and-m{i}" d="M430,{gy} L450,{gy} L450,{or_pin_y} L{or_x + 10},{or_pin_y}" fill="none" stroke="var(--border)" stroke-width="2"/>')

    svg.append('</svg>')
    return '\n'.join(svg)


decoder_svg = create_decoder_svg()
mux_svg = create_mux_svg()

with open('06_circuiti.html', 'r') as f:
    ch6 = f.read()

# Replace S23 entirely
s23_start = '<!-- ══════════════ SEZIONE 23 ══════════════ -->'
s24_start = '<!-- ══════════════ SEZIONE 24 ══════════════ -->'
s23_content = f"""
  {s23_start}
  <section class="section" id="s23">
    <div class="section-header">
      <div class="section-num">23</div>
      <h2>I Mattoni <span class="accent">Logici</span></h2>
    </div>
    
    <p class="lead">Siamo scesi al Livello 0: qui il computer è solo un intricato sistema di tubature elettriche (0 Volt = Falso, 5 Volt = Vero). La matematica si costruisce "dirottando" questa elettricità tramite le Porte Logiche.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Circuiti Combinatori vs Sequenziali</h3>
    <p>In elettronica, i circuiti si dividono in due grandi famiglie:</p>
    <div class="card-grid cols2" style="margin-bottom:20px">
      <div class="card green">
        <div class="card-title">Circuiti Combinatori</div>
        <p style="font-size:13px;margin:4px 0 0">Non hanno memoria. L'uscita in questo esatto momento dipende <strong>esclusivamente</strong> da cosa c'è in ingresso in questo esatto momento. Come una calcolatrice semplice: digiti 2+2, esce 4. È istantaneo e "senza passato". (Es: ALU, Decoder, MUX).</p>
      </div>
      <div class="card amber">
        <div class="card-title">Circuiti Sequenziali</div>
        <p style="font-size:13px;margin:4px 0 0">Hanno memoria. L'uscita dipende dagli ingressi attuali <strong>e</strong> da quello che è successo in passato. Usano il segnale di <em>Clock</em> (il metronomo) per decidere <em>quando</em> aggiornare i propri dati. (Es: RAM, Registri, Flip-Flop).</p>
      </div>
    </div>

    <h3 style="font-size:16px;font-weight:500;margin:24px 0 12px">Le Porte Logiche Base</h3>
    <p>I circuiti combinatori si costruiscono incastrando miliardi di transistor configurati per formare queste "porte" elementari:</p>
    <div class="card-grid cols4" style="margin-bottom:24px">
      <div class="card" style="padding:15px;text-align:center"><strong style="color:var(--blue)">AND</strong><br><span style="font-size:12px">Esce 1 solo se TUTTI gli ingressi sono 1</span></div>
      <div class="card" style="padding:15px;text-align:center"><strong style="color:var(--green)">OR</strong><br><span style="font-size:12px">Esce 1 se ALMENO UN ingresso è 1</span></div>
      <div class="card" style="padding:15px;text-align:center"><strong style="color:var(--purple)">NOT</strong><br><span style="font-size:12px">Ribalta il segnale (1 diventa 0)</span></div>
      <div class="card" style="padding:15px;text-align:center"><strong style="color:var(--red)">XOR</strong><br><span style="font-size:12px">Esce 1 solo se gli ingressi sono DIVERSI</span></div>
    </div>

    <h3 style="font-size:16px;font-weight:500;margin:24px 0 12px">Il Decoder 3 a 8 (Il Cecchino)</h3>
    <p>Un Decoder riceve un numero binario in ingresso (es. 3 bit) e "accende" esattamente <strong>una sola</strong> linea di uscita (tra le $2^3 = 8$ possibili). È il cuore della memoria RAM, perché permette di selezionare la singola riga di celle desiderata partendo dall'indirizzo.</p>
    
    <div class="widget-container" style="position:relative;padding-left:10px;">
      <div class="widget-title">Simulatore Interattivo: Decoder</div>
      <p style="font-size:12px;color:var(--muted);margin-bottom:16px">Clicca sui bottoni A, B, C per cambiare il numero in ingresso. Osserva come il labirinto di porte NOT e AND accende un'unica uscita `D`.</p>
      
      <!-- Input buttons overlay for Decoder -->
      <div style="position:absolute; top: 110px; left: 20px; display:flex; flex-direction:column; gap:20px; z-index:10;">
        <div style="display:flex;align-items:center;gap:8px"><span class="bit-label" style="min-width:10px">A</span><button id="dec-btn-a" class="bit-btn dec-input">0</button></div>
        <div style="display:flex;align-items:center;gap:8px"><span class="bit-label" style="min-width:10px">B</span><button id="dec-btn-b" class="bit-btn dec-input">0</button></div>
        <div style="display:flex;align-items:center;gap:8px"><span class="bit-label" style="min-width:10px">C</span><button id="dec-btn-c" class="bit-btn dec-input">0</button></div>
      </div>
      
      {decoder_svg}
    </div>

    <h3 style="font-size:16px;font-weight:500;margin:32px 0 12px">Il Multiplexer 8 a 1 (Lo Scambio Ferroviario)</h3>
    <p>Il MUX (Multiplexer) fa l'esatto opposto: riceve 8 fili dati diversi, ma ne fa passare <strong>solo uno</strong> verso l'uscita. I fili di "Select" (A, B, C) decidono quale dei cancelli AND verrà sbloccato. È essenziale nella CPU per decidere, ad esempio, se all'ALU mandare il valore di un registro o una costante.</p>

    <div class="widget-container" style="position:relative;padding-left:10px;">
      <div class="widget-title">Simulatore Interattivo: Multiplexer</div>
      <p style="font-size:12px;color:var(--muted);margin-bottom:16px">Premi i tasti `Select` per decidere quale `Dato` far passare. Poi premi il bottone del Dato sbloccato per vedere il segnale scorrere fino alla grande porta OR finale.</p>
      
      <!-- Data buttons overlay -->
      <div style="position:absolute; top: 130px; left: 20px; display:flex; flex-direction:column; gap:28px; z-index:10;">
        <button id="mux-d0" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
        <button id="mux-d1" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
        <button id="mux-d2" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
        <button id="mux-d3" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
        <button id="mux-d4" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
        <button id="mux-d5" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
        <button id="mux-d6" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
        <button id="mux-d7" class="bit-btn mux-data" style="width:25px;height:25px;font-size:12px">0</button>
      </div>

      <!-- Select buttons overlay -->
      <div style="position:absolute; bottom: 30px; left: 220px; display:flex; gap:30px; z-index:10;">
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px"><button id="mux-sel-a" class="bit-btn mux-sel">0</button><span class="bit-label" style="min-width:10px">A</span></div>
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px"><button id="mux-sel-b" class="bit-btn mux-sel">0</button><span class="bit-label" style="min-width:10px">B</span></div>
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px"><button id="mux-sel-c" class="bit-btn mux-sel">0</button><span class="bit-label" style="min-width:10px">C</span></div>
      </div>
      
      {mux_svg}
    </div>

  </section>
"""

new_ch6 = ch6.split(s23_start)[0] + s23_content + '\n  ' + s24_start + ch6.split(s24_start)[1]

# Add Javascript logic for Decoder and MUX
js_logic = """
  // ----------------------------------------------------
  // DECODER LOGIC
  // ----------------------------------------------------
  const decBtnA = document.getElementById('dec-btn-a');
  const decBtnB = document.getElementById('dec-btn-b');
  const decBtnC = document.getElementById('dec-btn-c');

  let decA = 0, decB = 0, decC = 0;

  function updateDecoder() {
    const notA = decA === 0 ? 1 : 0;
    const notB = decB === 0 ? 1 : 0;
    const notC = decC === 0 ? 1 : 0;

    // Colora le linee verticali
    const colorWire = (selector, isOn) => {
      document.querySelectorAll(selector).forEach(el => {
        el.style.stroke = isOn ? 'var(--green)' : 'var(--border)';
      });
    };

    colorWire('.wire-A', decA); colorWire('.wire-!A', notA);
    colorWire('.wire-B', decB); colorWire('.wire-!B', notB);
    colorWire('.wire-C', decC); colorWire('.wire-!C', notC);

    // Calcola l'uscita delle porte AND
    const outD = [
      notA && notB && notC, // D0
      notA && notB && decC, // D1
      notA && decB && notC, // D2
      notA && decB && decC, // D3
      decA && notB && notC, // D4
      decA && notB && decC, // D5
      decA && decB && notC, // D6
      decA && decB && decC  // D7
    ];

    for(let i=0; i<8; i++) {
      const isOn = outD[i];
      document.querySelectorAll(`.wire-d${i}`).forEach(el => el.style.stroke = isOn ? 'var(--green)' : 'var(--border)');
      document.querySelectorAll(`.gate-d${i} path`).forEach(el => el.style.fill = isOn ? 'rgba(34,197,94,0.2)' : 'var(--surface)');
      document.querySelectorAll(`.text-d${i}`).forEach(el => {
        el.style.fill = isOn ? 'var(--green)' : 'var(--text)';
        el.style.fontWeight = isOn ? 'bold' : 'normal';
      });
    }
  }

  function toggleDec(btn, setter) {
    let v = parseInt(btn.textContent) === 0 ? 1 : 0;
    btn.textContent = v;
    if(v) btn.classList.add('active'); else btn.classList.remove('active');
    setter(v);
    updateDecoder();
  }

  decBtnA.addEventListener('click', () => toggleDec(decBtnA, v => decA = v));
  decBtnB.addEventListener('click', () => toggleDec(decBtnB, v => decB = v));
  decBtnC.addEventListener('click', () => toggleDec(decBtnC, v => decC = v));
  updateDecoder();

  // ----------------------------------------------------
  // MULTIPLEXER LOGIC
  // ----------------------------------------------------
  const muxBtnsD = [];
  let muxD = [0,0,0,0,0,0,0,0];
  for(let i=0; i<8; i++) {
    const btn = document.getElementById(`mux-d${i}`);
    muxBtnsD.push(btn);
    btn.addEventListener('click', () => {
      muxD[i] = muxD[i] === 0 ? 1 : 0;
      btn.textContent = muxD[i];
      if(muxD[i]) btn.classList.add('active'); else btn.classList.remove('active');
      updateMux();
    });
  }

  const muxBtnA = document.getElementById('mux-sel-a');
  const muxBtnB = document.getElementById('mux-sel-b');
  const muxBtnC = document.getElementById('mux-sel-c');
  let muxA = 0, muxB = 0, muxC = 0;

  function toggleMuxSel(btn, setter) {
    let v = parseInt(btn.textContent) === 0 ? 1 : 0;
    btn.textContent = v;
    if(v) btn.classList.add('active'); else btn.classList.remove('active');
    setter(v);
    updateMux();
  }
  muxBtnA.addEventListener('click', () => toggleMuxSel(muxBtnA, v => muxA = v));
  muxBtnB.addEventListener('click', () => toggleMuxSel(muxBtnB, v => muxB = v));
  muxBtnC.addEventListener('click', () => toggleMuxSel(muxBtnC, v => muxC = v));

  function updateMux() {
    const notA = muxA === 0 ? 1 : 0;
    const notB = muxB === 0 ? 1 : 0;
    const notC = muxC === 0 ? 1 : 0;

    const colorWireMux = (selector, isOn) => {
      document.querySelectorAll(selector).forEach(el => {
        el.style.stroke = isOn ? 'var(--purple)' : 'var(--border)';
      });
    };

    colorWireMux('.wire-A-mux', muxA); colorWireMux('.wire-!A-mux', notA);
    colorWireMux('.wire-B-mux', muxB); colorWireMux('.wire-!B-mux', notB);
    colorWireMux('.wire-C-mux', muxC); colorWireMux('.wire-!C-mux', notC);

    const selLines = [
      notA && notB && notC, // 0
      notA && notB && muxC, // 1
      notA && muxB && notC, // 2
      notA && muxB && muxC, // 3
      muxA && notB && notC, // 4
      muxA && notB && muxC, // 5
      muxA && muxB && notC, // 6
      muxA && muxB && muxC  // 7
    ];

    let orOut = 0;

    for(let i=0; i<8; i++) {
      const isSelected = selLines[i];
      const dataIn = muxD[i];
      const andOut = isSelected && dataIn;
      
      // Colora l'ingresso dati
      document.querySelectorAll(`.wire-din-${i}`).forEach(el => el.style.stroke = dataIn ? 'var(--amber)' : 'var(--border)');
      
      // Colora l'AND (si illumina se è selezionato e sta passando il dato)
      document.querySelectorAll(`.gate-and-m${i} path`).forEach(el => el.style.fill = andOut ? 'rgba(168,85,247,0.2)' : (isSelected ? 'rgba(255,255,255,0.05)' : 'var(--surface)'));
      document.querySelectorAll(`.gate-and-m${i} path`).forEach(el => el.style.stroke = isSelected ? 'var(--purple)' : 'var(--border)');

      // Colora l'uscita dell'AND
      document.querySelectorAll(`.wire-and-m${i}`).forEach(el => el.style.stroke = andOut ? 'var(--amber)' : 'var(--border)');

      if(andOut) orOut = 1;
    }

    // Colora OR e Final Output
    document.querySelectorAll(`.gate-or-mux path`).forEach(el => el.style.fill = orOut ? 'rgba(234,179,8,0.2)' : 'var(--surface)');
    document.querySelectorAll(`.wire-out-mux`).forEach(el => el.style.stroke = orOut ? 'var(--amber)' : 'var(--border)');
    document.querySelectorAll(`.text-out-mux`).forEach(el => {
      el.style.fill = orOut ? 'var(--amber)' : 'var(--text)';
      el.style.fontWeight = orOut ? 'bold' : 'normal';
    });
  }
  updateMux();
"""

new_ch6 = new_ch6.replace('</script>\n\n<script src="shared.js">', js_logic + '\n</script>\n\n<script src="shared.js">')

with open('06_circuiti.html', 'w') as f:
    f.write(new_ch6)

print("Widgets created successfully!")
