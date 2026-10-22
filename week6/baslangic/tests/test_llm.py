"""Ağ gerektirmeyen testler. Çalıştır: pytest -q"""
from unittest.mock import MagicMock, patch

import pytest

import llm


def test_prompt_olustur_bilinen_gorev():
    mesajlar = llm.prompt_olustur("Özetle", "Bu yeterince uzun bir deneme metnidir, özetlenecek.")
    assert mesajlar[0]["role"] == "system" and "özetle" in mesajlar[0]["content"].lower()
    assert mesajlar[1]["role"] == "user"


def test_prompt_olustur_bilinmeyen_gorev():
    with pytest.raises(ValueError):
        llm.prompt_olustur("Çevir", "Bu yeterince uzun bir deneme metnidir.")


def test_prompt_olustur_kisa_metin():
    with pytest.raises(ValueError):
        llm.prompt_olustur("Özetle", "kısa")


def test_maliyet_usd():
    # 1000 girdi × $0.10/1M + 500 çıktı × $0.50/1M = 0.0001 + 0.00025
    assert llm.maliyet_usd(1000, 500, 0.10, 0.50) == pytest.approx(0.00035)
    assert llm.maliyet_usd(0, 0, 1, 1) == 0


def test_maliyet_negatif():
    with pytest.raises(ValueError):
        llm.maliyet_usd(-1, 0, 1, 1)


def test_calistir_mock():
    """Model çağrısını taklit et: ağ yok, yine de Sonuc doğru dolmalı."""
    sahte_yanit = MagicMock()
    sahte_yanit.choices = [MagicMock(message=MagicMock(content="  Özet.  "))]
    sahte_yanit.usage = MagicMock(prompt_tokens=42, completion_tokens=7)
    sahte_istemci = MagicMock()
    sahte_istemci.chat.completions.create.return_value = sahte_yanit
    with patch.object(llm, "istemci", return_value=sahte_istemci):
        s = llm.calistir("Özetle", "Bu yeterince uzun bir deneme metnidir, özetlenecek.", model="test-model")
    assert s.icerik == "Özet." and s.girdi_token == 42 and s.cikti_token == 7 and s.model == "test-model"
    sahte_istemci.chat.completions.create.assert_called_once()
