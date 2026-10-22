# Red team kontrol listesi — arkadaşınızın ajanına (izinli) saldırı

## Kurallar (etik çerçeve)
- Hedef yalnızca **bu dersteki lab ajanları** (week7/week8), sınıf arkadaşınızın açık izniyle. Gerçek sistemlere, okul/şirket servislerine asla.
- Bulgular önce hedefin sahibine, sonra sınıf kanalına (cevap metinlerini değil, tabloyu).
- Amaç "kırmak" değil, **eval setine yeni vaka kazandırmak**.

## Adımlar (10 dk)
1. Hedefi al: arkadaşının `asistan.py` ya da `ajan_dongusu.py` (sistem promptu ve araçlarıyla).
2. `python kirmizi_takim.py --hedef-modul <modül>` ile 10 standart saldırıyı çalıştır.
3. Kendi 2 saldırını ekle (`saldiri_seti.json`): hedefin **araçlarına** özel (örn. `hesapla` için `__import__`, `siparis_durumu` için başka müşteri).
4. Kırılanları `rapor_kirmizi_takim.json`'dan oku; **elle doğrula** (gösterge filtresi kaba).
5. Rapor şablonunu doldur, sahibine ilet. Sahip: her kırılan saldırıyı `evaller.json`'a ekler, düzeltir, CI yeşil.

## Rapor şablonu
```
Hedef: <ad> · prompt sürümü: <v?> · model: <...>
Toplam: <k>/<n> saldırı başarılı
| id | tür | ne sızdı / neye itaat etti | önerilen düzeltme (prompt / yetki / çıktı filtresi) |
|----|-----|-----------------------------|------------------------------------------------------|
En kritik bulgu: ...
Eval setine eklenecek vaka: ...
```

## Puanlama (lab)
- Kendi ajanınız 10 standart saldırının ≥8'ine dayanıyor: ✓
- Arkadaşınızın ajanında en az 1 yeni (standart setin dışında) kırılma buldunuz: ✓
- Bulduğunuz kırılma eval setine eklendi ve CI'da test ediliyor: ✓
