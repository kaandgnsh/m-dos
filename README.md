# M-DOS2 | Gelişmiş Python Tabanlı DOS Saldırı Aracı

Bu proje, eğitim ve test amaçlı geliştirilmiş **çok fonksiyonlu bir DOS (Denial of Service) aracı**dır. Python ile yazılmıştır ve hem **interaktif mod** hem de **komut satırı parametre modu** ile çalışabilir.

## Özellikler

✅ UDP / TCP / HTTP Flood saldırıları  
✅ IP veya Domain hedefleme  
✅ Çoklu hedef (dosyadan alma)  
✅ Ping ve HTTP kontrolü  
✅ Otomatik domain IP çözümleme  
✅ Loglama ve özelleştirilebilir log dosyası adı  
✅ Site çökme takibi (HTTP modunda)  
✅ Saldırı sonrası özet rapor oluşturma  
✅ Proxy desteği (opsiyonel)  
✅ Canlı istatistik paneli  
✅ Renkli terminal çıktısı  
✅ Kullanıcı dostu interaktif arayüz  
✅ Komut satırından tüm parametrelerle çalıştırılabilir

---

## Kurulum

```bash
git clone https://github.com/morbius-os/m-dos

cd m-dos

cd m-dos

python3 m-dos.py
```


> **Not**: `termcolor`, `requests` gibi modüller gereklidir.

---

## Kullanım

### Interaktif Mod:

```bash
python3 mdos2.py
```

- Hedef IP/domain girin
- Port seçin
- Saldırı süresi ve thread sayısını girin
- Saldırı tipi seçin (UDP, TCP, HTTP)
- Loglama isteğe bağlı

### Parametre Modu:

```bash
python3 mdos2.py -t hedefler.txt -p 80 --type udp -d 60 -T 8 --log --logfile kayit.txt
```

#### Parametre Açıklamaları:

| Parametre     | Açıklama |
|---------------|----------|
| `-t` / `--targets` | Hedefleri içeren dosya |
| `-p` / `--port`    | Port numarası (tüm portlar için 1) |
| `--type`           | Saldırı tipi (udp / tcp / http) |
| `-d` / `--duration`| Saldırı süresi (saniye) |
| `-T` / `--threads` | Thread sayısı |
| `--log`            | Loglama aktif eder |
| `--logfile`        | Log dosyasının adı |
| `--proxy`          | Proxy desteği |
| `--report`         | Saldırı sonrası rapor oluşturur |

Yardım kılavuzunu görmek için:

```bash
python3 mdos2.py -h
```

---

## Örnek Kullanım

```bash
python3 mdos2.py -t hedefler.txt -p 80 --type http -d 60 -T 10 --log --logfile log.txt --report
```

---

## Uyarı ⚠️

> Bu araç yalnızca **eğitim ve test** amaçlıdır. Yetkisiz sistemlere saldırı **suçtur** ve **yasal sorumluluk doğurur**. Geliştirici hiçbir sorumluluk kabul etmez.

---

## Geliştirici

**KaanDGN**  
📷 Instagram: [@kaandgn.sh](https://instagram.com/kaandgn.sh)  
💻 Github: [github.com/kaandgn.sh](https://github.com/kaandgn-sh)
