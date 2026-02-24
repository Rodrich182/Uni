import re

# Patrón para TELÉFONO (Norteamérica: formato ###-###-####)
# Mantenemos el que tenías, funcionaba perfecto.
phone_pattern = (
    r'(?:(?:TEL|Phone|Tel|Call|Fax|Office|Contact)\s*[:\.]?\s*)?'
    r'(?:\+?1\s*[-.\s]?)?'
    r'(?:[\(\[]?\s*)?'
    r'([2-9]\d{2})'                    # área
    r'(?:\s*[\)\]]?\s*[-.\s/]*)?'
    r'([2-9]\d{2})'                    # exchange
    r'[-.\s/]*'
    r'(\d{4})'                         # línea
    r'(?!\d)'
)

email_patterns = [
    # 0) obfuscate('domain','user') - El clásico script
    r"obfuscate\(['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]\)",

    # 1) mailto: (Captura segura directa del HTML)
    r"mailto:([a-zA-Z0-9._+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,6})",

    # 2) Standard user@domain.tld (Con word boundaries para no pillar .eduphone)
    r"\b([a-zA-Z0-9._+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})\b",

    # 3) "user at domain dot tld" (Con separadores explícitos)
    # Captura: "ashishg at stanford dot edu"
    r"\b([a-zA-Z0-9._+-]+)\s+at\s+([a-zA-Z0-9.-]+(?:\s+(?:dot|dt)\s+[a-zA-Z0-9.-]+)+)\b",

    # 4) "user (at) domain (dot) tld"
    r"\b([a-zA-Z0-9._+-]+)\s*\(at\)\s*([a-zA-Z0-9.-]+(?:\s*\(dot\)\s*[a-zA-Z0-9.-]+)+)\b",

    # 5) "followed by" (Caso Cheriton)
    r"([a-zA-Z0-9._+-]+)[,\s]+followed\s+by\s+(?:the\s+domain\s+|@)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})",

    # 6) "user at server dot domain" (Caso Ashishg/Server)
    # Ejemplo: "ashishg at server cs.stanford.edu" o "ashishg at machine cs.stanford.edu"
    r"\b([a-zA-Z0-9._+-]+)\s+(?:at|on)\s+(?:server|machine)\s+([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})\b",

    # 7) EL SALVAVIDAS: Espacios implícitos (Caso Ullman, JKS, Engler)
    # Captura: "ullman at cs stanford edu"
    # TRUCO: Exigimos que termine en un TLD común para evitar Falsos Positivos
    r"\b([a-zA-Z0-9._+-]+)\s+at\s+((?:[a-zA-Z0-9-]+\s+)+?(?:edu|com|org|net|gov|mil))\b"
    # 8) "user at domain.tld" (Dominio ya formado, solo separado por 'at')
    # Ejemplo: "ashishg at stanford.edu"
    r"\b([a-zA-Z0-9._+-]+)\s+at\s+([a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})\b"
]
