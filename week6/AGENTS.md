# AGENTS.md — bu repoda çalışan kodlama ajanları için kurallar

> Bu dosyayı projenizin köküne koyun. Copilot, Claude Code, Zed, Cursor ve Antigravity bu dosyayı (ya da `.cursorrules` / `.github/copilot-instructions.md` eşdeğerini) ilk okur.
> Kısa tutun; ajan uzun kuralları unutur, kısa olanlara uyar.

## Proje
- Python 3.12 · Streamlit · `openai` istemcisi (OpenAI uyumlu endpoint, sağlayıcıdan bağımsız)
- Dosya düzeni: `app.py` (arayüz, yalnızca st.*), `llm.py` (model katmanı, st.* YOK), `tests/` (ağsız)
- Spec: `SPEC.md` — kabul kriterleri numaralıdır; bir kriteri karşılayan her değişiklik ilgili testi de ekler

## Yapılacaklar
- Değişiklikten önce planı 3-5 madde halinde yaz, onay bekle
- Her kabul kriteri için en az bir test; `pytest -q` yeşil olmadan "bitti" deme
- Model çağrılarını `llm.py` içinde tek fonksiyonda topla; testlerde `patch` ile taklit et
- Hata mesajları Türkçe ve kullanıcıya anlaşılır; teknik iz (traceback) arayüze sızmaz
- Küçük, açıklayıcı commit'ler: `feat: K3 maliyet gösterimi`, `test: K2 cümle sayısı`

## Yapılmayacaklar
- `.env`, `secrets.toml`, API anahtarı ya da token'ı HİÇBİR dosyaya yazma, log'lama, commit'leme
- Yeni bağımlılık ekleme — önce sor
- `SPEC.md` kapsam dışı maddelerini "madem buradayız" diye yapma
- Testi geçirmek için testi silme ya da `skip` etme
- Model adını koda sabitleme; `LLM_MODEL` ortam değişkeninden oku

## Bittiğinde
- `pytest -q` çıktısını göster
- README'deki "AI kullanımı" bölümüne ne yaptığını 3 madde ile yaz
- Değiştirdiğin dosyaları listele
