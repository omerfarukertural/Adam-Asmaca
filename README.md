# Adam Asmaca (Tkinter)

Modern, estetik ve zengin özellikli bir Adam Asmaca oyunu.

## Özellikler
- **Modern ve sade arayüz**: Açık mavi arka plan, siyah yazılar, kutusuz ve bütünleşik tasarım
- **Türkçe karakter desteği**: Ç, Ş, İ, Ğ, Ü, Ö harfleriyle tam uyum
- **Zorluk seviyeleri**: Kolay (5dk), Orta (4dk), Zor (3dk) – her bölümde 10 kelime
- **Bölüm bazlı süre**: Her bölüm için toplam süre, kelime başına süre yok
- **Skor sistemi**: Doğru harf +5, yanlış harf -2 (sıfırın altına inemez), kelimeyi bulunca +20, kalan süreye bonus
- **İpucu sistemi**: Her bölümde sınırlı sayıda harf açma hakkı
- **Yüksek skor tablosu**: Kalıcı, ana menüden sıfırlanabilir
- **Oyun istatistikleri**: Oynanan, kazanılan, kaybedilen oyun ve toplam skor
- **Ses efektleri**: Doğru/yanlış tahmin, kaybetme ve bölüm sonunda kazanma sesi
- **Çoklu dil desteği**: Türkçe ve İngilizce kelime havuzları
- **Ana menüye dönme**: Oyun sırasında istediğin zaman ana menüye dönebilirsin

## Kurulum
1. **Python 3.8+** yüklü olmalı.
2. Gerekli paketleri yükle:
   ```bash
   pip install pygame
   ```
3. Proje klasörüne aşağıdaki ses dosyalarını ekle:
   - `snd_correct.wav` (doğru tahmin)
   - `snd_wrong.wav` (yanlış tahmin)
   - `snd_win.wav` (bölüm sonunda kazanma)
   - `snd_lose.wav` (kaybetme)
   (Ses dosyalarını bulamazsan, oyun sessiz çalışır.)

## Çalıştırma
Ana dizinde:
```bash
python adam_asmaca.py
```
veya
```bash
python3 adam_asmaca.py
```

## Ekran Görüntüsü
> ![Adam Asmaca Ekran Görüntüsü](ekran_goruntusu.png)

## Katkı ve Lisans
- Her türlü katkıya açıktır.
- MIT Lisansı ile lisanslanmıştır.

---
**Hazırlayan:** [Senin Adın] 