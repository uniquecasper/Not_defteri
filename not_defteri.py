import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from datetime import datetime
import json, os

# ── RENKLER & FONT ──────────────────────────────────────────
BG      = "#0f0f1a"
KART    = "#1a1a2e"
VURGU   = "#e040fb"
VURGU2  = "#00e5ff"
YAZI    = "#f0f0ff"
GRI     = "#2a2a3e"
YESIL   = "#b2ff59"
KIRMIZI = "#ff5252"
TURUNCU = "#ffab40"
CAMGOB  = "#69f0ae"
MAVIS   = "#90caf9"

BASLIK_FONT = ("Courier New", 18, "bold")
ETIKET_FONT = ("Courier New", 9,  "bold")
GIRIS_FONT  = ("Courier New", 11)
BUTON_FONT  = ("Courier New", 9,  "bold")
LISTE_FONT  = ("Courier New", 10)
DURUM_FONT  = ("Courier New", 9,  "bold")
TARIH_FONT  = ("Courier New", 8)

DOSYA    = "notlar.txt"
SIFRE_D  = "sifre.txt"

notlar = {}  # { baslik: {"metin": ..., "tarih": ...} }

# ── DOSYA İŞLEMLERİ ─────────────────────────────────────────
def kaydet_dosya():
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(notlar, f, ensure_ascii=False, indent=2)

def oku_dosya():
    global notlar
    try:
        with open(DOSYA, "r", encoding="utf-8") as f:
            ham = json.load(f)
        notlar = {}
        for k, v in ham.items():
            if isinstance(v, str):
                notlar[k] = {"metin": v, "tarih": ""}
            else:
                notlar[k] = v
    except:
        notlar = {}

# ── ŞİFRE İŞLEMLERİ ─────────────────────────────────────────
def sifre_oku():
    try:
        with open(SIFRE_D, "r") as f:
            return f.read().strip()
    except:
        return None

def sifre_yaz(s):
    with open(SIFRE_D, "w") as f:
        f.write(s)

# ── KİLİT EKRANI ─────────────────────────────────────────────
def kilit_ekrani_ac():
    kilit = tk.Toplevel()
    kilit.title("🔒 Giriş")
    kilit.configure(bg=BG)
    kilit.geometry("300x220")
    kilit.resizable(False, False)
    kilit.grab_set()
    kilit.protocol("WM_DELETE_WINDOW", lambda: pencere.destroy())

    # Üst bar
    tk.Frame(kilit, bg=VURGU, height=3).pack(fill="x")

    tk.Label(kilit, text="🔒 NOT DEFTERİM", font=("Courier New", 14, "bold"),
             bg=BG, fg=VURGU).pack(pady=(18, 4))

    hata_lbl = tk.Label(kilit, text="", font=DURUM_FONT, bg=BG, fg=KIRMIZI)
    hata_lbl.pack()

    kayitli = sifre_oku()
    if not kayitli:
        hata_lbl.config(text="İlk kullanım: Şifre belirleyin.", fg=VURGU2)

    sifre_var = tk.StringVar()
    sifre_kutu = tk.Entry(kilit, textvariable=sifre_var, show="●",
                          font=("Courier New", 14), bg=GRI, fg=YAZI,
                          insertbackground=VURGU, relief="flat",
                          bd=8, justify="center")
    sifre_kutu.pack(padx=30, fill="x", pady=8)
    sifre_kutu.focus()

    def giris():
        girilen = sifre_var.get()
        kayitli2 = sifre_oku()
        if not kayitli2:
            if len(girilen) < 4:
                hata_lbl.config(text="En az 4 karakter!", fg=KIRMIZI)
                return
            sifre_yaz(girilen)
            kilit.destroy()
            pencereyi_ac()
        else:
            if girilen == kayitli2:
                kilit.destroy()
                pencereyi_ac()
            else:
                hata_lbl.config(text="❌ Yanlış şifre!", fg=KIRMIZI)
                sifre_kutu.delete(0, tk.END)

    def sifirla():
        if messagebox.askyesno("Sıfırla", "Şifre sıfırlansın mı?\n⚠ Tüm notlar silinecek!"):
            if os.path.exists(SIFRE_D): os.remove(SIFRE_D)
            if os.path.exists(DOSYA):   os.remove(DOSYA)
            hata_lbl.config(text="Sıfırlandı. Yeni şifre belirleyin.", fg=VURGU2)
            sifre_kutu.delete(0, tk.END)

    sifre_kutu.bind("<Return>", lambda e: giris())

    btn_f = tk.Frame(kilit, bg=BG)
    btn_f.pack(pady=4)

    tk.Button(btn_f, text="GİRİŞ", command=giris,
              font=BUTON_FONT, bg=VURGU2, fg=BG,
              relief="flat", cursor="hand2", padx=14, pady=5).pack(side="left", padx=4)

    tk.Button(btn_f, text="SIFIRLA", command=sifirla,
              font=BUTON_FONT, bg=KIRMIZI, fg=BG,
              relief="flat", cursor="hand2", padx=10, pady=5).pack(side="left", padx=4)

# ── ANA PENCEREYİ AÇ ─────────────────────────────────────────
def pencereyi_ac():
    oku_dosya()
    listeyi_guncelle()
    ana_cerceve.pack(fill="both", expand=True, padx=18, pady=8)
    alt_bar.pack(fill="x", side="bottom")
    durum_guncelle("✅ Giriş yapıldı. Hoş geldiniz!", VURGU2)

# ── LİSTEYİ GÜNCELLE ─────────────────────────────────────────
def listeyi_guncelle():
    liste.delete(0, tk.END)
    for baslik in notlar:
        tarih = notlar[baslik].get("tarih", "")
        liste.insert(tk.END, "  📌 " + baslik)
    tarih_goster()

def tarih_goster():
    secim = liste.curselection()
    if secim:
        baslik = liste.get(secim).replace("  📌 ", "")
        t = notlar.get(baslik, {}).get("tarih", "")
        tarih_lbl.config(text=("🕐 " + t) if t else "")
    else:
        tarih_lbl.config(text="")

# ── BUTON FONKSİYONLARI ──────────────────────────────────────
def kaydet():
    baslik = baslik_kutu.get().strip()
    icerik = metin_kutu.get("1.0", tk.END).strip()
    if not baslik:
        messagebox.showwarning("Uyarı", "Başlık boş olamaz!")
        return
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
    notlar[baslik] = {"metin": icerik, "tarih": tarih}
    kaydet_dosya()
    listeyi_guncelle()
    tarih_lbl.config(text="🕐 " + tarih)
    durum_guncelle("✅ Kaydedildi → " + baslik, VURGU2)

def oku_not():
    secim = liste.curselection()
    if not secim:
        durum_guncelle("⚠ Listeden bir not seçin.", TURUNCU)
        return
    baslik = liste.get(secim).replace("  📌 ", "")
    baslik_kutu.delete(0, tk.END)
    baslik_kutu.insert(0, baslik)
    metin_kutu.delete("1.0", tk.END)
    metin_kutu.insert("1.0", notlar[baslik]["metin"])
    t = notlar[baslik].get("tarih", "")
    tarih_lbl.config(text=("🕐 " + t) if t else "")
    durum_guncelle("📖 Okunuyor → " + baslik, VURGU)

def yeni():
    liste.selection_clear(0, tk.END)
    baslik_kutu.delete(0, tk.END)
    metin_kutu.delete("1.0", tk.END)
    tarih_lbl.config(text="")
    durum_guncelle("✨ Yeni not...", GRI)
    baslik_kutu.focus()

def sil():
    secim = liste.curselection()
    if not secim:
        durum_guncelle("⚠ Listeden bir not seçin.", TURUNCU)
        return
    baslik = liste.get(secim).replace("  📌 ", "")
    if messagebox.askyesno("Sil", f'"{baslik}" silinsin mi?'):
        del notlar[baslik]
        kaydet_dosya()
        listeyi_guncelle()
        baslik_kutu.delete(0, tk.END)
        metin_kutu.delete("1.0", tk.END)
        tarih_lbl.config(text="")
        durum_guncelle("🗑 Silindi → " + baslik, KIRMIZI)

def disari_aktar():
    dosya_yolu = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Dosyası", "*.json")],
        initialfile="notlar_yedek.json",
        title="Notları Dışa Aktar"
    )
    if not dosya_yolu: return
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        json.dump(notlar, f, ensure_ascii=False, indent=2)
    durum_guncelle("📤 Dışa aktarıldı → " + os.path.basename(dosya_yolu), TURUNCU)

def iceri_aktar():
    dosya_yolu = filedialog.askopenfilename(
        filetypes=[("JSON Dosyası", "*.json")],
        title="Notları İçe Aktar"
    )
    if not dosya_yolu: return
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            gelen = json.load(f)
        for k, v in gelen.items():
            if isinstance(v, str):
                notlar[k] = {"metin": v, "tarih": ""}
            else:
                notlar[k] = v
        kaydet_dosya()
        listeyi_guncelle()
        durum_guncelle("📥 İçe aktarıldı!", CAMGOB)
    except:
        messagebox.showerror("Hata", "Geçersiz dosya!")

def kilitle():
    ana_cerceve.pack_forget()
    alt_bar.pack_forget()
    kilit_ekrani_ac()

def durum_guncelle(mesaj, renk):
    durum_etiketi.config(text=mesaj, fg=renk)

def buton_yap(parent, yazi, komut, renk, w=None):
    b = tk.Button(parent, text=yazi, command=komut,
                  font=BUTON_FONT, bg=renk, fg=BG,
                  activebackground=YAZI, activeforeground=BG,
                  relief="flat", cursor="hand2", pady=5)
    if w: b.config(width=w)
    return b

# ── ANA PENCERE ───────────────────────────────────────────────
pencere = tk.Tk()
pencere.title("✦ Not Defterim")
pencere.configure(bg=BG)
pencere.geometry("560x640")
pencere.resizable(False, False)

# Üst çizgi
tk.Frame(pencere, bg=VURGU, height=4).pack(fill="x")

# Başlık
tk.Label(pencere, text="✦ NOT DEFTERİM ✦",
         font=BASLIK_FONT, bg=BG, fg=VURGU).pack(pady=(14, 2))
tk.Label(pencere, text="─" * 50, font=("Courier New", 8),
         bg=BG, fg=GRI).pack()

# Ana çerçeve (giriş yapılınca gösterilecek)
ana_cerceve = tk.Frame(pencere, bg=BG)

# SOL SÜTUN
sol = tk.Frame(ana_cerceve, bg=BG)
sol.pack(side="left", fill="both", expand=True)

tk.Label(sol, text="BAŞLIK", font=ETIKET_FONT, bg=BG, fg=VURGU2).pack(anchor="w")
baslik_kutu = tk.Entry(sol, font=GIRIS_FONT, bg=GRI, fg=YAZI,
                       insertbackground=VURGU, relief="flat", bd=6)
baslik_kutu.pack(fill="x", pady=(2, 8))

tk.Label(sol, text="NOT İÇERİĞİ", font=ETIKET_FONT, bg=BG, fg=VURGU2).pack(anchor="w")
metin_cerceve = tk.Frame(sol, bg=VURGU, bd=1)
metin_cerceve.pack(fill="x", pady=(2, 2))
metin_kutu = tk.Text(metin_cerceve, font=GIRIS_FONT, bg=GRI, fg=YAZI,
                     insertbackground=VURGU, relief="flat",
                     height=8, bd=6, wrap="word")
metin_kutu.pack(fill="x")

tarih_lbl = tk.Label(sol, text="", font=TARIH_FONT, bg=BG, fg=VURGU2)
tarih_lbl.pack(anchor="w", pady=(2, 6))

# Butonlar - 1. satır
bf1 = tk.Frame(sol, bg=BG)
bf1.pack(fill="x", pady=2)
for yazi, komut, renk in [
    ("💾 KAYDET", kaydet,    VURGU2),
    ("📖 OKU",    oku_not,   VURGU),
    ("✨ YENİ",   yeni,      YESIL),
    ("🗑 SİL",    sil,       KIRMIZI),
]:
    buton_yap(bf1, yazi, komut, renk).pack(side="left", expand=True, fill="x", padx=2)

# Butonlar - 2. satır
bf2 = tk.Frame(sol, bg=BG)
bf2.pack(fill="x", pady=2)
for yazi, komut, renk in [
    ("📤 DIŞA AKTAR",  disari_aktar, TURUNCU),
    ("📥 İÇE AKTAR",   iceri_aktar,  CAMGOB),
    ("🔒 KİLİTLE",     kilitle,      MAVIS),
]:
    buton_yap(bf2, yazi, komut, renk).pack(side="left", expand=True, fill="x", padx=2)

# SAĞ SÜTUN
sag = tk.Frame(ana_cerceve, bg=BG)
sag.pack(side="right", fill="y", padx=(12, 0))

tk.Label(sag, text="NOTLARIM", font=ETIKET_FONT, bg=BG, fg=VURGU2).pack(anchor="w")
liste_cerceve = tk.Frame(sag, bg=VURGU, bd=1)
liste_cerceve.pack(fill="y", expand=True)

kaydirma = tk.Scrollbar(liste_cerceve)
kaydirma.pack(side="right", fill="y")

liste = tk.Listbox(liste_cerceve, font=LISTE_FONT,
                   bg=KART, fg=YAZI,
                   selectbackground=VURGU, selectforeground=BG,
                   relief="flat", bd=0, width=18, height=18,
                   yscrollcommand=kaydirma.set, activestyle="none")
liste.pack(side="left", fill="y")
kaydirma.config(command=liste.yview)
liste.bind("<Double-Button-1>", lambda e: oku_not())
liste.bind("<<ListboxSelect>>", lambda e: tarih_goster())

# Alt durum çubuğu
alt_bar = tk.Frame(pencere, bg=KART, height=28)
durum_etiketi = tk.Label(alt_bar, text="Hazır.", font=DURUM_FONT,
                          bg=KART, fg=GRI, anchor="w", padx=10)
durum_etiketi.pack(fill="x", pady=4)

# ── BAŞLAT ───────────────────────────────────────────────────
kilit_ekrani_ac()
pencere.mainloop()
