# <Uygulama adı>

> Bir cümlede ne yapar, kim için.

## Çalıştırma

```bash
pip install -r requirements.txt
cp ../../.env.example .env        # LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
streamlit run app.py
pytest -q                          # ağ gerektirmez
```

## Yayın

Streamlit Community Cloud: repo → `app.py` → Settings → Secrets'a `.streamlit/secrets.toml.example` içeriğini anahtarınızla yapıştırın.

## AI kullanımı

<!-- Ders kuralı: yapay zeka araçlarını kullanmanız beklenir; nasıl kullandığınızı belirtin. -->
- Araç(lar): …
- Ajanın yazdığı / benim yazdığım kısımlar: …
- Ajanın yaptığı ve benim düzelttiğim hata(lar): …
- Testler: hangi testler ajan tarafından üretildi, hangilerini elle yazdım: …

## Spec

Bkz. `SPEC.md` (kabul kriterleri ve kapsam dışı maddeler).
