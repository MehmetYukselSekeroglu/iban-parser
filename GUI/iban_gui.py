import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter.font import Font


def CheckIsOk(raw_iban):
    country_number = raw_iban[0] + raw_iban[1]
    country_number = country_number.upper()


    if country_number == "TR" and len(raw_iban) == 26:
        return True
        
    else:
        return False



def iban_parametres(iban_1):
    global control_number_global 
    global bank_code_local
    global rezerve_code  
    if True:
        try:
            control_number_global = iban_1[2] + iban_1[3]
            bank_code_local = iban_1[4] + iban_1[5] + iban_1[6] + iban_1[7] + iban_1[8]
            rezerve_code = iban_1[9]
            account_number = iban_1[10:26]
            sube_kodu = iban_1[10:14]
            müşteri_nosu_raw = iban_1[13:22]
            hesap_eki_kodu = iban_1[22:]
        except Exception:
           pass
        if bank_code_local == "00001":
            bank_name = "TC Merkez Bankası"
        elif bank_code_local == "00004":
            bank_name = "İller Bankası"
        elif bank_code_local == "00010":
            bank_name = "Ziraat Bankası"
        elif bank_code_local == "00012":
            bank_name = "Halkbank"
        elif bank_code_local == "00015":
            bank_name = "Vakıflar Bankası"
        elif bank_code_local == "00017":
            bank_name = "Kalkınma Bankası"
        elif bank_code_local == "00029":
            bank_name = "Birleşik Fon Bankası"
        elif bank_code_local == "00032":
            bank_name = "Türk Ekonomi Bankası"
        elif bank_code_local == "00046":
            bank_name = "Akbank"
        elif bank_code_local == "00059":
            bank_name = "Şekerbank"
        elif bank_code_local == "00062":
            bank_name = "Garanti Bankası"
        elif bank_code_local == "00064":
            bank_name = "İş Bankası"
        elif bank_code_local == "00067":
            bank_name = "Yapı ve Kredi Bankası"
        elif bank_code_local == "00099":
            bank_name = "ING Bank"
        elif bank_code_local == "00100":
            bank_name = "Adabank"
        elif bank_code_local == "00111":
            bank_name = "Finansbank"
        elif bank_code_local == "00123":
            bank_name = "HSBC"
        elif bank_code_local == "00132":
            bank_name = "Takasbank"
        elif bank_code_local == "00134":
            bank_name = "Denizbank"
        elif bank_code_local == "00135":
            bank_name = "Anadolu Bank"
        elif bank_code_local == "00137":
            bank_name = "Rabobank"
        elif bank_code_local == "00138":
            bank_name = "Dilerbank"
        elif bank_code_local == "00139":
            bank_name = "GSD Bank"
        elif bank_code_local == "00141":
            bank_name = "Nurol Yatırım Bankası"
        elif bank_code_local == "00142":
            bank_name = "Bankpozitif Kredi ve Kalkınma Bankası"
        elif bank_code_local == "00143":
            bank_name = "Aktif Yatırım Bankası"
        elif bank_code_local == "00146":
            bank_name = "Odea Bank"
        elif bank_code_local == "00147":
            bank_name = "Bank of Tokyo-Mitsubishi UFJ Turkey"
        elif bank_code_local == "00203":
            bank_name = "Albaraka Türk Katılım Bankası"
        elif bank_code_local == "00205":
            bank_name = "Kuveyt Türk Katılım Bankası"
        elif bank_code_local == "00206":
            bank_name = "Türkiye Finans Katılım Bankası"
        elif bank_code_local == "00209":
            bank_name = "Ziraat Katılım Bankası"
        elif bank_code_local == "00210":
            bank_name = "Vakıf Katılım Bankası"
        elif bank_code_local == "00806":
            bank_name = "Merkezi Kayıt Kuruluşu"
        elif bank_code_local == "00109":
            bank_name = "ICBC Turkey Bank"
        else:
            bank_name="Tespit edilemedi"
            #else_proc = "0"
            #return else_proc
        
        ReturnData = [control_number_global, bank_code_local,bank_name, account_number, sube_kodu, müşteri_nosu_raw, hesap_eki_kodu]
        return ReturnData

        
def ScarpIbanInfo(iban):
    scrap_url=f"https://iban.gen.tr/iban-cozumleme-ve-dogrulama?kod={iban}"
    try:
        sorgulama=requests.get(url=scrap_url,timeout=10)
        ayıklamanmıs_data=BeautifulSoup(sorgulama.content,"html.parser")
        data_1=ayıklamanmıs_data.find(attrs={"class":"table table-bordered table-sm table-resolve-verify"})
        data_1=data_1.find_all('td')
        hata_durumu=False
        try:
            iban_il=data_1[2]
            iban_ilce=data_1[1]
        except Exception:
            iban_il="<td>Alınamadı</td>"
            iban_ilce="<td>Alınamadı</td>"
    except Exception:
        iban_il="<td>Alınamadı</td>"
        iban_ilce="<td>Alınamadı</td>"
    
    iban_il = str(iban_il)
    iban_ilce = str(iban_ilce)

    iban_il = iban_il.strip('<td>')
    iban_il= iban_il.strip('</td>')
    
    iban_ilce= iban_ilce.strip('<td>')
    iban_ilce = iban_ilce.strip('</td>')
    
    
    return [iban_il, iban_ilce]





def ParseIban():
        raw_iban = iban_input.get()
        raw_iban = str(raw_iban)
        raw_iban = raw_iban.replace(" ", "")
        if len(raw_iban) == 0 or len(raw_iban) > 30:
            iban_output_label["text"] = "Hata: iban boş bırakılamaz!"
            iban_output_label["fg"] = "red"
            
            return ""
        if CheckIsOk(raw_iban):
            standart_parameters = iban_parametres(raw_iban)
            web_crawling = ScarpIbanInfo(raw_iban)

            Output = f"""İşlem: Başarılı
Standart bilgiler:
Banka adı: {standart_parameters[2]}
Yerel banka kodu: {standart_parameters[1]}
Şube kodu: {standart_parameters[4]}
Hesap numarası: {standart_parameters[3]}
Global kontrol kodu: {standart_parameters[0]}
Müşteri numarası: {standart_parameters[5]}
Hesap ek numarası: {standart_parameters[6]}

İl & ilçe bilgileri:
Kayıtlı olduğu il: {web_crawling[0]}
Kayıtlı olduğu ilçe: {web_crawling[1]}"""
            iban_output_label["text"] = Output
            iban_output_label["fg"] = StandartColor
        
        
        else:
            iban_output_label["text"] = "Hata: iban geçersizdir lütfen kontrol ediniz!"
            iban_output_label["fg"] = "red"

        iban_input.delete(0, len(iban_input.get()))





APP_NAME = "iban parser"
CORP_NAME = "PRIME"

RootWindow = tk.Tk()
RootWindow.title(CORP_NAME+" | "+ APP_NAME)
RootWindow.geometry("900x500+200+50")

TitleFonts = Font(family="arial",size="16",)
StandartFonts = Font(family="arial",  size="12",)   
StandartColor = "#0a1e4a"
info_fonts = Font(family="arial", size="9")


IBanBilgi = tk.Label( text="iban: ", font=TitleFonts, fg=StandartColor)
IBanBilgi.place(relx=0.01, rely=0.01)

iban_input = tk.Entry()
iban_input.place(relx=0.15, rely=0.02 ,relheight=0.05, relwidth=0.5)


GetParseIban_button = tk.Button(text="çözümle", command=ParseIban)
GetParseIban_button.place(relx=0.01, rely=0.08)


iban_output_label = tk.Label( text="", justify="left")
iban_output_label.place(relx=0.01, rely=0.2)


ek_gösterge = tk.Label(text=f"Powered by {CORP_NAME}", justify="left", font=info_fonts)
ek_gösterge.place(relx=0.01, rely=0.9)


RootWindow.mainloop()