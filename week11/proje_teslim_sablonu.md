# Final projesi teslim şablonu

> Proje notun %30'u ([`proje/PROJE_ODEVI.md`](../proje/PROJE_ODEVI.md)). Teslim = **public GitHub reposu** + bu dosyanın doldurulmuş hali (`TESLIM.md`) repo kökünde + aynı dosyanın PDF çıktısı (≤ 6 sayfa) LMS'e. Son teslim tarihi ve sunum günü sınıf kanalında duyurulur; geç teslimde günlük −10 puan, en fazla 3 gün.

## Takım
| Ad Soyad | Üniversite / No | GitHub | Sorumluluk |
|---|---|---|---|
| | | | |
(1-3 kişi. Üç kişilik takımda kapsam büyür; rubrikte "kişi başı katkı" commit geçmişinden bakılır.)

## Proje
- **Ad:**
- **Tek cümle:** <kim> için <ne> yapan, <nasıl> çalışan bir yapay zeka uygulaması
- **Canlı demo URL:** (Streamlit Cloud / Container Apps / HF Spaces)
- **Demo video (≤2 dk):** (YouTube unlisted / Drive)
- **Kullanım senaryosu özeti:** `docs/kullanim_senaryosu.md` (Hafta 9 şablonu)
- **Model kartı:** `docs/model_karti.md` (Hafta 9 şablonu)

## Zorunlu bileşenler ve kanıtları (`PROJE_ODEVI.md` §3; her satır için kanıt dosyası)
| Beceri | Kullanıldı mı | Kanıt (dosya yolu) | Sayı |
|---|---|---|---|
| Tipli ve doğrulanmış çıktılar (H3) | | | doğrulayıcı sayısı |
| Sağlayıcıdan bağımsız istemci + maliyet ölçümü (H4) | | | $/istek, 2 sağlayıcı |
| RAG + hibrit arama + değerlendirme (H5) | | | sadakat / isabet |
| Spec + AGENTS.md ile ajan destekli geliştirme (H6) | | | test sayısı |
| Araç çağıran ajan + bütçe / MCP (H7) | | | araç sayısı, bütçe |
| Eval seti + CI + red team + tracing (H8) | | | x/n, kırılan saldırı |
| ROI + risk sınıfı + KVKK + insan onayı (H9) | | | geri ödeme ayı |

## Değerlendirme sonuçları (zorunlu)
- Eval seti: ___ vaka (zorlayıcı: ___), kaynak: ___, hakem: ___, tarih: ___ → geçen: ___/___
- (RAG varsa) sadakat ___ · kaynak isabeti ___
- Red team (≥8 saldırı; Hafta 12 eşleşmesi): ___/___ saldırı dayandı; eval setine eklenen vaka: ___; saldıran takım: ___
- **Ne bozuldu, nasıl düzelttiniz** (3-5 cümle; bu bölüm boşsa rubrikte dürüstlük puanı düşer):

## Maliyet
- İstek başına: $___ · aylık tahmin (___ istek/gün için): $___ · kullanılan kaldıraçlar: ___

## Güvenlik ve yönetişim
- EU AI Act risk sınıfı: ___ (gerekçe)
- İnsan onayı noktası: ___
- Kişisel veri: var/yok → KVKK notu
- Injection önlemleri: ___

## AI kullanımı (ders kuralı)
- Araçlar: ___
- Ajanın yazdığı / sizin yazdığınız: ___
- Ajanın en az bir hatası ve düzeltmeniz: ___

## Bilinen eksikler ve sonraki adım
- 3 madde
