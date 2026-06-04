import re

def create_decoder_svg():
    svg = ['<svg id="decoder-svg" viewBox="0 0 600 400" width="100%" height="400">']
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

    vx = {'notA': 140, 'A': 180, 'notB': 220, 'B': 260, 'notC': 300, 'C': 340}

    # Draw vertical lines
    for key, x in vx.items():
        svg.append(f'<path class="wire-{key}" d="M{x},30 L{x},360" fill="none" stroke="var(--border)" stroke-width="2"/>')

    # A (y=100)
    svg.append(f'<path class="wire-A" d="M20,100 L60,100" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="60" y="100"/>')
    svg.append(f'<path class="wire-A" d="M60,100 L60,90 L180,90" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="180" y="90"/>')
    svg.append(f'<path class="wire-A" d="M60,100 L100,100" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate" x="100" y="90"/>')
    svg.append(f'<path class="wire-notA" d="M128,100 L140,100" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="140" y="100"/>')

    # B (y=180)
    svg.append(f'<path class="wire-B" d="M20,180 L60,180" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="60" y="180"/>')
    svg.append(f'<path class="wire-B" d="M60,180 L60,170 L260,170" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="260" y="170"/>')
    svg.append(f'<path class="wire-B" d="M60,180 L100,180" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate" x="100" y="170"/>')
    svg.append(f'<path class="wire-notB" d="M128,180 L220,180" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="220" y="180"/>')

    # C (y=260)
    svg.append(f'<path class="wire-C" d="M20,260 L60,260" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="60" y="260"/>')
    svg.append(f'<path class="wire-C" d="M60,260 L60,250 L340,250" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="340" y="250"/>')
    svg.append(f'<path class="wire-C" d="M60,260 L100,260" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate" x="100" y="250"/>')
    svg.append(f'<path class="wire-notC" d="M128,260 L300,260" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot" x="300" y="260"/>')

    connections = [
        ['notA', 'notB', 'notC'], # D0
        ['notA', 'notB', 'C'],    # D1
        ['notA', 'B', 'notC'],    # D2
        ['notA', 'B', 'C'],       # D3
        ['A', 'notB', 'notC'],    # D4
        ['A', 'notB', 'C'],       # D5
        ['A', 'B', 'notC'],       # D6
        ['A', 'B', 'C']           # D7
    ]

    gate_y_centers = [40, 80, 120, 160, 200, 240, 280, 320]
    for i, gy in enumerate(gate_y_centers):
        svg.append(f'<use href="#and-gate" class="gate-d{i}" x="420" y="{gy-15}"/>')
        svg.append(f'<path class="wire-d{i}" d="M450,{gy} L500,{gy}" fill="none" stroke="var(--border)" stroke-width="2"/>')
        svg.append(f'<text class="text-d{i}" x="510" y="{gy+5}" fill="var(--text)" font-family="monospace">D{i}</text>')

        conn = connections[i]
        pin_y = [gy-8, gy, gy+8]
        for j, c in enumerate(conn):
            px = vx[c]
            py = pin_y[j]
            svg.append(f'<path class="wire-{c} wire-conn" d="M{px},{py} L420,{py}" fill="none" stroke="var(--border)" stroke-width="2"/>')
            svg.append(f'<use href="#dot" x="{px}" y="{py}"/>')

    svg.append('</svg>')
    return '\n'.join(svg)

def create_mux_svg():
    svg = ['<svg id="mux-svg" viewBox="0 0 600 450" width="100%" height="450">']
    svg.append('''
    <defs>
      <g id="and-gate-mux">
        <path d="M0,0 L15,0 A15,15 0 0,1 15,30 L0,30 Z" fill="var(--surface)" stroke="var(--blue)" stroke-width="2"/>
      </g>
      <g id="or-gate-giant">
        <path d="M0,0 Q30,175 0,350 L20,350 Q80,175 100,175 Q80,175 20,0 Z" fill="var(--surface)" stroke="var(--green)" stroke-width="2"/>
      </g>
      <g id="not-gate-up">
        <polygon points="0,20 10,0 20,20" fill="var(--surface)" stroke="var(--purple)" stroke-width="2"/>
        <circle cx="10" cy="-4" r="4" fill="var(--surface)" stroke="var(--purple)" stroke-width="2"/>
      </g>
      <g id="dot-mux">
        <circle cx="0" cy="0" r="3" fill="var(--text)"/>
      </g>
    </defs>
    ''')

    vx = {'A': 200, 'notA': 220, 'B': 250, 'notB': 270, 'C': 300, 'notC': 320}

    for key, x in vx.items():
        svg.append(f'<path class="wire-{key}-mux" d="M{x},30 L{x},400" fill="none" stroke="var(--border)" stroke-width="2"/>')

    # A (x=200)
    svg.append(f'<path class="wire-A-mux" d="M200,430 L200,400" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot-mux" x="200" y="410"/>')
    svg.append(f'<path class="wire-A-mux" d="M200,410 L220,410 L220,390" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate-up" x="210" y="370"/>')
    svg.append(f'<path class="wire-notA-mux" d="M220,362 L220,400" fill="none" stroke="var(--border)" stroke-width="2"/>')

    # B (x=250)
    svg.append(f'<path class="wire-B-mux" d="M250,430 L250,400" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot-mux" x="250" y="410"/>')
    svg.append(f'<path class="wire-B-mux" d="M250,410 L270,410 L270,390" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate-up" x="260" y="370"/>')
    svg.append(f'<path class="wire-notB-mux" d="M270,362 L270,400" fill="none" stroke="var(--border)" stroke-width="2"/>')

    # C (x=300)
    svg.append(f'<path class="wire-C-mux" d="M300,430 L300,400" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#dot-mux" x="300" y="410"/>')
    svg.append(f'<path class="wire-C-mux" d="M300,410 L320,410 L320,390" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<use href="#not-gate-up" x="310" y="370"/>')
    svg.append(f'<path class="wire-notC-mux" d="M320,362 L320,400" fill="none" stroke="var(--border)" stroke-width="2"/>')

    connections = [
        ['notA', 'notB', 'notC'], # D0
        ['notA', 'notB', 'C'],    # D1
        ['notA', 'B', 'notC'],    # D2
        ['notA', 'B', 'C'],       # D3
        ['A', 'notB', 'notC'],    # D4
        ['A', 'notB', 'C'],       # D5
        ['A', 'B', 'notC'],       # D6
        ['A', 'B', 'C']           # D7
    ]

    gate_y_centers = [40, 85, 130, 175, 220, 265, 310, 355]
    or_x = 450
    or_y = 20
    or_back_curve = [470, 480, 485, 488, 488, 485, 480, 470]

    svg.append(f'<use href="#or-gate-giant" class="gate-or-mux" x="{or_x}" y="{or_y}"/>')
    svg.append(f'<path class="wire-out-mux" d="M550,195 L580,195" fill="none" stroke="var(--border)" stroke-width="2"/>')
    svg.append(f'<text class="text-out-mux" x="585" y="200" fill="var(--text)" font-family="monospace">F</text>')

    for i, gy in enumerate(gate_y_centers):
        svg.append(f'<use href="#and-gate-mux" class="gate-and-m{i}" x="370" y="{gy-15}"/>')
        svg.append(f'<path class="wire-din-{i}" d="M40,{gy-12} L370,{gy-12}" fill="none" stroke="var(--border)" stroke-width="2"/>')

        conn = connections[i]
        pin_y = [gy-4, gy+4, gy+12]
        for j, c in enumerate(conn):
            px = vx[c]
            py = pin_y[j]
            svg.append(f'<path class="wire-{c}-mux wire-conn" d="M{px},{py} L370,{py}" fill="none" stroke="var(--border)" stroke-width="2"/>')
            svg.append(f'<use href="#dot-mux" x="{px}" y="{py}"/>')

        # output of AND to OR
        ox = or_back_curve[i]
        svg.append(f'<path class="wire-and-m{i}" d="M400,{gy} L{ox},{gy}" fill="none" stroke="var(--border)" stroke-width="2"/>')

    svg.append('</svg>')
    return '\n'.join(svg)

# Replace in file
with open('06_circuiti.html', 'r') as f:
    content = f.read()

# Replace SVG for decoder
dec_start = content.find('<svg id="decoder-svg"')
dec_end = content.find('</svg>', dec_start) + 6
content = content[:dec_start] + create_decoder_svg() + content[dec_end:]

# Replace SVG for mux
mux_start = content.find('<svg id="mux-svg"')
mux_end = content.find('</svg>', mux_start) + 6
content = content[:mux_start] + create_mux_svg() + content[mux_end:]

# Fix Javascript classes: replace !A with notA etc
# Already done in logic, but let's make sure the JS block matches exactly
js_start = content.find('<script>\n  // ----------------------------------------------------')
js_block = """<script>
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

    const colorWire = (selector, isOn) => {
      document.querySelectorAll(selector).forEach(el => {
        el.style.stroke = isOn ? 'var(--green)' : 'var(--border)';
      });
    };

    colorWire('.wire-A', decA); colorWire('.wire-notA', notA);
    colorWire('.wire-B', decB); colorWire('.wire-notB', notB);
    colorWire('.wire-C', decC); colorWire('.wire-notC', notC);

    const outD = [
      notA && notB && notC,
      notA && notB && decC,
      notA && decB && notC,
      notA && decB && decC,
      decA && notB && notC,
      decA && notB && decC,
      decA && decB && notC,
      decA && decB && decC
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
    if(btn) {
      muxBtnsD.push(btn);
      btn.addEventListener('click', () => {
        muxD[i] = muxD[i] === 0 ? 1 : 0;
        btn.textContent = muxD[i];
        if(muxD[i]) btn.classList.add('active'); else btn.classList.remove('active');
        updateMux();
      });
    }
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

    colorWireMux('.wire-A-mux', muxA); colorWireMux('.wire-notA-mux', notA);
    colorWireMux('.wire-B-mux', muxB); colorWireMux('.wire-notB-mux', notB);
    colorWireMux('.wire-C-mux', muxC); colorWireMux('.wire-notC-mux', notC);

    const selLines = [
      notA && notB && notC,
      notA && notB && muxC,
      notA && muxB && notC,
      notA && muxB && muxC,
      muxA && notB && notC,
      muxA && notB && muxC,
      muxA && muxB && notC,
      muxA && muxB && muxC
    ];

    let orOut = 0;

    for(let i=0; i<8; i++) {
      const isSelected = selLines[i];
      const dataIn = muxD[i];
      const andOut = isSelected && dataIn;
      
      document.querySelectorAll(`.wire-din-${i}`).forEach(el => el.style.stroke = dataIn ? 'var(--amber)' : 'var(--border)');
      
      document.querySelectorAll(`.gate-and-m${i} path`).forEach(el => {
        el.style.fill = andOut ? 'rgba(168,85,247,0.2)' : (isSelected ? 'rgba(255,255,255,0.05)' : 'var(--surface)');
        el.style.stroke = isSelected ? 'var(--purple)' : 'var(--border)';
      });

      document.querySelectorAll(`.wire-and-m${i}`).forEach(el => el.style.stroke = andOut ? 'var(--amber)' : 'var(--border)');

      if(andOut) orOut = 1;
    }

    document.querySelectorAll(`.gate-or-mux path`).forEach(el => el.style.fill = orOut ? 'rgba(234,179,8,0.2)' : 'var(--surface)');
    document.querySelectorAll(`.wire-out-mux`).forEach(el => el.style.stroke = orOut ? 'var(--amber)' : 'var(--border)');
    document.querySelectorAll(`.text-out-mux`).forEach(el => {
      el.style.fill = orOut ? 'var(--amber)' : 'var(--text)';
      el.style.fontWeight = orOut ? 'bold' : 'normal';
    });
  }
  updateMux();
"""

js_end = content.find('  // ----------------------------------------------------', js_start + 100)
# We will just replace from `<script>\n  // -----` to the ALU 1-BIT logic which we MUST NOT OVERWRITE
# Wait, my `js_logic` block above only contains Decoder and Multiplexer logic.
# The `updateLogic` for ALU 1-bit is further down or above?
# Let's check where `updateLogic` is in the original content.
