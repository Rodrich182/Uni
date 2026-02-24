"""
Code adapted from the NLP class by Daniel Jurafski & Christopher Manning
"""
import sys
import os
import re
import pprint
import html
from dictionary import email_patterns, phone_pattern
my_first_pat = r'(\w+)@(\w+).edu'

""" 
TODO
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers
"""
def process_file(name, f):
    res = []
    text = f.read()
    
    # ------------------------------------------------
    # 1. FIX BALAJI (Antes de limpiar HTML)
    # ------------------------------------------------
    emails = set()
    for m in re.finditer(r'mailto:([a-zA-Z0-9._+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,6})', text, re.IGNORECASE):
        emails.add(m.group(1))

    # ------------------------------------------------
    # 2. LIMPIEZA
    # ------------------------------------------------
    clean = html.unescape(text)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = re.sub(r'&[a-zA-Z0-9#]+;', ' ', clean)
    
    # Normalización simple (ayuda a las regex siguientes)
    clean = clean.replace(' AT ', ' at ').replace(' DOT ', ' dot ')
    
    # ------------------------------------------------
    # 3. PATRONES ESTÁNDAR (Los que ya tenías)
    # ------------------------------------------------
    
    # User@domain
    for m in re.finditer(r'([a-zA-Z0-9._+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})\b', clean):
        emails.add(m.group(0))

    # Obfuscate
    for m in re.finditer(r"obfuscate\(['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]\)", clean):
        emails.add(f"{m.group(2)}@{m.group(1)}")

    # User at domain dot tld (Con 'dot' explícito)
    # Mejoramos la limpieza: reemplaza " dot " por "." y quita espacios sobrantes
    for m in re.finditer(r'([a-zA-Z0-9._+-]+)\s+at\s+([a-zA-Z0-9.-]+(?:\s+dot\s+[a-zA-Z0-9.-]+)+)', clean, re.IGNORECASE):
        domain_raw = m.group(2)
        # Limpiar "dot"
         # AHORA: Incluye 'dt'
        domain = re.sub(r'\s+(?:dot|dt)\s+', '.', domain_raw, flags=re.IGNORECASE)
        # Limpiar posibles dobles puntos o espacios que queden
        domain = domain.replace('..', '.').replace(' ', '')
        emails.add(f"{m.group(1)}@{domain}")
    # ------------------------------------------------
    # 4. FIXES ESPECÍFICOS (Añadidos ahora)
    # ------------------------------------------------

    # FIX CHERITON: "followed by"
    for m in re.finditer(r'([a-zA-Z0-9._+-]+)[,\s]+followed\s+by\s+(?:the\s+domain\s+|@)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})', clean, re.IGNORECASE):
        emails.add(f"{m.group(1)}@{m.group(2)}")

     # ------------------------------------------------------------------
    # FIX COMBINADO (ASHISHG/ULLMAN/ENGLER) - Versión Segura y Rápida
    # ------------------------------------------------------------------
    # Captura "user at ..." seguido de CUALQUIER COSA hasta llegar a un TLD
    # Esto cubre tanto "cs stanford edu" (espacios) como "stanford.edu" (puntos)
    
    regex_safe = r'\b([a-zA-Z0-9._+-]+)\s+at\s+([a-zA-Z0-9\s.-]{1,50})\s+(edu|com|org|net)\b'
    
    for m in re.finditer(regex_safe, clean, re.IGNORECASE):
        user = m.group(1)
        middle = m.group(2) # Puede ser "cs stanford" o "stanford." o "cs dot stanford"
        tld = m.group(3)
        
        # 1. Limpiar "dot" y "dt" explícitos
        temp = re.sub(r'(?:dot|dt)', '.', middle, flags=re.IGNORECASE)
        # 2. Convertir espacios en puntos
        temp = re.sub(r'\s+', '.', temp)
        # 3. Eliminar puntos repetidos (ej: "stanford.." -> "stanford.")
        temp = re.sub(r'\.+', '.', temp)
        # 4. Quitar puntos finales si quedaron (ej: "stanford." -> "stanford")
        temp = temp.strip('.')
        
        # Reconstruir dominio
        domain = f"{temp}.{tld}"
        
        # Validaciones de seguridad
        # - Que no empiece por punto
        if domain.startswith('.'): domain = domain[1:]
        # - Que tenga caracteres válidos
        if not re.match(r'^[a-zA-Z0-9.-]+$', domain): continue
        # - Que no sea una frase larga disfrazada (max 4 subdominios)
        if domain.count('.') > 4: continue
        
        emails.add(f"{user}@{domain}")
    # FIX FINAL (ASHISHG/ULLMAN SIMPLE): "user at domain.edu"
    # Captura casos donde el dominio NO está troceado con espacios, sino que ya tiene puntos.
    # Ejemplo: "ashishg at stanford.edu"
    for m in re.finditer(r'\b([a-zA-Z0-9._+-]+)\s+at\s+([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})\b', clean, re.IGNORECASE):
        user = m.group(1)
        domain = m.group(2)
        # Limpieza extra por si acaso (ej: quitar espacios alrededor de puntos)
        domain = domain.replace(" ", "")
        emails.add(f"{user}@{domain}")
    
        
    # ------------------------------------------------
    # 5. GUARDAR Y FILTRAR
    # ------------------------------------------------
    invalid = {'server', 'contact', 'email', 'phone', 'fax', 'admin'}
    
    for email in emails:
        email = email.lower().replace("'", "")
        if '@' not in email: continue
        
        u, d = email.split('@', 1)
        if u in invalid or len(u) < 2: continue
        if '.' not in d: continue
        
        res.append((name, 'e', email))

    # ------------------------------------------------
    # 6. TELÉFONOS (Tu código original perfecto)
    # ------------------------------------------------
    phones = set()
    for m in re.finditer(r'(?:\+?1[-.\s]?)?\(?([2-9]\d{2})\)?[-.\s]?([2-9]\d{2})[-.\s]?(\d{4})', clean):
        phones.add(f"{m.group(1)}-{m.group(2)}-{m.group(3)}")
    
    for p in phones:
        res.append((name, 'p', p))
        
    return res

"""
You should not need to edit this function.
Given a path to a directory, it processes all files
in that directory using the method 'process_file',
and collects all results in a unique list of tuples 
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    print('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))



"""
The main program takes a directory name and gold file (you should not need to edit it).
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    guess_list = process_dir('./data/dev')
    gold_list =  get_gold('./data/devGOLD')
    score(guess_list, gold_list)
