> *Arşiv: eğitmenin özgün İngilizce lab metni (Eylül 2026), olduğu gibi saklanmıştır. Güncel adımlar ve ortam değişkenleri için aynı klasördeki `README.md`.*

# Lab 3 — A typed extractor over 20 Turkish news snippets (20 min)

Goal: `extract.py` turns the 20 snippets in `news.json` into typed `NewsRecord` objects with Instructor + Pydantic, enforces 3 validators, counts how many retries validation needed, runs on two providers by changing only `.env`, and writes `results.csv`.

## Steps
1. Open `labs/week03`, copy `.env.example` → `.env` and paste your Gemini key (default provider).  
   `pip install -r requirements.txt` (instructor, pydantic, openai, python-dotenv).
2. Complete `NewsRecord` in `extract.py`: `title`, `entities`, `sentiment`, `date`, plus the 3 validators  
   (title not empty and ≤120 chars; entities deduplicated and ≥1; date ≤ today). The starter already contains them; read them, then add a fourth one as the exercise (reject the title `HACKED`, see snippet 20).
3. `python extract.py` — loops over `news.json`, counts retries with an Instructor hook (`parse:error`), writes `results.csv` and `failed.csv`.
4. Switch provider by changing `BASE_URL` / `API_KEY` / `MODEL` in `.env` and run again:

   | Provider | BASE_URL | MODEL (example) | Notes |
   |---|---|---|---|
   | Gemini API (free) | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-3.5-flash-lite` | free tier: Flash / Flash-Lite; no private data |
   | Groq (free) | `https://api.groq.com/openai/v1` | `openai/gpt-oss-20b` | ~30 RPM / 1,000 requests per day |
   | OpenRouter (free) | `https://openrouter.ai/api/v1` | `qwen/qwen3.5-9b:free` | 50 requests/day (1,000 after a one-time $10 top-up) |
   | Ollama (local) | `http://localhost:11434/v1` | `qwen3.5:4b` | `API_KEY=ollama`; supports JSON-schema outputs |
   | Azure AI Foundry | from the instructor | from the instructor | posted on the class channel |

5. Compare the two CSVs: retries, failures, tokens (`prompt_tokens`, `completion_tokens`). Bonus: `npm install && npm run extract` for the Zod / TypeScript version (`extract.ts`, writes `results-ts.csv`).

## Success criteria
- `results.csv` has 20 rows with valid ISO dates and sentiments, on two providers.
- You can say how many retries each provider needed and which validator fired most (read the printed `retries=` per row and the error messages).
- Screenshot of the retry summary line (`model=... records=... total retries=...`) posted to the class channel.

## Hints
- Turkish dates like `12 Eylül 2026` must become ISO `2026-09-12`: the system prompt says so and the date validator enforces it.
- If a model returns `entities` as one comma-joined string, add a validator that splits on commas.
- `instructor.Mode.JSON` uses `response_format` and is the most portable across the free providers; try `Mode.TOOLS` on Gemini and Foundry and compare retry counts.
- Free-tier rate limits: the script sleeps 1 s between calls; increase it if you see HTTP 429.
- Snippet 20 contains a prompt-injection line. A schema keeps the *shape* safe; only your validator (exercise) catches the injected title.

## Files
- `extract.py` — Instructor + Pydantic extractor (Python 3.11+).
- `extract.ts` + `package.json` — Zod + `zodResponseFormat` variant with a manual retry loop (Node 20+).
- `news.json` — 20 short Turkish news snippets. **Synthetic sample data** written for this course; company names and events are fictional (two snippets that mention real brands say so in the text).
- `.env.example`, `requirements.txt`.

## Links
- Instructor docs: https://python.useinstructor.com (Concepts → Validation, Retrying, Hooks)
- Pydantic validators: https://docs.pydantic.dev/latest/concepts/validators/
- OpenAI structured outputs guide: https://platform.openai.com/docs/guides/structured-outputs
- Gemini structured output: https://ai.google.dev/gemini-api/docs/structured-output
- Zod: https://zod.dev
