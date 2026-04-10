# AiBerto

Codice di supporto agli articoli del blog [aiberto.it](https://aiberto.it).

Ogni cartella raccoglie il codice di un singolo post: dentro trovi gli script e un `requirements.txt` dedicato, così puoi riprodurre gli esempi in modo isolato.

## Indice dei post

| Cartella | Post | Link |
|---|---|---|
| [`intro-llm/01-tokenizzazione`](intro-llm/01-tokenizzazione) | Tokenizzazione: italiano vs inglese, codice, confronto tra modelli | [aiberto.it/tokenizzazione-llm](https://aiberto.it/tokenizzazione-llm) |
| [`intro-llm/02-transformers`](intro-llm/02-transformers) | Testare gli LLM aperti in locale | [aiberto.it/testare-gli-llm-aperti-in-locale](https://aiberto.it/testare-gli-llm-aperti-in-locale) |

> Man mano che escono nuovi articoli, la tabella viene aggiornata con il link al post corrispondente.

## Come usare il codice

Ogni cartella è autonoma. Esempio:

```bash
cd intro-llm/01-tokenizzazione
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python 01_conteggio_tiktoken_it_vs_en.py
```
