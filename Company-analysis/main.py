#ライブラリ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy.polynomial.polynomial as P
from function import *
import time

#変数 
Codes = []
Dividend = []
L_earn_y = []
L_earn_a = []
L_earn = []
L_earn_akazi = []
L_earn_rate_counts = []
L_o_income_y = []
L_o_income = []
L_o_income_akazi = []
L_o_income_a = []
L_eps_y = []
L_eps = []
L_eps_akazi = []
L_eps_a = []
L_income_rate_y = []
L_income_rate = []
L_income_rate_a = []
L_income_rate_ave = []
L_selfcash_y = []
L_selfcash = []
L_selfcash_a = []
L_selfcash_ave = []
L_cf_akazi = []
L_cf_a = []
L_cash_a = []
L_cash_ave = []
L_one_div_a = []
L_div_dec_counts = []
L_one_div_counts = []
L_div_ten_a = []
L_div_ten_counts = []
L_div_ten_ave = []

#設定値
earn_rate = 0.3 #売上増減の激しさ何%以上をカウントするか
div_ten_rate = 50 #配当性向
div_rate = 10 #配当金 X以上(%)
file_name = "test.csv"

# chromedriverの設定
options = Options()
options.add_argument('--headless')

Url = "https://minkabu.jp/financial_item_ranking/dividend_yield?page={}".format(1)

browser = webdriver.Chrome(chrome_options=options)
browser.get(Url)
time.sleep(1)

elem_counts = browser.find_element(By.CLASS_NAME,"ico_search")
elem_counts = int(elem_counts.text[1:-1])
pages = elem_counts // 20

browser.quit()

for i in range(1,pages):

    Url_m = "https://minkabu.jp/financial_item_ranking/dividend_yield?page={}".format(i)
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(Url_m)
    elems = browser.find_elements(By.TAG_NAME,"tr")
    print(i)
    for i in range(2,22):
        xpath = "/html/body/div[1]/div[2]/div[3]/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[2]/table/tbody/tr[{}]/td[2]/a/div[1]".format(i)
        elem_codes = browser.find_element(By.XPATH,xpath)
        Codes.append(int(elem_codes.text))

        xpath = "/html/body/div[1]/div[2]/div[3]/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[2]/table/tbody/tr[{}]/td[4]".format(i)
        elem_divident = browser.find_element(By.XPATH,xpath)
        elem_divident = elem_divident.text.rstrip('%')
        Dividend.append(float(elem_divident))

    browser.quit()

    if Dividend[-1] <= div_rate:
        break

#pandasにまとめる
df =pd.DataFrame()
df["企業コード"] = Codes
df["配当金(%)"] = Dividend

for code in Codes:
    Earn = []
    O_income = []
    Eps = []
    R_income = []
    Selfcash = []
    Cf = []
    Cash = []
    One_div = []
    Div_ten = []
    print(code)

    Url = "https://irbank.net/{}/ir".format(code)

    browser = webdriver.Chrome(chrome_options=options)
    browser.get(Url)
    time.sleep(2)
    
    xpath = "//*[@id='chb']/h1/a"
    elem_balance = browser.find_element(By.XPATH,xpath)
    #決算ページ
    elem_balance.click()
    time.sleep(1)
    cur_url = browser.current_url
    page = cur_url + "/results"
    
    browser.get(page)
    time.sleep(3)

    #抽出表の場所を検索
    Name = []
    Title = []
    for i in range(1,40):
        try:
            name = "c_" + str(i)
            xpath_name ='//*[@id="{}"]/h2'.format(name)
            elem = browser.find_element(By.XPATH,xpath_name).text
            if "#" in elem:
                c = elem.index("#")
                elem = elem[:c]
            Name.append(name)
            Title.append(elem)
        except:
            pass   
    #売上高
    if "売上高" in Title:
        uriage = Title.index("売上高")
    elif "営業収益" in Title:
        uriage = Title.index("営業収益")
    elif "経常収益" in Title:
        uriage = Title.index("経常収益")
    elif "収益" in Title:
        uriage = Title.index("収益")

    elem = browser.find_element(By.ID,Name[uriage])
    elems_Earn = elem.find_elements(By.TAG_NAME,"dd")
    elems_year = elem.find_elements(By.TAG_NAME,"dt")

    earn_akazi = 0
    earn_rate_counts = 0
    i = -1
    for elem in elems_Earn:
        a = elem.text
        if "*" in a :
            a = a[1:]
        if a == "-":
            a = 0
        else:
            a = henkan(a)
        if a < 0 :
            earn_akazi -= 1
        Earn.append(a)
        try:
            if round(a/Earn[i]-1,2) > earn_rate or round(a/Earn[i]-1,2) < -earn_rate :
                earn_rate_counts += 1
        except:
            pass
        i += 1

    Year_earn = []
    for elem in elems_year:
        y = elem.text.split("/")
        Year_earn.append(int(y[0]))

    #営業利益
    if "営業利益" in Title:
        eigyourieki = Title.index("営業利益")
    elif "経常利益" in Title:
        eigyourieki = Title.index("経常利益")

    elem = browser.find_element(By.ID,Name[eigyourieki])
    elems = elem.find_elements(By.TAG_NAME,"dd")
    elems_year = elem.find_elements(By.TAG_NAME,"dt")

    o_income_akazi = 0
    for elem in elems:
        a = elem.text
        if "*" in a :
            a = a[1:]
        if a == "-":
            a = 0
        else:
            a = henkan(a)
        if a < 0 :
            o_income_akazi -= 1
        O_income.append(a)

    Year_inc = []
    for elem in elems_year:
        y = elem.text.split("/")
        Year_inc.append(int(y[0]))

    #EPS
    eps = Title.index("EPS")
    elem = browser.find_element(By.ID,Name[eps])
    elems_eps = elem.find_elements(By.TAG_NAME,"dd")
    elems_year = elem.find_elements(By.TAG_NAME,"dt")

    eps_akazi = 0
    for elem in elems_eps:
        a = elem.text
        if "*" in a :
            a = a[1:]
        if elem.text == "-":
            a = 0
        else:
            A = elem.text.split("円")
            a = float(A[0])
        if a < 0 :
            eps_akazi -= 1
        Eps.append(a)

    Year_eps = []
    for elem in elems_year:
        y = elem.text.split("/")
        Year_eps.append(int(y[0]))

    #営業利益率
    Year_income = []
    if "営業利益率" in Title:
        eigyouriekiritu = Title.index("営業利益率")
        elem = browser.find_element(By.ID,Name[eigyouriekiritu])
        elems = elem.find_elements(By.TAG_NAME,"dd")
        elems_year = elem.find_elements(By.TAG_NAME,"dt")
        
        for elem in elems:
            a = elem.text
            if "*" in a :
                a = a[1:]
            if elem.text == "-":
                a = 0
            else:
                A = elem.text.split("%")
                a = float(A[0])
            R_income.append(a)

        for elem in elems_year:
            y = elem.text.split("/")
            Year_income.append(int(y[0]))
    else:
        R_income.append(0)
        Year_income.append(0)


    #自己資本比率
    Year_selfcash = []
    if "自己資本比率" in Title:
        zikosihonhiritu = Title.index("自己資本比率")
        elem = browser.find_element(By.ID,Name[zikosihonhiritu])
        elems = elem.find_elements(By.TAG_NAME,"dd")
        elems_year = elem.find_elements(By.TAG_NAME,"dt")

        for elem in elems:
            a = elem.text
            if "*" in a :
                a = a[1:]
            if elem.text == "-":
                a = 0
            else:
                A = elem.text.split("%")
                a = float(A[0])
            Selfcash.append(a)

        for elem in elems_year:
            y = elem.text.split("/")
            Year_selfcash.append(int(y[0]))

    else:
        Selfcash.append(0)
        Year_selfcash.append(0)
    
#営業活動によるCF
    eigyoucf = Title.index("営業活動によるCF")
    elem = browser.find_element(By.ID,Name[eigyoucf])
    elems = elem.find_elements(By.TAG_NAME,"dd")
    elems_year = elem.find_elements(By.TAG_NAME,"dt")

    cf_akazi = 0
    for elem in elems:
        a = elem.text
        if "*" in a :
            a = a[1:]
        if elem.text == "-":
            a = 0
        else:
            a = elem.text
            a = henkan(a)
        if a < 0 :
            cf_akazi -= 1
        Cf.append(a)

    Year_cf = []
    for elem in elems_year:
        y = elem.text.split("/")
        Year_cf.append(int(y[0]))

    
    #現金等
    genkin = Title.index("現金等")
    elem = browser.find_element(By.ID,Name[genkin])
    elems = elem.find_elements(By.TAG_NAME,"dd")
    elems_year = elem.find_elements(By.TAG_NAME,"dt")

    for elem in elems:
        a = elem.text
        if "*" in a :
            a = a[1:]
        if a == "-":
            a = 0
        else:
            a = elem.text
            a = henkan(a)
        Cash.append(a)

    Year_cash = []
    for elem in elems_year:
        y = elem.text.split("/")
        Year_cash.append(int(y[0]))

    #一株配当
    hitokabu = Title.index("一株配当")
    elem = browser.find_element(By.ID,Name[hitokabu])
    elems = elem.find_elements(By.TAG_NAME,"dd")
    elems_year = elem.find_elements(By.TAG_NAME,"dt")

    one_div_counts = 0
    div_dec_counts = 0
    i = -1
    for elem in elems:
        a = elem.text
        if "*" in a :
            a = a[1:]
        if elem.text == "-":
            a = 0
        else:
            A = a.split("円")
            a = float(A[0])
        if a == 0 :
            one_div_counts =+ 1
        One_div.append(a)
        if a - One_div[i] < 0: 
            div_dec_counts += 1
        i += 1

    Year_one_div = []
    for elem in elems_year:
        y = elem.text.split("/")
        Year_one_div.append(int(y[0]))

    #配当性向
    Year_div_ten = []
    if "配当性向" in Title:
        haitouseikou = Title.index("配当性向")
        elem = browser.find_element(By.ID,Name[haitouseikou])
        elems = elem.find_elements(By.TAG_NAME,"dd")
        elems_year = elem.find_elements(By.TAG_NAME,"dt")

        div_ten_counts = 0
        for elem in elems:
            a = elem.text
            if "*" in a :
                a = a[1:]
            if elem.text == "-":
                a = 0
            else:
                A = elem.text.split("%")
                a = float(A[0])
            if a >= div_ten_rate:
                div_ten_counts += 1
            Div_ten.append(a)

        
        for elem in elems_year:
            y = elem.text.split("/")
            Year_div_ten.append(int(y[0]))
    else:
        Div_ten.append(0)
        Year_div_ten.append(0)
    browser.quit()
    
        #1次関数近似----------
    df_c =pd.DataFrame()
    df_c["年"] = Year_earn
    df_c["売上(億)"] = Earn

    df_d = pd.DataFrame()
    df_d["年"] = Year_inc
    df_d["営業利益(億)"] = O_income

    df_e =pd.DataFrame()
    df_e["年"] =Year_eps
    df_e["EPS"] = Eps

    df_income = pd.DataFrame()
    df_income["年"]=Year_income
    df_income["営業利益率"]=R_income

    df_selfcash = pd.DataFrame()
    df_selfcash["年"]=Year_selfcash
    df_selfcash["自己資本比率"]=Selfcash

    df_cf = pd.DataFrame()
    df_cf["年"] = Year_cf
    df_cf["営業活動によるCF"] = Cf

    df_cash = pd.DataFrame()
    df_cash["年"] = Year_cash
    df_cash["現金等"] = Cash

    df_one = pd.DataFrame()
    df_one["年"] = Year_one_div
    df_one["一株配当"] = One_div

    df_div = pd.DataFrame()
    df_div["年"] = Year_div_ten
    df_div["配当性向"] = Div_ten

    earn_a = P.polyfit(df_c["年"],df_c["売上(億)"],1)
    o_income_a = P.polyfit(df_d["年"],df_d["営業利益(億)"],1)
    eps_a = P.polyfit(df_e["年"],df_e["EPS"],1)
    income_a = P.polyfit(df_income["年"],df_income["営業利益率"],1)
    selfcash_a = P.polyfit(df_selfcash["年"],df_selfcash["自己資本比率"],1)
    cf_a = P.polyfit(df_cf["年"],df_cf["営業活動によるCF"],1)
    cash_a = P.polyfit(df_cash["年"],df_cash["現金等"],1)
    one_a = P.polyfit(df_one["年"],df_one["一株配当"],1)
    div_ten_a = P.polyfit(df_div["年"],df_div["配当性向"],1)

    #平均値
    income_rate_ave = round(sum(R_income)/len(R_income),2)
    selfcash_ave = round(sum(Selfcash)/len(Selfcash),2)
    cash_ave = round(sum(Cash)/len(Cash),2)
    div_ten_ave = round(sum(Div_ten)/len(Div_ten),2)

    #リストへの格納
    L_earn_y.append(Year_earn[-1])
    L_earn_a.append(round(earn_a[1],2))
    L_earn.append(Earn[-1])
    L_earn_akazi.append(earn_akazi)
    L_earn_rate_counts.append(earn_rate_counts)
    L_o_income_y.append(Year_inc[-1])
    L_o_income.append(O_income[-1])
    L_o_income_akazi.append(o_income_akazi)
    L_o_income_a.append(round(o_income_a[1],2))
    L_eps_y.append(Year_eps[-1])
    L_eps.append(Eps[-1])
    L_eps_akazi.append(eps_akazi)
    L_eps_a.append(round(eps_a[1],2))
    L_income_rate_y.append(Year_income[-1])
    L_income_rate.append(R_income[-1])
    L_income_rate_a.append(round(income_a[1],2))
    L_income_rate_ave.append(income_rate_ave)
    L_selfcash_y.append(Year_selfcash[-1])
    L_selfcash.append(Selfcash[-1])
    L_selfcash_a.append(round(selfcash_a[1],2))
    L_selfcash_ave.append(selfcash_ave)
    L_cf_akazi.append(cf_akazi)
    L_cf_a.append(round(cf_a[1],2))
    L_cash_a.append(round(cash_a[1],2))
    L_cash_ave.append(cash_ave)
    L_one_div_a.append(round(one_a[1],2))
    L_div_dec_counts.append(div_dec_counts)
    L_one_div_counts.append(one_div_counts)
    L_div_ten_a.append(round(div_ten_a[1],2))
    L_div_ten_counts.append(div_ten_counts)
    L_div_ten_ave.append(div_ten_ave)

#pandasに格納

df["売上年"] = L_earn_y
df["最新売上(億)"] = L_earn
df["売上傾向"] = L_earn_a
df["売上赤字の数"] = L_earn_akazi
df["売上増減{}以上".format(earn_rate)] =L_earn_rate_counts
df["営業利益年"] = L_o_income_y
df["営業利益(億)"] = L_o_income
df["利益赤字数"] = L_o_income_akazi
df["利益傾向"] = L_o_income_a
df["EPS年"] = L_eps_y
df["EPS(円)"]= L_eps
df["EPS 傾向"] = L_eps_a
df["EPS 赤字"] = L_eps_akazi
df["営業利益率 年"] = L_income_rate_y
df["営業利益率(%)"] = L_income_rate
df["営業利益率　傾向"] = L_income_rate_a
df["営業利益率　平均値"] = L_income_rate_ave
df["自己資本比率　年"] = L_selfcash_y
df["自己資本比率"] = L_selfcash
df["自己資本比率　傾向"] = L_selfcash_a
df["自己資本比率　平均値"] = L_selfcash_ave
df["営業CF 赤字数"] = L_cf_akazi
df["営業CF 傾向"] = L_cf_a
df["現金等 傾向"] = L_cash_a
df["現金等 平均値"] = L_cash_ave
df["一株配当　傾向"] = L_one_div_a
df["配当減の数"] = L_div_dec_counts
df["0円配当の数"] = L_one_div_counts
df["配当性向の傾向"] = L_div_ten_a
df["配当性向 {}%以上の数".format(div_ten_rate)] = L_div_ten_counts
df["配当性向 平均値"] = L_div_ten_ave

print(df)
#インデックスコード（一番左の行番号）
df.to_csv(file_name,index=False)