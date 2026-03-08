# 📋 Contesto Sessione — Gmail Organizer v2

## Stato attuale (2026-03-08)
- Docker: n8n (porta 5678) + Python Flask (porta 5679) — entrambi running
- Workflow ibrido importato in n8n e testato — FUNZIONANTE
- Python classifica domini noti (es. ryanair.com) senza chiamare OpenAI
- GitHub: jmonte712-hub/gmail-organizer-v2 — aggiornato

## Prossimi passi (domani)
- [ ] Verificare containers: docker compose ps
- [ ] Correggere label ID Gmail nel workflow (sono hardcoded, vanno aggiornati)
- [ ] Test con email reali — una per categoria
- [ ] Attivare workflow in produzione
- [ ] Commit finale

## Stack
- n8n: http://localhost:5678
- Python API: http://localhost:5679
- Workflow: Gmail Organizer v2 — Python + OpenAI Hybrid
- GitHub: github.com/jmonte712-hub/gmail-organizer-v2

## Come riaprire la sessione con Claude
Incolla questo all'inizio della nuova chat:
"Stiamo lavorando su gmail-organizer-v2, workflow ibrido n8n + Python Flask.
Docker gira con n8n (5678) e Python classifier (5679).
Domani dobbiamo: correggere label ID Gmail, testare email reali, attivare produzione."
