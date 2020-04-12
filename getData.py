import requests
import json,schedule,time
import pandas as pd

response_country = requests.get("https://corona.lmao.ninja/countries")
data_dic = response_country.json()
def country_data(country):
    dataframe = pd.DataFrame(data_dic)
    dataframe = dataframe[['country', 'cases', 'deaths', 'recovered', 'todayCases', 'active', 'todayDeaths']]
    if country == '':
        dataframe = dataframe[dataframe['country'] == 'Italy']
    else:
        dataframe = dataframe[dataframe['country'] == country]
    dataframe = dataframe.to_dict('records')[0]
    return dataframe
def Extract_data():
    data_dics = sorted(data_dic, key=lambda x: x['cases'], reverse=True)
    dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    wanted_keys = ("country", "cases", "deaths","recovered")
    data = []
    for i in data_dics:
        filter_data = dictfilt(i, wanted_keys)
        data.append(filter_data)
    return data

def nepal_data():
    url = 'https://nepalcorona.info/api/v1/data/nepal'
    response = requests.get(url)
    data = response.json()
    return data
def global_update():
    data=Extract_data()
    df=pd.DataFrame(data)
    total_cases = sum(df['cases'])
    total_recovered = sum(df['recovered'])
    total_deaths = sum(df['deaths'])
    data=[total_cases,total_deaths,total_recovered]
    return data
def global_news_update():
    url = 'https://first-api1234.herokuapp.com/covid/api/news'
    response = requests.get(url)
    data = response.json()
    df_news = pd.DataFrame(data['news'])
    news_source = []
    for i in range(len(df_news)):
        news_source.append((df_news["title"][i]))
    return news_source[:50]


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
