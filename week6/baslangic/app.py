"""
week6 · baslangic/app.py — Streamlit iskeleti. Spec'inizi bunun üzerine kurun.

Çalıştır:  streamlit run app.py
Yerleşim:  kenar çubuğu = ayarlar, ana alan = girdi → sonuç → ölçümler.
Streamlit Cloud'da .env yerine Secrets kullanılır; llm.py ikisini de okur (st.secrets → os.environ köprüsü aşağıda).
"""
from __future__ import annotations

import os

import streamlit as st

# Streamlit Cloud: Secrets → ortam değişkeni köprüsü (yerelde .env zaten yüklenir)
for anahtar in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"):
    try:
        if anahtar in st.secrets and not os.getenv(anahtar):
            os.environ[anahtar] = str(st.secrets[anahtar])
    except Exception:  # noqa: BLE001 — secrets dosyası yoksa sessizce geç
        pass

from llm import GOREVLER, calistir, maliyet_usd  # noqa: E402  (köprüden sonra içe aktarılmalı)

st.set_page_config(page_title="Metin Asistanı", page_icon="🧰", layout="centered")
st.title("🧰 Metin Asistanı")
st.caption("week6 başlangıç iskeleti · Bulut Bilişim ve Yapay Zeka Teknolojileri")

with st.sidebar:
    st.header("Ayarlar")
    model = st.text_input("Model", os.getenv("LLM_MODEL", "gpt-6-luna"))
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
    max_tokens = st.number_input("Maks çıktı token", 64, 4000, 600, 32)
    st.divider()
    st.caption("Maliyet için 1M token fiyatı (USD) — week4/fiyatlar.json")
    girdi_fiyat = st.number_input("Girdi $/1M", 0.0, 100.0, 0.10, 0.01)
    cikti_fiyat = st.number_input("Çıktı $/1M", 0.0, 500.0, 0.50, 0.01)
    st.divider()
    endpoint = os.getenv("LLM_BASE_URL", "")
    st.caption(f"Endpoint: `{endpoint.split('/')[2] if '//' in endpoint else '— ayarlanmadı —'}`")

gorev = st.radio("Görev", list(GOREVLER), horizontal=True)
metin = st.text_area("Metin", height=220, placeholder="Türkçe bir metin yapıştırın (en az 20 karakter)...")

if st.button("Çalıştır", type="primary", use_container_width=True):
    try:
        with st.spinner("Model düşünüyor..."):
            sonuc = calistir(gorev, metin, temperature, int(max_tokens), model)
    except ValueError as hata:
        st.warning(str(hata))
    except Exception as hata:  # noqa: BLE001
        st.error(f"Model çağrısı başarısız: {hata}")
    else:
        st.subheader("Sonuç")
        st.write(sonuc.icerik)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Girdi token", sonuc.girdi_token)
        k2.metric("Çıktı token", sonuc.cikti_token)
        k3.metric("Süre", f"{sonuc.sure_ms} ms")
        k4.metric("Maliyet", f"${maliyet_usd(sonuc.girdi_token, sonuc.cikti_token, girdi_fiyat, cikti_fiyat):.6f}")
        with st.expander("Ham sonuç"):
            st.json(sonuc.__dict__)

st.divider()
st.caption("Bu uygulama yapay zeka destekli kodlama araçlarıyla geliştirildi; ayrıntı README → 'AI kullanımı'.")
