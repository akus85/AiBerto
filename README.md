# AiBerto

Codice di supporto agli articoli del blog [aiberto.it](https://aiberto.it).

Ogni cartella raccoglie il codice di un singolo post: dentro trovi gli script e un `requirements.txt` dedicato, così puoi riprodurre gli esempi in modo isolato.

## Indice dei post

| Cartella | Post | Link |
|---|---|---|
| [`intro-llm/01-tokenizzazione`](intro-llm/01-tokenizzazione) | Tokenizzazione: italiano vs inglese, codice, confronto tra modelli | [aiberto.it/tokenizzazione-llm](https://aiberto.it/tokenizzazione-llm) |
| [`intro-llm/02-transformers`](intro-llm/02-transformers) | Testare gli LLM aperti in locale | [aiberto.it/testare-gli-llm-aperti-in-locale](https://aiberto.it/testare-gli-llm-aperti-in-locale) |
| [`intro-llm/03-quantizzazione`](intro-llm/03-quantizzazione) | Quantizzazione: come far girare un LLM 7B | [aiberto.it/quantizzazione-come-far-girare-un-llm-7b](https://aiberto.it/quantizzazione-come-far-girare-un-llm-7b/) |
| [`intro-llm/04-chunking`](intro-llm/04-chunking) | Chunking per RAG | [aiberto.it/chunking-rag](https://aiberto.it/chunking-rag) |
| [`intro-llm/05-database-vettoriali`](intro-llm/05-database-vettoriali) | Database vettoriali | [aiberto.it/vector-database](https://aiberto.it/vector-database) |
| [`intro-llm/06-dspy`](intro-llm/06-dspy) | DSPy: programmare i Language Model | [aiberto.it/dspy-programmare-language-model](https://aiberto.it/dspy-programmare-language-model) |
| [`intro-llm/07-rag-locale`](intro-llm/07-rag-locale) | RAG locale: dal PDF alla risposta | [aiberto.it/rag-locale-dal-pdf-alla-risposta](https://aiberto.it/rag-locale-dal-pdf-alla-risposta) |
| [`intro-llm/08-reranking`](intro-llm/08-reranking) | Reranking per RAG | [aiberto.it/reranking-per-rag](https://aiberto.it/reranking-per-rag) |
| [`intro-llm/11-valutare-un-rag`](intro-llm/11-valutare-un-rag) | Valutare un RAG: Ragas e metriche | [aiberto.it/valutare-rag-ragas-metriche](https://aiberto.it/valutare-rag-ragas-metriche/) |
| [`intro-llm/13-vanna-text-to-sql`](intro-llm/13-vanna-text-to-sql) | Vanna: text-to-SQL, dal database al linguaggio naturale | [aiberto.it/vanna-text-to-sql-database-linguaggio-naturale](https://aiberto.it/vanna-text-to-sql-database-linguaggio-naturale/) |

> Man mano che escono nuovi articoli, la tabella viene aggiornata con il link al post corrispondente.

## Come usare il codice

Ogni cartella è autonoma. Esempio:

```bash
cd intro-llm/01-tokenizzazione
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python 01_conteggio_tiktoken_it_vs_en.py
```
