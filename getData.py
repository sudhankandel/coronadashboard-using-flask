import requests
import json,schedule,time
import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import itertools
import statsmodels.api as sm

response_country = requests.get("https://disease.sh/v3/covid-19/countries")
data_dic = response_country.json()


def convert(a):
    c = {'०':'0','१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9',',':','}
    for key,value in c.items():
        a = a.replace(key,value)
    return a



    
def nepal_data():
    response = requests.get('https://coronanepal.live/')
    soup = BeautifulSoup(response.text, 'html.parser')
    get_table_1 = soup.findAll('div',attrs={'class':'col-lg-3'})
    get_table_1=get_table_1[2]
    get_table_data_1 = get_table_1.find_all(["h4",'h1'])
    keys=['tested_total','total_cases','total_death','total_recover']
    data=[]
    for i in range(1,8,2):
        data.append(convert(get_table_data_1[i+1].text))
    return dict(zip(keys,data))
    
def global_news_update():
    url = "https://www.worldometers.info/coronavirus/"
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    urls = []
    heading = []
    for news in soup.find_all('div', class_='news_post'):
        heading.append(news.text)
        for url in news.find_all('a', class_='news_source_a'):
            urls.append(url.get('href'))
    clear_data = []
    for i in heading:
    #     clean=i.str.replace('[^\w\s]'," ")
        clean = re.sub(r'[\n]', ' ', i)
        clear_data.append(clean)
    final_news = []
    for i in clear_data:
        final_news.append(i.replace('source', ''))
    df_news_zipped = list(zip(final_news, urls))
    df_news = pd.DataFrame(df_news_zipped, columns=['Title', 'Source'])
    news = []
    for i, title in enumerate(df_news['Title']):
        news.append({'id':i, 'title':title})
    return heading
def global_table():
    data_dics = sorted(data_dic, key=lambda x: x['cases'], reverse=True)
    dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    wanted_keys = ("country", "cases", "deaths","recovered","continent")
    data = []
    for i in data_dics:
        filter_data = dictfilt(i, wanted_keys)
        data.append(filter_data)
    return data

def global_update():
    table_data=global_table()
    df=pd.DataFrame(table_data).sum()
    return [df.cases,df.deaths,df.recovered]

def TimeSeries(country):
    response = requests.get('https://pomber.github.io/covid19/timeseries.json')
    data = response.json()
    combo = data.keys()
    keys = []
    for i in combo:
        keys.append(i)
    if country=='':
        coun='China'
        aa = data[coun]
    else:
        aa=data[country]
    date = []
    confirm = []
    death = []
    recover = []
    for i in aa:
        date.append(i['date'])
        confirm.append(i['confirmed'])
        death.append(i['deaths'])
        recover.append(i['recovered'])
    time_data = {'date': date,
                 'confirm': confirm,
                 'death': death,
                 'recover': recover,
                 'combo':keys}
    return time_data

def Nepal_table():
    response = requests.get('https://coronanepal.live/')
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    list_of_rows = []
    for tr in table.find_all('tr'):
        list_of_cells = []
        for td in tr.find_all(['td', 'th']):
            text = td.text
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    df = pd.DataFrame(list_of_rows)
    c = {'०':0,'१':1,'२':2,'३':3,'४':4,'५':5,'६':6,'७':7,'८':8,'९':9}
    for i in df.columns:
        df[i]=df[i].apply(lambda x: convert(x))
        
    df=df[[1,2,4,5]][1:]
    columns_name = ['District','Total_Case','Total_Death','Total_Recover']
    df.columns = columns_name
    df=df.sort_values(by="District", ascending=True)
    provision=pd.read_csv('provision.csv')
    df['State']=provision['State']
    df[['Total_Case','Total_Death','Total_Recover']]=df[['Total_Case','Total_Death','Total_Recover']].apply(pd.to_numeric)
    df=df.sort_values(by="Total_Case", ascending=False)
    df.reset_index(drop=True, inplace=True)
    df=df.T
    data=df.to_dict().values()
    filterdata=[]
    for i in data:
        filterdata.append(i)
    return filterdata


def caseforcast():
    response = requests.get('https://pomber.github.io/covid19/timeseries.json')
    data = response.json()
    aa=pd.DataFrame(data)
    aa=(aa['Nepal'])
    data=[]
    for i in aa:
        data.append(i)
    df=pd.DataFrame(data)
    df[['confirmed','deaths','recovered']]=df[['confirmed','deaths','recovered']].apply(pd.to_numeric)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date',drop=True,inplace=True)
    y=df['confirmed'][80:]
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 5) for x in list(itertools.product(p, d, q))]
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
            except:
                continue
    mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 5),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

    results = mod.fit()
    pred = results.get_prediction(start=pd.to_datetime('2020-08-3') ,dynamic=False)
    y_forecasted = pred.predicted_mean
    data=int(round(y_forecasted))
    return data
