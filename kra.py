import mechanize
from bs4 import BeautifulSoup 
import ssl

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Firefox')]


# KRA WEBSITE DETAILS
URL = "https://www.nsekra.com/"
CAPTCHA_CODE = "lblDynamicCode"
PAN_ID = "txtPan"
CAPTCHA_TEXT = "txtImageBox"
SUBMIT_ID = "btnAllKRA"


# EXTRACT TEXT VALUE
PAN_NUMBER = "lblpan_m"
PAN_NAME = "lblname_m"
KRA_NAME = "lblKra_name"
KYC_DATE = "lblkyc_date"
KYC_STATUS = "lblkyc_status"
KYC_MODE = "lblKycMode"
IPV_FLAG = "lblIpvFlag"


def scrap_kra(pan_number):   
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
    # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context 

        
    translated_text = br.open(URL)
    translated_text = translated_text.read().decode('UTF-8')
    soup = BeautifulSoup(translated_text,"html.parser")
    div_content = soup.find('span', {'id' : CAPTCHA_CODE})
    tempForm = br.forms()[0]
    br.select_form(nr=0)
    br.form[PAN_ID] = pan_number
    br.form[CAPTCHA_TEXT] = div_content.text
    br.form.set_all_readonly(False)
    sub = br.submit(id=SUBMIT_ID)
    sub = sub.read().decode('UTF-8')
    soup = BeautifulSoup(sub,"html.parser")
    return extract_kyc(soup)

def extract_kyc(soup):
    pan_number = soup.find(id=PAN_NUMBER)
    pan_name = soup.find(id=PAN_NAME)
    kra_name = soup.find(id=KRA_NAME)
    kyc_date = soup.find(id=KYC_DATE)
    kyc_status = soup.find(id=KYC_STATUS)
    kyc_mode = soup.find(id=KYC_MODE)
    ipv = soup.find(id=IPV_FLAG)

    # print(pan_number.text)
    # print(pan_name.text)
    # print(kra_name.text)
    # print(kyc_date.text)
    # print(kyc_status.text)
    # print(kyc_mode.text)
    # print(ipv.text)
    return { 
        "status_code":1,
        "pan_number" : pan_number.text,
        "pan_name"   : pan_name.text,
        "kra_name" :kra_name.text,
        "kyc_date" : kyc_date.text,
        "kyc_status":kyc_status.text,
        "kyc_mode":kyc_mode.text,
        "ipv":ipv.text
         }


# if __name__ == "__main__":
#     scrap_kra("BFJPG1385P")
