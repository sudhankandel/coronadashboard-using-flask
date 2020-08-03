from flask import Flask, render_template,request
from getData import global_news_update,nepal_data,global_table,Nepal_table,caseforcast
from visualized  import create_bar,multiLine,piechart,global_update,nepal_top,nepal_less,Statepiechart


results=global_table()
new=global_news_update()
nepal=nepal_data()
nep_table=Nepal_table()
global_data=global_update()

nep_top=nepal_top()
bar = create_bar()
npl_less=nepal_less()
state= Statepiechart()
casefor=caseforcast()


app = Flask(__name__)


@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON= multiLine(feature)
    return graphJSON
@app.route('/continent', methods=['GET', 'POST'])
def change_Piechart():
    feature = request.args['selected']
    graphJSON= piechart(feature)
    return graphJSON


@app.route('/', methods=['POST', 'GET'])
def index():
   feature='Nepal'
   line=multiLine(feature)
   cond='cases'
   pie=piechart(cond)
   return  render_template('index.html',global_news=new,
                            nepal_data=nepal,
                            table_data=results,
                            plot=bar,
                            line_data=line,
                            table_data1=nep_table,
                            globals_data=global_data,
                            piechart_data=pie,
                            nepal_top_bar=nep_top,
                            nepal_less_bar=npl_less,
                            state_piechart=state,
                            forcas=casefor,
                            )
if __name__ == "__main__":
    app.run(debug=True)