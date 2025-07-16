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
    print(f"""  
{Beyaz} __  __            _     _            {Kırmızı} ____             {Sarı} _____           _  
{Beyaz}|  \/  | ___  _ __| |__ (_)_   _ ___  {Kırmızı}|  _ \  ___  ___  {Sarı}|_   _|__   ___ | |  
{Beyaz}| |\/| |/ _ \| '__| '_ \| | | | / __| {Kırmızı}| | | |/ _ \/ __|   {Sarı}| |/ _ \ / _ \| |  
{Beyaz}| |  | | (_) | |  | |_) | | |_| \__ \ {Kırmızı}| |_| | (_) \__ \   {Sarı}| | (_) | (_) | |  
{Beyaz}|_|  |_|\___/|_|  |_.__/|_|\__,_|___/ {Kırmızı}|____/ \___/|___/   {Sarı}|_|\___/ \___/|_|  
{Yeşil}  
Author: Morbius.os  
Instagram: @morbius.os  
Github: https://github.com/morbius-os{Bitir}""")  

def show_help_guide():  
    guide = f"""  
{Kırmızı}{Kalın}KOMUT SATIRI PARAMETRELERİ:{Bitir}  
  
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

# Diğer fonksiyonlar (ip_gecerli_mi, domain_denetle_ve_ip_al, ping_kontrol, http_kontrol, saldırı_udp, saldırı_tcp, saldırı_http, hedef_belirle_ve_saldırı_yap, hedefleri_dosyadan_oku) değişmediğinden yukarıdan alınacaktır.

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
            # mevcut interaktif hedef girişi devam eder
            pass

    # kod burada devam eder...

if __name__ == "__main__":
    ana()