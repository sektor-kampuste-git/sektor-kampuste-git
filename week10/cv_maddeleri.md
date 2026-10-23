# CV maddeleri: zayıf → güçlü

Formül: **Ne yaptın (fiil) + neyle (teknoloji) + ölçülebilir sonuç + kanıt bağlantısı.** İngilizce sürümünü de yazın; çoğu ilan sistemi İngilizce tarıyor.

| Zayıf | Güçlü (TR) | Güçlü (EN) |
|---|---|---|
| "LLM projeleri yaptım" | "OpenAI uyumlu tek istemciyle 3 sağlayıcıya (OpenRouter, Gemini, Ollama) bağlanan, model başına maliyet/gecikme ölçen bir karşılaştırma aracı yazdım" | "Built a provider-agnostic LLM benchmarking tool (Foundry, Gemini, Ollama) reporting per-model cost and latency via a single OpenAI-compatible client" |
| "RAG chatbot geliştirdim" | "8 belgelik Türkçe derlemde hibrit (BM25+vektör, RRF) RAG kurdum; RAGAS tarzı eval ile sadakati 0.71'den 0.93'e çıkardım" | "Built hybrid-retrieval RAG (BM25 + vectors, RRF) over a Turkish corpus; raised faithfulness from 0.71 to 0.93 using a RAGAS-style eval set" |
| "AI ajanı yaptım" | "Araç çağıran destek ajanına adım/token/USD/süre bütçesi ve durma koşulları ekledim; 4 aracı MCP sunucusu olarak VS Code'a açtım" | "Designed a tool-calling support agent with step/token/USD/time budgets and stop conditions; exposed 4 tools via an MCP server consumed by VS Code" |
| "Prompt engineering" | "15 vakalık eval setini CI'ya bağladım; prompt v1→v3 geçişinde 6/15 → 14/15, güvenlik vakalarında 0 regresyon" | "Wired a 15-case eval suite into CI; prompt v1→v3 improved pass rate from 6/15 to 14/15 with zero security regressions" |
| "Güvenlik konularına ilgiliyim" | "12 saldırılık red team setiyle prompt injection testi yaptım; dolaylı injection'a karşı yetki kısıtı + canary tabanlı çıktı filtresi uyguladım (OWASP LLM01/06)" | "Red-teamed an LLM assistant with a 12-attack suite; mitigated indirect prompt injection via least-privilege tools and canary-based output filtering (OWASP LLM01/06)" |
| "ChatGPT kullanıyorum" | "Spec + AGENTS.md ile ajan tabanlı IDE'de 40 dakikada testli Streamlit uygulaması geliştirip Streamlit Cloud'a yayınladım; README'de AI kullanımını belgeledim" | "Shipped a tested Streamlit app from spec in 40 minutes using an agentic IDE with AGENTS.md guardrails; documented AI usage in the README" |
| "İş analizi yaptım" | "Sigorta hasar triyajı için ROI modeli kurdum (hata oranı duyarlılığı dahil); EU AI Act risk sınıfı ve KVKK kontrol listesiyle kullanım senaryosu özeti yazdım" | "Modeled ROI for an insurance claims triage use case (incl. error-rate sensitivity); authored a one-page brief with EU AI Act risk classification and KVKK checklist" |

## Yapılmayacaklar
- Araç listesi yığını ("Python, LangChain, OpenAI, Pinecone, Docker, Kubernetes…") — sonuç yoksa liste değersiz
- "Sorumluydum", "dahil oldum" — ne *yaptığınızı* yazın
- Sayısız iddia ("başarıyı artırdım")
- Doğrulanamayan bağlantı (private repo, ölü URL). Public repo ya da ekran görüntülü PDF.

## Bu dersten çıkan 5 madde (şablon)
Beş beceri tablosundan her satıra bir madde; her maddenin sonunda `github.com/<siz>/<repo>/tree/main/<klasör>`.
