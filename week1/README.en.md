> *Arşiv: eğitmenin özgün İngilizce lab metni (Eylül 2026), olduğu gibi saklanmıştır. Güncel adımlar ve ortam değişkenleri için aynı klasördeki `README.md`.*

# Lab 1 — Your zero-cost AI toolkit (20 min)

Goal: every account you will use this semester is set up, and you have run the same prompt on a cloud model and a local model.

## Steps
1. **GitHub Student Developer Pack** → https://education.github.com/pack  
   Needs: GitHub account, university email (if you have one) **plus** a photo of your student ID / enrollment document. Approval takes days to weeks; apply today. You get GitHub Pro, Codespaces 180 core-hours/month, JetBrains, DigitalOcean credit, Heroku credit.
2. **Azure for Students** ($100, 12 months, no card) → https://azure.microsoft.com/free/students (verify with school email or student ID; you can also link through the GitHub pack).
3. **Google AI Plus, free 1 year for Turkish university students** (18+, until 31 Dec 2026) → https://gemini.google/tr/students  
   Then create a free **Gemini API key** → https://aistudio.google.com (free tier: Flash / Flash-Lite; do not send private data, free-tier data may be used for training).
4. **Zed Pro, free 1 year for students** → https://zed.dev/education (university email + GitHub account older than 30 days).
5. **Ollama** → https://ollama.com/download then  
   `ollama pull qwen3.5:4b` (8 GB RAM laptops) or `ollama pull vngrs-ai/Kumru-2B` (Turkish, ~2B).  
   16 GB RAM: `qwen3.5:9b` or `gemma4:e4b`.
6. Clone the course repo, open `labs/week01`, copy `.env.example` → `.env`, paste your Gemini key.  
   `pip install -r requirements.txt` then `python hello.py`.

Optional free APIs (same code, different `base_url`): Groq (https://console.groq.com), OpenRouter `:free` models (https://openrouter.ai; 50 req/day, 1,000/day after a one-time $10 top-up).

## Success criteria
- `hello.py` prints two answers, two latencies, and one non-zero cost.
- You can explain why the local model reported $0.00 (and what it cost instead: your CPU time and electricity).
- Screenshot posted to the class channel.

## Notes (Sept 2026)
- GitHub Copilot Student sign-ups are paused since April 2026; use **Copilot Free** (2,000 completions + 50 chats/month).
- Cursor's free student year ended 25 June 2026 (Hobby tier still free). Kiro's student year does not include Türkiye.
- Gemini CLI was retired 18 June 2026; Google's replacement is **Antigravity CLI**.
- Codespaces cannot run Ollama (no GPU, limited RAM); run the local half on your laptop.
- Full verified list of student offers: `00-Tasarim/student-resources-2026.md`.
