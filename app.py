from flask import Flask, render_template,request
from getData import Extract_data,nepal_data,global_update,global_news_update,country_data,TimeSeries
results=Extract_data()
nepal=nepal_data()
global_data=global_update()
new=global_news_update()
bar_data=results[0:11]

app = Flask(__name__)
@app.route('/timeSeries', methods=['GET', 'POST'])
def Time():
    combodata = request.get_data()
    combodata = combodata.decode("utf-8")
    Time_data=TimeSeries(str(combodata))
    return Time_data

@app.route('/global', methods=['GET', 'POST'])
def Global():
    results = Extract_data()
    country = []
    case = []
    death = []
    recover = []
    for i in results[:10]:
        country.append(i['country'])
        case.append(i['cases'])
        death.append(i['deaths'])
        recover.append(i['recovered'])
    datas = {'country': country,
             'case': case,
             'death':death,
             'recover':recover}
    return datas
@app.route('/country', methods=['GET', 'POST'])
def Get_data():
    data = request.get_data()
    data = data.decode("utf-8")
    data = data.strip()
    countrydata = country_data(data)
    return  countrydata

@app.route('/', methods=['POST', 'GET'])
def index():
    return  render_template('index.html',table_data=results,nepaldata=nepal,globaldata=global_data,global_news=new,
                            bar_datas=bar_data)


if __name__ == "__main__":
    app.run(debug=True)