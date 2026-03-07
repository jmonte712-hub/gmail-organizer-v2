# 📬 Gmail Organizer — v2

> Evoluzione di gmail-organizer v1.0
> Master EBIS · Hyper-Automation IA

## Stack
- **n8n** (Docker) — motore di automazione
- **OpenAI gpt-4o-mini** — classificatore AI
- **Google Drive** — storage allegati cloud
- **iCloud Drive** — storage allegati locale/sync Mac

## Sincronizzazione
| Tool | Ruolo |
|---|---|
| 🐳 Docker | n8n locale isolato e riproducibile |
| 🐙 GitHub | versioning workflow JSON + codice |
| 💻 VS Code | editor con workspace dedicato |
| ☁️ Google Drive | storage allegati + backup workflow |
| 🍎 iCloud | mirror locale allegati su Mac |

## Struttura
```
gmail-organizer-v2/
├── workflows/          # JSON da importare in n8n
├── schemas/            # Schemi visivi del workflow
├── docs/               # Documentazione e note
├── scripts/            # Script JS/utilità
├── .github/workflows/  # CI/CD GitHub Actions
├── docker-compose.yml  # n8n in Docker
├── .env.example        # Variabili d'ambiente (template)
├── .gitignore          # Esclude .env e dati sensibili
└── README.md
```

## Avvio rapido
```bash
# 1. Clona il repo
git clone https://github.com/TUO_USERNAME/gmail-organizer-v2

# 2. Copia e configura le variabili
cp .env.example .env
# → apri .env e inserisci le tue chiavi

# 3. Avvia n8n in Docker
docker compose up -d

# 4. Apri n8n nel browser
open http://localhost:5678
```

## Versioni
| Data | Versione | Note |
|---|---|---|
| 2026-03-05 | v1.0 | Prima versione (npx n8n) |
| 2026-03-07 | v2.0 | Docker + GitHub + struttura ordinata |
