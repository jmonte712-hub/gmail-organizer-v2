from flask import Flask, request, jsonify
import re, logging, os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOMAIN_RULES = {
    "anthropic.com":       ("AI-TECH",           "claude",              98),
    "openai.com":          ("AI-TECH",           "openai",              98),
    "midjourney.com":      ("AI-TECH",           "midjourney",          98),
    "huggingface.co":      ("AI-TECH",           "huggingface",         98),
    "cursor.sh":           ("AI-TECH",           "cursor",              98),
    "n8n.io":              ("AI-TECH",           "n8n",                 98),
    "copilot.github.com":  ("AI-TECH",           "github-copilot",      98),
    "ryanair.com":         ("VIAGGI",            "voli",                99),
    "vueling.com":         ("VIAGGI",            "voli",                99),
    "iberia.com":          ("VIAGGI",            "voli",                99),
    "easyjet.com":         ("VIAGGI",            "voli",                99),
    "booking.com":         ("VIAGGI",            "hotel",               99),
    "airbnb.com":          ("VIAGGI",            "hotel",               99),
    "renfe.com":           ("VIAGGI",            "treni",               99),
    "trenitalia.com":      ("VIAGGI",            "treni",               99),
    "avis.com":            ("VIAGGI",            "noleggio-auto",       98),
    "hertz.com":           ("VIAGGI",            "noleggio-auto",       98),
    "amazon.com":          ("ACQUISTI-ONLINE",   "amazon",              99),
    "amazon.es":           ("ACQUISTI-ONLINE",   "amazon",              99),
    "amazon.it":           ("ACQUISTI-ONLINE",   "amazon",              99),
    "aliexpress.com":      ("ACQUISTI-ONLINE",   "aliexpress",          99),
    "ebay.com":            ("ACQUISTI-ONLINE",   "ebay",                99),
    "ebay.es":             ("ACQUISTI-ONLINE",   "ebay",                99),
    "zalando.es":          ("ACQUISTI-ONLINE",   "zalando",             99),
    "pccomponentes.com":   ("ACQUISTI-ONLINE",   "pccomponentes",       99),
    "mediamarkt.es":       ("ACQUISTI-ONLINE",   "mediamarkt",          99),
    "revolut.com":         ("FATTURE-RICEVUTE",  "banca",               98),
    "n26.com":             ("FATTURE-RICEVUTE",  "banca",               98),
    "paypal.com":          ("FATTURE-RICEVUTE",  "ricevute-generiche",  95),
    "ebis.es":             ("EBIS",              "comunicazioni",       99),
}

SUBJECT_RULES = [
    (r"(fattura|invoice|ricevuta|receipt)",    "FATTURE-RICEVUTE", "ricevute-generiche", 88),
    (r"(bolletta|bill|utenza)",                "FATTURE-RICEVUTE", "bollette-luce-gas",  88),
    (r"(volo|flight|boarding|check.in)",       "VIAGGI",           "voli",               88),
    (r"(prenotazione|booking|reservation)",    "VIAGGI",           "hotel",              82),
    (r"(ordine|order|spedizione|shipment)",    "ACQUISTI-ONLINE",  "altri-shop",         82),
    (r"(newsletter|unsubscribe)",              "ALTRO",            "newsletter",         90),
    (r"(offerta|promo|sconto|deal|sale)",      "ALTRO",            "spam-promo",         85),
    (r"(affitto|rent|appartamento)",           "IMMOBILIARE",      "affitti",            85),
    (r"(estratto.conto|bank.statement)",       "FATTURE-RICEVUTE", "banca",              88),
]

PERSONAL_SENDERS = {
    "siria":    ("PERSONALE", "siria",    95),
    "luigi":    ("PERSONALE", "luigi",    95),
    "novella":  ("PERSONALE", "novella",  95),
    "niccolo":  ("PERSONALE", "niccolo",  95),
    "patrizia": ("PERSONALE", "patrizia", 95),
}

def classify(domain, subject, sender_name, snippet):
    domain = (domain or "").lower().strip()
    subject = (subject or "").lower().strip()
    sender_name = (sender_name or "").lower().strip()
    snippet = (snippet or "").lower().strip()

    if domain in DOMAIN_RULES:
        cat, sub, conf = DOMAIN_RULES[domain]
        return _result(cat, sub, conf, "domain_exact")

    for rule_domain, (cat, sub, conf) in DOMAIN_RULES.items():
        if domain.endswith("." + rule_domain):
            return _result(cat, sub, conf, "domain_partial")

    for name, (cat, sub, conf) in PERSONAL_SENDERS.items():
        if name in sender_name or name in subject:
            return _result(cat, sub, conf, "personal_sender")

    combined = f"{subject} {snippet}"
    for pattern, cat, sub, conf in SUBJECT_RULES:
        if re.search(pattern, combined, re.IGNORECASE):
            return _result(cat, sub, conf, "subject_keyword")

    return _result("UNKNOWN", "da-valutare", 0, "no_match")

def _result(categoria, sottocategoria, confidence, method):
    needs_ai = confidence < 85
    return {
        "categoria":      categoria,
        "sottocategoria": sottocategoria,
        "confidence":     confidence,
        "needs_ai":       needs_ai,
        "method":         method,
        "label_gmail":    f"{categoria}/{sottocategoria}" if not needs_ai else None,
        "priorita":       "alta" if categoria in ("FATTURE-RICEVUTE","EBIS") and confidence >= 85 else "media" if categoria in ("VIAGGI","ACQUISTI-ONLINE") else "bassa",
    }

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "gmail-classifier-python", "version": "2.0"})

@app.route("/classify", methods=["POST"])
def classify_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Body JSON mancante"}), 400
        result = classify(
            data.get("domain", ""),
            data.get("subject", ""),
            data.get("sender_name", ""),
            data.get("snippet", "")
        )
        logger.info(f"[CLASSIFY] domain={data.get('domain')} cat={result['categoria']}/{result['sottocategoria']} conf={result['confidence']} needs_ai={result['needs_ai']}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e), "categoria": "ALTRO", "sottocategoria": "da-valutare", "confidence": 0, "needs_ai": True, "method": "error_fallback"}), 500

@app.route("/rules", methods=["GET"])
def list_rules():
    return jsonify({"domain_rules": len(DOMAIN_RULES), "subject_rules": len(SUBJECT_RULES), "domains_covered": list(DOMAIN_RULES.keys())})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5679))
    app.run(host="0.0.0.0", port=port)
