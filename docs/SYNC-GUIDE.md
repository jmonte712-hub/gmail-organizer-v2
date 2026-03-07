# 🔄 Guida Sincronizzazione — Gmail Organizer v2

## Flusso di lavoro

```
VS Code (editi) ──→ git commit ──→ GitHub (versioning)
                                        │
                                   Google Drive
                                   (backup JSON)
Docker n8n ←── importi JSON aggiornato
     │
     └──→ iCloud (allegati email salvati)
```

## Checklist — dopo ogni modifica al workflow

- [ ] Esporta il JSON da n8n  (Menu → Download)
- [ ] Sovrascivi `workflows/gmail-organizer-v2.workflow.json`
- [ ] `git add . && git commit -m "feat: descrizione modifica"`
- [ ] `git push origin main`
- [ ] Copia il JSON su Google Drive: `Email Organizer/_backups/`

## Comandi Docker

```bash
docker compose up -d         # avvia n8n
docker compose down          # ferma
docker compose logs -f n8n   # log in tempo reale
docker compose pull          # aggiorna immagine n8n
docker compose restart n8n   # riavvia
```

## Percorsi importanti

| Dove | Percorso |
|---|---|
| n8n UI | http://localhost:5678 |
| Workflow JSON | workflows/gmail-organizer-v2.workflow.json |
| iCloud allegati | ~/Library/Mobile Documents/com~apple~CloudDocs/Email Organizer/ |
| GDrive allegati | Email Organizer/CATEGORIA/sottocategoria/ |
| GitHub | github.com/TUO_USERNAME/gmail-organizer-v2 |

## Git — comandi base

```bash
git init                          # prima volta
git remote add origin URL_REPO    # collega GitHub
git add .
git commit -m "messaggio"
git push origin main
```
