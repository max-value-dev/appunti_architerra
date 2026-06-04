import re

header = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RISC-V — Fondamenti Hardware</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="layout">

<!-- SIDEBAR -->
<nav class="sidebar">
  <a class="sidebar-title" href="index.html">
    RISC-V Fondamentali
    <span>Guida completa</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s01">
    <div class="nav-dot"></div> Il Motore del Computer
    <span class="nav-num">01</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s02">
    <div class="nav-dot"></div> Il Lavoro Quotidiano
    <span class="nav-num">02</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s03">
    <div class="nav-dot"></div> L'Organizzazione dello Spazio
    <span class="nav-num">03</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s04">
    <div class="nav-dot"></div> 32 vs 64 bit e Little Endian
    <span class="nav-num">04</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s05">
    <div class="nav-dot"></div> Bus e Allineamento
    <span class="nav-num">05</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s06">
    <div class="nav-dot"></div> I Processi nella RAM
    <span class="nav-num">06</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s07">
    <div class="nav-dot"></div> Software e Traduzione
    <span class="nav-num">07</span>
  </a>
  <a class="nav-item" href="01_fondamenti.html#s08">
    <div class="nav-dot"></div> L'Anatomia di un'istruzione
    <span class="nav-num">08</span>
  </a>
</nav>

<!-- MAIN -->
<main class="main">

  <!-- HERO -->
  <div class="hero">
    <div class="hero-tag">CAPITOLO 01 — FONDAMENTI</div>
    <h1>Il Grande Viaggio<br><em>Dalla Cucina all'Hardware</em></h1>
    <p>Una narrazione completa dei fondamenti dell'architettura dei calcolatori: dal ciclo di clock, alla gerarchia della memoria, fino ai formati binari delle istruzioni a 32 bit.</p>
  </div>
"""

# HTML sections based on Riassunti 1-9
html_content = """
  <!-- ══════════════ SEZIONE 01 ══════════════ -->
  <section class="section" id="s01">
    <div class="section-header">
      <div class="section-num">01</div>
      <h2>Il Motore del <span class="accent">Computer</span></h2>
    </div>
    
    <p class="lead">Abbiamo usato la metafora della cucina per rendere visibili concetti invisibili: la CPU è la nostra brigata di cucina, la RAM è il frigorifero e il Disco Fisso è il supermercato.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Clock, GHz e Core</h3>
    <p>Tutto parte da un componente inerte di silicio che ha bisogno di un ritmo per muoversi.</p>
    <div class="card-grid cols3">
      <div class="card blue">
        <div class="card-title">Il Clock (Il metronomo)</div>
        <p style="font-size:13px;margin:4px 0 0">È il battito cardiaco del sistema. Emette impulsi elettrici regolari (Tick) che spingono i dati attraverso i circuiti. Se si ferma, il PC si congela.</p>
      </div>
      <div class="card green">
        <div class="card-title">I Gigahertz (GHz)</div>
        <p style="font-size:13px;margin:4px 0 0">Misurano la velocità di questo metronomo. Un processore a 3.0 GHz compie 3 miliardi di "battiti" al secondo.</p>
      </div>
      <div class="card amber">
        <div class="card-title">I Core (I cuochi)</div>
        <p style="font-size:13px;margin:4px 0 0">Sono i "cervelli" indipendenti dentro il processore. Un Multi-Core permette di eseguire più compiti in parallelo (vero multitasking).</p>
      </div>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 02 ══════════════ -->
  <section class="section" id="s02">
    <div class="section-header">
      <div class="section-num">02</div>
      <h2>Il Lavoro Quotidiano: <span class="accent">Ciclo e Registri</span></h2>
    </div>

    <p class="lead">Ad ogni battito di metronomo, ogni singolo Core esegue una coreografia perfetta divisa in tre fasi: Fetch (Recupero), Decode (Decodifica) ed Execute (Esecuzione).</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">I Registri (Il bancone della cucina)</h3>
    <p>Per farlo senza impazzire, la CPU usa dei minuscoli banchi di memoria interni chiamati <strong>Registri</strong>:</p>
    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>PC (Program Counter):</strong> È il segnalibro. Ricorda quale riga di codice deve essere eseguita subito dopo.</li>
      <li><strong>MAR (Memory Address Register):</strong> Il fattorino degli indirizzi. Il PC gli passa il numero (l'indirizzo in RAM) di dove si trova il dato da recuperare.</li>
      <li><strong>MDR (Memory Data Register):</strong> Il cesto della spesa. I dati presi dalla RAM arrivano fisicamente qui dentro.</li>
      <li><strong>CIR (Current Instruction Register):</strong> Il tagliere. L'istruzione grezza passa dall'MDR al CIR affinché la CPU la decodifichi e la esegua.</li>
    </ul>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">L'Assembly RISC-V: Il linguaggio della macchina</h3>
    <p>Tutte queste operazioni fisiche sono controllate dal codice Assembly (come il RISC-V). Questo linguaggio mette a disposizione del programmatore 32 registri visibili sul bancone per fare i calcoli.</p>
    <div class="card-grid cols3">
      <div class="card teal">
        <div class="card-title">Load (lw)</div>
        <p style="font-size:13px;margin:4px 0 0">Il processore usa MAR e MDR per prendere dati dalla RAM.</p>
      </div>
      <div class="card purple">
        <div class="card-title">Calcolo (add)</div>
        <p style="font-size:13px;margin:4px 0 0">Il processore usa la calcolatrice interna (ALU) sui dati presenti sul bancone.</p>
      </div>
      <div class="card red">
        <div class="card-title">Controllo (beq)</div>
        <p style="font-size:13px;margin:4px 0 0">Il processore devia il flusso modificando il PC per fargli saltare righe di codice.</p>
      </div>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 03 ══════════════ -->
  <section class="section" id="s03">
    <div class="section-header">
      <div class="section-num">03</div>
      <h2>L'Organizzazione <span class="accent">dello Spazio</span></h2>
    </div>

    <p class="lead">Per far funzionare un computer senza colli di bottiglia, i dati vengono organizzati su diversi livelli fisici, dal più piccolo e veloce al più capiente e lento.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">La Gerarchia della Memoria</h3>
    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>0. Numeri immediati:</strong> Massima velocità (viaggiano a cavallo dell'istruzione).</li>
      <li><strong>1. Registri CPU (< 1 ns):</strong> Il tagliere. L'unico posto dove i dati possono essere manipolati.</li>
      <li><strong>2. Cache L1, L2, L3 (2-15 ns):</strong> La dispensa sotto il bancone. Memoria ultra-veloce saldata sulla CPU.</li>
      <li><strong>3. RAM (~50 ns):</strong> La cella frigorifera. Il magazzino diviso logicamente in Stack e Heap.</li>
      <li><strong>4. Disco Fisso / SSD (> 50k ns):</strong> Il supermercato. Spazio immenso ma troppo lento per la CPU.</li>
    </ul>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Stack, Heap e il Collo di Bottiglia</h3>
    <div class="card-grid cols2" style="margin-bottom:20px">
      <div class="card blue">
        <div class="card-title">Lo Stack (La Pila LIFO)</div>
        <p style="font-size:13px;margin:4px 0 0">Gestita dal registro SP, cresce verso il basso. Serve per le chiamate a funzione e variabili temporanee. Rischio: Stack Overflow.</p>
      </div>
      <div class="card amber">
        <div class="card-title">L'Heap (Il Magazzino)</div>
        <p style="font-size:13px;margin:4px 0 0">Porzione elastica per dati pesanti e persistenti. Richiede allocazione manuale e rischia il Memory Leak.</p>
      </div>
    </div>
    
    <div class="callout red">
      <strong>Il Thrashing:</strong> Se carichi troppi dati nell'Heap, la RAM si riempie. Il Sistema Operativo inizia a fare "Swap" (copiare pezzi su Disco), paralizzando il PC.
    </div>

    <h3 style="font-size:16px;font-weight:500;margin:24px 0 12px">Il Principio Load / Store e l'Architettura</h3>
    <p>Nella memoria RAM non avviene nessun calcolo. L'ALU lavora solo sui Registri. Da qui nascono due filosofie costruttive opposte (ISA):</p>
    <div class="card-grid cols2">
      <div class="card green">
        <div class="card-title">RISC (Reduced Instruction Set Computer)</div>
        <p style="font-size:13px;margin:4px 0 0">Esempi: RISC-V, ARM (Apple Silicon). Vocabolario ridotto, comandi semplici. Hardware fulmineo e freddo. Obbligo di usare Load/Store espliciti.</p>
      </div>
      <div class="card purple">
        <div class="card-title">CISC (Complex Instruction Set Computer)</div>
        <p style="font-size:13px;margin:4px 0 0">Esempi: Intel, AMD. Vocabolario ricco. Permette operazioni direttamente su RAM, ma costringe la CPU ad avere un Traduttore Hardware interno (Decoder) che scalda e consuma molto.</p>
      </div>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 04 ══════════════ -->
  <section class="section" id="s04">
    <div class="section-header">
      <div class="section-num">04</div>
      <h2>32 vs 64 bit e <span class="accent">Little Endian</span></h2>
    </div>

    <p class="lead">Cosa significa veramente avere un processore a 64 bit? Non è una misura di velocità, ma della "larghezza" fisica dei componenti interni.</p>

    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>Grandezza Registri:</strong> Un'ALU a 64 bit calcola numeri giganteschi in un colpo solo.</li>
      <li><strong>Limite RAM:</strong> A 32 bit, le combinazioni si fermano a 4 Miliardi (massimo 4 GB di RAM indirizzabili). A 64 bit esplodono a 18,4 Exabyte (memoria virtualmente infinita).</li>
    </ul>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Anatomia della RAM: celle da 8 bit</h3>
    <p>Nonostante la CPU lavori a 64 bit, la RAM è sempre organizzata in celle da <strong>8 bit (1 Byte)</strong>. Per leggere 64 bit, la CPU deve prelevare il contenuto di 8 celle consecutive.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Little Endian e la fisica dello Stack</h3>
    <p>Dato che un numero grande dev'essere fatto a fette da 1 byte, in che ordine si salva? Usiamo il <strong>Little Endian</strong>: il pezzo meno significativo va nell'indirizzo più piccolo (l'estremità piccola per prima). Questo permette alla CPU di iniziare a calcolare partendo subito dalle unità.</p>

    <div class="callout amber" style="margin-top:16px">
      <strong>L'enigma dello Stack: cresce verso il basso o si scrive verso l'alto?</strong><br>
      Entrambe! La RAM è "cieca". Lo Stack Pointer (Logica CPU) scende verso il basso per <em>fare spazio</em>. Ma quando la CPU dice "scrivi un blocco a 32 bit da qui", la RAM (Fisica) scrive i 4 byte <em>verso l'alto</em> secondo la regola Little Endian.
    </div>
  </section>

  <!-- ══════════════ SEZIONE 05 ══════════════ -->
  <section class="section" id="s05">
    <div class="section-header">
      <div class="section-num">05</div>
      <h2>Bus di Sistema e <span class="accent">Allineamento</span></h2>
    </div>

    <p class="lead">Per risolvere il mistero di come la CPU possa leggere 8 celle diverse in un colpo solo senza rallentare, dobbiamo guardare i collegamenti fisici: il Bus.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Le Tre Autostrade</h3>
    <div class="card-grid cols3">
      <div class="card teal">
        <div class="card-title">Address Bus</div>
        <p style="font-size:13px;margin:4px 0 0">A senso unico dalla CPU alla RAM. Trasporta il numero dello "scaffale". Largo 32 o 64 bit.</p>
      </div>
      <div class="card red">
        <div class="card-title">Control Bus</div>
        <p style="font-size:13px;margin:4px 0 0">Il semaforo. Accende un filo specifico (es. Write Enable) per dire alla RAM se leggere o scrivere.</p>
      </div>
      <div class="card blue">
        <div class="card-title">Data Bus</div>
        <p style="font-size:13px;margin:4px 0 0">Autostrada a doppio senso per trasportare il blocco di dati. Largo 32, 64 o 128 bit.</p>
      </div>
    </div>

    <p style="margin-top:16px; font-size:14px">Quando usi un'istruzione come <code>sw</code> (Store), la RAM non ha idea di cosa sia RISC-V. La CPU attiva l'Address Bus con l'indirizzo, mette il dato sul Data Bus e accende il segnale di "Scrittura" sul Control Bus. La RAM esegue ciecamente l'operazione sui pin accesi.</p>

    <h3 style="font-size:16px;font-weight:500;margin:24px 0 12px">L'Allineamento in Memoria</h3>
    <p>Il "camion" del Data Bus è largo (es. 4 Byte), ma <strong>può parcheggiare solo a indirizzi multipli della sua dimensione</strong> (es. 0, 4, 8, 12).</p>
    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>Lettura Allineata (Verde):</strong> Leggi 4 Byte partendo da 0. Il Bus prende il blocco 0-3 in 1 ciclo di clock. Perfetto.</li>
      <li><strong>Lettura Non Allineata (Rossa):</strong> Leggi 4 Byte partendo da 1. Il Bus deve fare due viaggi (blocco 0-3 e blocco 4-7) e scartare le eccedenze. Prestazioni dimezzate!</li>
    </ul>
    <p><em>Regola d'oro:</em> Le Word (4 byte) vanno salvate sempre partendo da indirizzi multipli di 4.</p>
  </section>

  <!-- ══════════════ SEZIONE 06 ══════════════ -->
  <section class="section" id="s06">
    <div class="section-header">
      <div class="section-num">06</div>
      <h2>I Processi <span class="accent">nella RAM</span></h2>
    </div>

    <p class="lead">Quando fai doppio clic su un file eseguibile, il Sistema Operativo gli assegna una "stanza virtuale" della RAM, divisa rigorosamente in 4 quartieri (Segmenti).</p>

    <div class="card-grid cols2">
      <div class="card green">
        <div class="card-title">1. Segmento di Testo (.text)</div>
        <p style="font-size:13px;margin:4px 0 0">È il "Libro delle Ricette". Contiene il codice eseguibile puro (istruzioni binarie). È bloccato in <strong>Sola Lettura</strong> per motivi di sicurezza.</p>
      </div>
      <div class="card amber">
        <div class="card-title">2. Segmento Dati (.data / .bss)</div>
        <p style="font-size:13px;margin:4px 0 0">Contiene variabili globali e costanti. Esistono per tutta la vita del programma e mantengono indirizzi fissi.</p>
      </div>
      <div class="card blue">
        <div class="card-title">3. Heap (Memoria Dinamica)</div>
        <p style="font-size:13px;margin:4px 0 0">Spazio enorme per dati creati "al volo" (es. foto pesanti caricate con `malloc`). Cresce verso l'alto.</p>
      </div>
      <div class="card purple">
        <div class="card-title">4. Stack (Pila di Esecuzione)</div>
        <p style="font-size:13px;margin:4px 0 0">Appeso al "soffitto", cresce verso il basso. Contiene Record di Attivazione (indirizzi di ritorno, variabili locali). Se si scontra con l'Heap, avviene un disastro (Stack Overflow).</p>
      </div>
    </div>
  </section>

  <!-- ══════════════ SEZIONE 07 ══════════════ -->
  <section class="section" id="s07">
    <div class="section-header">
      <div class="section-num">07</div>
      <h2>Software e <span class="accent">Traduzione</span></h2>
    </div>

    <p class="lead">Prima che la CPU possa calcolare qualcosa, il codice umano deve essere tradotto nella lingua dei circuiti: zeri e uni.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">La Catena di Montaggio</h3>
    <ul style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><strong>Compilatore:</strong> Traduce il codice C/Java/ecc in linguaggio Assembly (il vocabolario della CPU).</li>
      <li><strong>Assemblatore:</strong> Traduce l'Assembly in codice macchina puro (file oggetto, 0 e 1).</li>
      <li><strong>Linker:</strong> Unisce tutti i moduli per creare un singolo file eseguibile (.exe o ELF).</li>
    </ul>

    <div class="callout blue" style="margin-top:16px">
      <strong>L'Illusione delle Variabili (La rivelazione finale)</strong><br>
      Alla CPU non importa nulla dei "tipi di dato" (int, float, char) né dei "nomi" delle variabili. Nel codice macchina, il <code>.text</code> contiene solo <strong>Verbi</strong> (istruzioni) incanalati via Opcode, e i <strong>Bersagli</strong> sono sempre e solo Indirizzi di Memoria nel <code>.data</code> o offset dallo Stack Pointer. Le "variabili" sono una comodità umana!
    </div>
  </section>

  <!-- ══════════════ SEZIONE 08 ══════════════ -->
  <section class="section" id="s08">
    <div class="section-header">
      <div class="section-num">08</div>
      <h2>Anatomia di <span class="accent">un'istruzione a 32 bit</span></h2>
    </div>

    <p class="lead">Nel mondo RISC-V, ogni singola istruzione deve essere lunga ESATTAMENTE 32 bit. Non un bit in più, non uno in meno. Questo permette al Decoder di sapere sempre dove tagliare.</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">I Formati Macchina</h3>
    <p>Come facciamo a dire alla CPU "Somma registro 1 e 2" con soli 32 bit? Usando dei "settori" specifici:</p>

    <div class="card-grid cols2">
      <div class="card green">
        <div class="card-title">Formato R (Register)</div>
        <p style="font-size:13px;margin:4px 0 0">Usato se tutti gli ingredienti sono già nei registri (es: <code>add x5, x6, x7</code>). <br>Ha settori per <code>Opcode</code> (7 bit), <code>rd</code>, <code>funct3</code>, <code>rs1</code>, <code>rs2</code>, <code>funct7</code>.<br>
        <em>Nota: i registri usano campi da 5 bit perché $2^5 = 32$ registri!</em></p>
      </div>
      <div class="card amber">
        <div class="card-title">Formato I (Immediate)</div>
        <p style="font-size:13px;margin:4px 0 0">Unisce lo spazio di rs2 e funct7 per creare un settore da <strong>12 bit</strong>, permettendoti di sommare un numero fisso (es: <code>addi x5, x6, 10</code>) o di avere un <strong>Offset</strong> per leggere in RAM.</p>
      </div>
    </div>
    
    <p style="margin-top:16px;font-size:14px">Esistono 6 formati (R, I, S, B, U, J), ognuno sposta i "muri interni" dei 32 bit a seconda delle esigenze (ad esempio, J usa 20 bit per gli indirizzi lunghi di un Jump).</p>

    <h3 style="font-size:16px;font-weight:500;margin:20px 0 12px">Il grande limite dei 32 bit</h3>
    <p>Poiché l'istruzione è chiusa in 32 bit e l'Opcode/Registri ne occupano una parte, <strong>è fisicamente impossibile</strong> caricare in un registro un indirizzo a 32 bit in una sola mossa. Si fa "a rate":</p>
    <ol style="font-size:14px;line-height:1.6;color:var(--text);margin-bottom:20px">
      <li><code>lui</code> (Load Upper Immediate): Carica i 20 bit alti (Formato U).</li>
      <li><code>addi</code> (Add Immediate): Somma i 12 bit bassi (Formato I).</li>
    </ol>
    <p>L'Assemblatore fa questo calcolo al posto nostro, mettendoci a disposizione la pseudo-istruzione <code>la</code> (Load Address)! Inoltre, nei formati I/S, l'offset per la memoria è limitato a 12 bit, limitando il "raggio d'azione" del puntatore a circa $\pm 2$ KB.</p>
  </section>

"""

footer = """</main>
</div>

<script src="shared.js"></script>
</body>
</html>
"""

with open('01_fondamenti.html', 'w') as f:
    f.write(header + html_content + footer)

print("Generated 01_fondamenti.html successfully!")
