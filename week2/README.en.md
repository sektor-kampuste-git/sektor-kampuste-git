> *Arşiv: eğitmenin özgün İngilizce lab metni (Eylül 2026), olduğu gibi saklanmıştır. Güncel adımlar ve ortam değişkenleri için aynı klasördeki `README.md`.*

# Lab 2 — Tokens, temperature, and a local Turkish bake-off (20 min)

Goal: measure three things you were told in the lecture instead of believing them: Turkish costs more tokens than English, temperature changes determinism, and a 2B Turkish model can compete with a 4B general model on your own laptop.

## Steps
1. **Setup (2 min)**  
   `cd labs/week02` → `pip install -r requirements.txt` → copy `.env.example` to `.env` and paste your Gemini key from Week 1 (https://aistudio.google.com).  
   On your laptop (not Codespaces): `ollama pull qwen3.5:4b` and `ollama pull vngrs-ai/Kumru-2B`. Start the pulls now; they take the longest.
2. **tokens.py (5 min)** — `python tokens.py`  
   Counts the same rental-contract paragraph in Turkish and English with **tiktoken** (`o200k_base`, the GPT-4o/5/6 vocabulary) and two Hugging Face tokenizers (**Qwen**, **Kumru**). Record the TR/EN ratio for each tokenizer. Then look at how `evlerimizdekilerden` is split.
3. **temperature.py (4 min)** — `python temperature.py`  
   One Turkish prompt on Gemini 3.5 Flash at temperature 0, 0.7 and 1.5, three runs each. Write a one-line verdict per temperature (identical? same meaning? broken?).
4. **bakeoff.py (8 min)** — `python bakeoff.py`  
   10 Turkish questions from `questions.json` against `vngrs-ai/Kumru-2B` and `qwen3.5:4b` on Ollama. Prints accuracy (keyword match) and tokens/s per model, writes `results.csv`.
5. **Bonus — similarity.py**  
   `pip install sentence-transformers`, then `python similarity.py`: cosine similarity matrix of 5 Turkish sentences with `ytu-ce-cosmos/turkish-e5-large`.

## Success criteria
- A table with TR and EN token counts for 3 tokenizers and the ratio (expect roughly 1.3–2.0 on o200k, lower on Kumru).
- Nine temperature outputs with your one-line verdict per temperature.
- `results.csv` with accuracy and tokens/s for both local models, posted to the class channel.

## Links
- Transformer Explainer: https://poloclub.github.io/transformer-explainer
- Tiktokenizer: https://tiktokenizer.vercel.app · tiktoken: https://github.com/openai/tiktoken
- Kumru-2B model card: https://huggingface.co/vngrs/Kumru-2B
- Ollama library: https://ollama.com/library
- Turkish embeddings: https://huggingface.co/ytu-ce-cosmos/turkish-e5-large

## Notes and troubleshooting (Sept 2026)
- Codespaces cannot run Ollama (no GPU, limited RAM). Steps 1 and 4 run on your laptop; steps 2–3 run anywhere.
- `ollama serve` must be running; check tags with `ollama list` and edit `MODELS` in `bakeoff.py` if yours differ.
- If campus Wi-Fi blocks huggingface.co, `tokens.py` skips the HF tokenizers and still prints the tiktoken row.
- Gemini free tier: Flash / Flash-Lite only; if `gemini-3.5-flash` is rate-limited, set `GEMINI_MODEL=gemini-3.5-flash-lite` in `.env`, or point `temperature.py` at Ollama (commented line in the file).
- Same code, other providers (change `BASE_URL`/`MODEL`/key): Groq `https://api.groq.com/openai/v1`, OpenRouter `https://openrouter.ai/api/v1`, the instructor's Azure AI Foundry endpoint.
- Keyword-match accuracy is deliberately crude; Week 8 replaces it with real evals. Look at the misses: wrong, or right with different wording?
