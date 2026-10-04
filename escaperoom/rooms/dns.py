import base64
import codecs

def valid_lines():
    valid_lines = []
    with open("escaperoom/data/dns.cfg", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                valid_lines.append(line)
    return valid_lines

def parseLine(lines):
    records = {}
    for line in lines:
        if "=" not in line:
            continue
        cle, valeur = line.split("=", 1)
        cle = cle.strip()
        valeur = valeur.strip()
        records[cle] = valeur
    return records

ENCODAGES_VALIDES = ("b64", "rot13+b64")

def encoding(values):
    if ":" not in values:
        raise ValueError(f"Invalid encoding format. Expected 'encodage:payload'.")
    encodage, payload = values.split(":", 1)
    encodage = encodage.strip()
    payload = payload.strip()
    
    if encodage not in ENCODAGES_VALIDES:
        raise ValueError(f"Invalid encoding '{encodage}'. Valid encodings are: {ENCODAGES_VALIDES}")
    if payload == "":
        raise ValueError("Payload is empty.")
    return encodage, payload


def decode(values):
    encodage, payload = encoding(values)
    if encodage == "rot13+b64":
        decoded_payload = codecs.decode(payload, "rot_13")
        decoded_payload = base64.b64decode(decoded_payload, validate=True).decode("utf-8")
    elif encodage == "b64":
        decoded_payload = base64.b64decode(payload, validate=True).decode("utf-8")
    else:
        raise ValueError(f"Unsupported encoding '{encodage}'.")
    return decoded_payload

def find_hint(records):
    if "token_tag" not in records:
        raise ValueError("Missing 'token_tag' in records.")
    
    hint = "hint" + decode(records["token_tag"]).strip()
    
    if hint not in records:
        raise ValueError(f"Missing '{hint}' in records.")

    return hint

def extract_token(sentence):
    words = sentence.strip().rstrip(".").split()
    return words[-1]


records = parseLine(valid_lines())
hint_key = find_hint(records)
sentence = decode(records[hint_key])
token = extract_token(sentence)
encodage = encoding(records[hint_key])[0]

print(f"TOKEN[DNS]={token}")
print(f"EVIDENCE[DNS].KEY={hint_key}")
print(f"EVIDENCE[DNS].ENCODING={encodage}")
print(f"EVIDENCE[DNS].DECODED_LINE={sentence}")