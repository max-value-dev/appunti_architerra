import re

with open('06_circuiti.html', 'r') as f:
    content = f.read()

# Trova inizio delle slide
start_slides = content.find('id="slidesContainer"')
end_slides = content.find('<!-- ══════════════ SEZIONE 26 ══════════════ -->')

# Slide 1 testuale:
# Da: <p>Costruiamo la versione...
# A: <img src="assets/alu/alu-1bit.png"
slide1_orig = '''<p>Costruiamo la versione primordiale dell'ALU: un circuito capace solo di eseguire le tre operazioni fondamentali su un singolo bit: AND, OR e l'Addizione matematica.</p>
            <p>Gli ingegneri piazzano in parallelo una porta AND, una porta OR e il nostro Full Adder. A decidere quale risultato sopravvivrà ci pensa un <strong>Multiplexer a 3 ingressi</strong> comandato dal filo <code>Operation</code>.</p>'''

slide1_new = '''<ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>Scopo:</strong> Costruire un'ALU primordiale per eseguire solo 3 calcoli (AND, OR, Somma).</li>
              <li><strong>Costruzione:</strong> Si piazzano in parallelo una porta AND, una porta OR e un Full Adder.</li>
              <li><strong>Il Controllo:</strong> I segnali entrano in tutti e tre i blocchi. Un <strong>Multiplexer a 3 vie</strong>, guidato dal filo <code>Operation</code>, sceglie l'unico risultato da far uscire.</li>
            </ul>'''

content = content.replace(slide1_orig, slide1_new)

# Slide 2 testuale:
slide2_orig = '''<p>L'ALU base è bloccata. Non sa calcolare il <code>NOR</code> logico e non sa sottrarre! E gli ingegneri si rifiutano di costruire un hardware nuovo di zecca solo per fare A - B.</p>
            <p>Sappiamo che per sottrarre ci basta usare l'addizionatore col <strong>Complemento a 2</strong>: capovolgere tutti i bit di B e aggiungere 1. Per "capovolgere" a comando, vengono piazzati due <strong>Multiplexer a 2 ingressi</strong> (i deviatori). Ognuno riceve il segnale intatto e quello passato da una porta <code>NOT</code>.</p>'''

slide2_new = '''<ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>Il Problema:</strong> L'ALU base non sa calcolare la Sottrazione né il NOR logico.</li>
              <li><strong>La Soluzione:</strong> Sfruttare l'addizionatore col <em>Complemento a 2</em> (inverti i bit + somma 1).</li>
              <li><strong>Hardware:</strong> Vengono piazzati due piccoli MUX in ingresso. Ognuno funge da deviatore tra il segnale <em>normale</em> e il segnale <em>capovolto</em> da una porta NOT.</li>
            </ul>'''

content = content.replace(slide2_orig, slide2_new)

# Slide 3 testuale:
slide3_orig = '''<p>Vogliamo che l'hardware risponda a $A < B$. Se è vero 1, altrimenti 0. L'unico modo è calcolare di nascosto $A - B$: se esce negativo, A era minore. Ma il "segno negativo" viene calcolato <em>soltanto</em> dall'ultima ALU, quella del bit 31. Dobbiamo sdoppiare l'hardware!</p>'''

slide3_new = '''<ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>L'Obiettivo:</strong> Rispondere alla domanda $A < B$ (istruzione <code>slt</code>).</li>
              <li><strong>Il Metodo:</strong> L'hardware calcola $A - B$. Se il risultato è negativo, A era minore di B.</li>
              <li><strong>Il Problema:</strong> Il "segno negativo" esiste <em>solo</em> nell'ultima ALU (bit 31). Dobbiamo sdoppiare il design!</li>
            </ul>'''

content = content.replace(slide3_orig, slide3_new)

# Slide 4 testuale (è in flex):
slide4_orig = '''<p>Se sommiamo due numeri positivi enormi, il loro risultato potrebbe "bucare" la capacità dei 32 bit e invadere proprio l'ultimo bit (il bit del segno). Il computer crederebbe erroneamente di aver ottenuto un numero negativo! È l'<strong>Overflow</strong>.</p>
            <p>Gli ingegneri hardware hanno dimostrato un teorema infallibile: c'è Overflow <em>esclusivamente</em> quando il riporto che entra nell'ultimo bit (<code>CarryIn</code> 31) è diverso dal riporto che ne esce (<code>CarryOut</code> 31).</p>
            <p>Soluzione? Per lanciare un segnale "1" quando due fili sono diversi tra loro, basta usare una magnifica porta <strong>XOR</strong>!</p>'''

slide4_new = '''<ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>L'Errore:</strong> Sommando numeri enormi, si invade il bit del segno. Il PC crede che il risultato positivo sia negativo: è l'<strong>Overflow</strong>.</li>
              <li><strong>La Scoperta:</strong> C'è Overflow <em>solo</em> quando il <code>CarryIn</code> dell'ultimo bit differisce dal <code>CarryOut</code> dell'ultimo bit.</li>
              <li><strong>La Soluzione:</strong> Si piazza una singola porta <strong>XOR</strong> a cavallo dei due Carry. Se sono diversi, scatta l'allarme!</li>
            </ul>'''

content = content.replace(slide4_orig, slide4_new)

# Slide 5 testuale:
slide5_orig = '''<p>Per le istruzioni come <code>beq</code> (salta se uguali), la CPU deve sapere istantaneamente se il calcolo ha prodotto Esattamente Zero. Tutti i 32 fili del risultato vengono infilati in un titanico <strong>NOR a 32 vie</strong> (un OR gigante + NOT). Solo se sono tutti zeri, il NOR sputa '1', accendendo l'allarme <strong>Zero</strong>!</p>'''

slide5_new = '''<ul style="font-size:14px; line-height:1.6; color:var(--text); padding-left:20px; margin-bottom:16px;">
              <li><strong>Il Requisito:</strong> Per l'istruzione <code>beq</code> (Branch if Equal), l'hardware deve capire istantaneamente se A = B calcolando A - B e verificando se il risultato è Zero.</li>
              <li><strong>La Soluzione:</strong> I 32 fili d'uscita entrano in un titanico <strong>NOR a 32 vie</strong> (un enorme OR seguito da un NOT).</li>
              <li><strong>Il Risultato:</strong> Solo se tutti i 32 bit sono 0, il circuito sputa fuori '1', accendendo la bandierina <strong>Zero</strong>.</li>
            </ul>'''

content = content.replace(slide5_orig, slide5_new)

with open('06_circuiti.html', 'w') as f:
    f.write(content)

print("Slide modificate e rese schematiche!")
