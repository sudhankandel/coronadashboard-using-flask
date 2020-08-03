import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from getData import *

def nepal_less():
    results=Nepal_table()
    district = []
    case = []
    for i in results[-10:]:
        district.append(i['District'])
        case.append(i['Total_Case']) 

    

    fig = go.Figure()
    fig.add_trace(go.Bar(x=district,
                    y=case,
                    name='case',
                    marker_color='rgb(55, 83, 109)'
                    ))

    fig.update_layout(

         yaxis=dict(
            title='Total Cases',
            titlefont_size=8,
            tickfont_size=8,
        ),
        title='District have Less Impact According to Cases ',
        xaxis_tickfont_size=8,
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=25,
        pad=0
    ),
        
        
        bargap=0.15, 
        bargroupgap=0.1 
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def nepal_top():
    results=Nepal_table()
    district = []
    case = []
    death = []
    recover = []
    for i in results[:5]:
        district.append(i['District'])
        case.append(i['Total_Case'])
        death.append(i['Total_Death'])
        recover.append(i['Total_Recover'])  

    

    fig = go.Figure()
    fig.add_trace(go.Bar(x=district,
                    y=case,
                    name='case',
                    marker_color='rgb(55, 83, 109)'
                    ))
    fig.add_trace(go.Bar(x=district,
                    y=death,
                    name='death',
                    marker_color='rgb(26, 118, 255)'
                    ))
    fig.add_trace(go.Bar(x=district,
                    y=recover,
                    name='Recover',
                    marker_color='rgb(26, 12, 255)'
                    ))

    fig.update_layout(
       yaxis=dict(
            title='Total Cases',
            titlefont_size=8,
            tickfont_size=8,
        ),
        title='District have High Impact According to Cases ',
        xaxis_tickfont_size=10,
         margin=dict(
        l=0,
        r=0,
        b=0,
        t=25,
        pad=0
    ),

        
        barmode='group',
        
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_bar(): 
    results=global_table() 
    country = []
    case = []
    death = []
    recover = []
    for i in results[:10]:
        country.append(i['country'])
        case.append(i['cases'])
        death.append(i['deaths'])
        recover.append(i['recovered'])  

    years = country

    fig = go.Figure()
    fig.add_trace(go.Bar(x=years,
                    y=case,
                    name='case',
                    marker_color='rgb(55, 83, 109)'
                    ))
    fig.add_trace(go.Bar(x=years,
                    y=death,
                    name='death',
                    marker_color='rgb(26, 118, 255)'
                    ))
    fig.add_trace(go.Bar(x=years,
                    y=recover,
                    name='Recover',
                    marker_color='rgb(26, 12, 255)'
                    ))

    fig.update_layout(
        title='Top 10 Country impacted by Covid-19 ',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Total Number of Cases',
            titlefont_size=16,
            tickfont_size=14,
        ),
            margin=dict(
        l=0,
        r=0,
        b=0,
        t=25,
        pad=0
    ),
        
        barmode='group',
        bargap=0.15, 
        bargroupgap=0.1 
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def multiLine(name):
    data=TimeSeries(name)
    Date = data['date']
    Confirm = data['confirm']
    Death = data['death']
    recover = data['recover']


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = Date,
        y = Confirm,
        name='Confirm'))
    fig.add_trace(go.Scatter(
        x = Date,
        y = Death,
        name='Death'
    ))
    fig.add_trace(
         go.Scatter(
        x = Date,
        y = recover,
        name='Recover'
    )
    )

    fig.update_layout(
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Total Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
            margin=dict(
        l=0,
        r=0,
        b=15,
        t=0,
        pad=0
    )),

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def piechart(condition):
    table_data=global_table()
    df=pd.DataFrame(table_data)
    a=df.groupby('continent')[condition].sum()
    continent=[]
    data=[]
    for j in a:
        data.append(j)
    for i in a.keys():
        continent.append(i)
    fig = go.Figure(data=[go.Pie(labels=continent, values=data)])
    fig.update_layout(
    
    height=250,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
    # paper_bgcolor="LightSteelBlue",
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def Statepiechart():
    table_data=Nepal_table()
    df=pd.DataFrame(table_data)
    
    a=df.groupby('State')['Total_Case'].sum()
    State=[]
    data=[]
    for j in a:
        data.append(j)
    for i in a.keys():
        State.append(i)
    fig = go.Figure(data=[go.Pie(labels=State, values=data)])
    fig.update_layout(
    title='State Wise Covid Impact',
    height=250,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=25,
        pad=0
    ),
  
    # paper_bgcolor="LightSteelBlue",
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
   

