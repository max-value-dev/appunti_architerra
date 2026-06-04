import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

# Trova la fine di S25 (cioè prima della chiusura del tag </main>)
main_end_idx = content.find('</main>')

if main_end_idx == -1:
    print("Errore: </main> non trovato")
    exit(1)

new_section = '''
  <!-- ══════════════ SEZIONE 26: Latch SR ══════════════ -->
  <section class="section" id="s26">
    <div class="section-header">
      <div class="section-num">26</div>
      <h2>Circuiti Sequenziali: <span class="accent">Il Latch SR</span></h2>
    </div>

    <p class="lead">Fino ad ora abbiamo visto solo Circuiti Combinatori (come l'ALU): calcolano risultati in base agli input attuali, ma non hanno "memoria". È arrivato il momento di intrappolare il segnale elettrico per ricordare le informazioni.</p>

    <h3 style="font-size:20px;font-weight:600;color:var(--text);margin:32px 0 16px">1. Che cos'è il Latch SR? (La Memoria Base)</h3>
    <p>Il <strong>Latch SR</strong> (Set-Reset) è il componente elettronico più semplice in grado di memorizzare <strong>1 singolo bit</strong>. È costruito incrociando le uscite di due porte logiche NOR, creando un circolo vizioso (feedback) che "intrappola" il segnale elettrico all'infinito.</p>
    
    <div style="background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:16px; margin:24px 0;">
      <h4 style="margin-top:0; color:var(--text)">I 3 Comandi Principali:</h4>
      <ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:0;">
        <li><strong>Set (S=1, R=0):</strong> Forza la memoria a salvare e accendersi a 1.</li>
        <li><strong>Reset (S=0, R=1):</strong> Forza la memoria a svuotarsi e spegnersi a 0.</li>
        <li><strong>Hold/Memoria (S=0, R=0):</strong> "Chiude" le porte in ingresso. Il circuito continua a far ruotare internamente l'ultimo valore, ricordandolo per sempre.</li>
      </ul>
    </div>

    <div class="widget-container" style="position:relative; background:rgba(0,0,0,0.1); border:2px dashed var(--border); padding:32px; text-align:center; margin:32px 0;">
      <p style="color:var(--muted); font-size:14px; margin:0;">[PLACEHOLDER IMMAGINE: Inserisci qui l'immagine del circuito Latch SR (es. assets/latch-sr.png)]</p>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--blue);margin:40px 0 16px">2. Come si "legge" il circuito? (Il Trucco Umano)</h3>
    <p>Tracciare a mente il percorso dei fili nelle due porte NOR incrociate fa venire il mal di testa. Ma esiste una regola d'oro per capire istantaneamente cosa succede:</p>
    
    <div class="card blue" style="margin-bottom:32px;">
      <div class="card-title">La Regola dell'Uno</div>
      <p style="font-size:14px;margin:4px 0 0">Devi sempre iniziare l'analisi partendo dall'ingresso che vale <strong>1</strong>.</p>
      <ul style="font-size:13px; line-height:1.5; margin-top:8px;">
        <li>L'1 è il "comandante" della porta NOR: appena una NOR vede entrare un 1, la sua uscita viene <strong>forzata istantaneamente a 0</strong>, a prescindere dall'altro filo.</li>
        <li>Questo 0 viene sputato fuori e scivola lungo il filo incrociato fino all'ingresso della porta opposta.</li>
        <li>L'altra porta NOR si ritrova quindi a ricevere sicuramente <em>due zeri</em> in ingresso. E la regola delle NOR dice che due zeri producono un <strong>1</strong> in uscita, confermando lo stato finale!</li>
      </ul>
    </div>

    <h3 style="font-size:20px;font-weight:600;color:var(--red);margin:40px 0 16px">3. Il Caso Vietato e l'Oscillazione (S=1, R=1)</h3>
    <p>Non devi <strong>mai</strong> premere Set e Reset contemporaneamente. Se lo fai, forzi entrambe le porte a sputare 0, un controsenso logico poiché le uscite sono matematicamente una il contrario dell'altra (Q e NOT Q).</p>
    
    <div class="callout red" style="margin-top:24px;">
      <strong>Il disastro del rilascio simultaneo</strong><br>
      Il vero disastro avviene quando rilasci entrambi i bottoni contemporaneamente, passando bruscamente da (S=1, R=1) a (S=0, R=0):
      <ol style="margin-top:8px;">
        <li>Poiché l'hardware lavora in <strong>parallelo</strong>, entrambe le porte si accorgono nello stesso identico istante che gli ingressi sono tornati a zero.</li>
        <li>Entrambe scattano contemporaneamente, sputando <strong>1</strong>.</li>
        <li>Questo 1 viaggia nei fili incrociati. Entrambe le porte lo vedono arrivare contemporaneamente, e scattano a <strong>0</strong>.</li>
        <li>Si innesca così un'<strong>oscillazione infinita e distruttiva</strong>: 0 ➔ 1 ➔ 0 ➔ 1.</li>
      </ol>
      <p style="margin-bottom:0">Alla fine il circuito si stabilizzerà solo perché, nel mondo reale, una delle due porte fisiche sarà <em>microscopicamente</em> più veloce dell'altra, ma il bit salvato in memoria sarà del tutto <strong>casuale e imprevedibile</strong>.</p>
    </div>
  </section>
'''

content = content[:main_end_idx] + new_section + "\n" + content[main_end_idx:]

# Aggiorniamo la sidebar aggiungendo la voce s26
def update_sidebar(html):
    start_sb = html.find('<a class="nav-item" href="06_circuiti.html#s25">')
    end_sb = html.find('</nav>')
    
    if start_sb != -1:
        new_sb = '''<a class="nav-item" href="06_circuiti.html#s25">
    <div class="nav-dot"></div> L'Evoluzione dell'ALU
    <span class="nav-num">25</span>
  </a>
  <a class="nav-item" href="06_circuiti.html#s26">
    <div class="nav-dot"></div> Il Latch SR
    <span class="nav-num">26</span>
  </a>
'''
        html = html[:start_sb] + new_sb + html[end_sb:]
    return html

content = update_sidebar(content)

with open('06_circuiti.html', 'w') as f:
    f.write(content)

# Update index.html array
with open('index.html', 'r') as f:
    idx_content = f.read()

# Replace section 25 with 25 and 26 in index.html
idx_content = re.sub(
    r'\{ id: "s25", title: "L\'Evoluzione dell\'ALU", file: "06_circuiti.html" \},',
    '''{ id: "s25", title: "L'Evoluzione dell'ALU", file: "06_circuiti.html" },
      { id: "s26", title: "Circuiti Sequenziali (Latch SR)", file: "06_circuiti.html" },''',
    idx_content, flags=re.DOTALL
)

with open('index.html', 'w') as f:
    f.write(idx_content)

print("Sezione Latch SR generata!")
