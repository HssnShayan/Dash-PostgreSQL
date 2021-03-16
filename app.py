import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine=create_engine('postgresql://postgresql:test123456@postgresql:5432/test_db', echo=False)
Session=sessionmaker(bind=engine)
session=Session()

Base=declarative_base()

class Person(Base):
    __tablename__ = 'person'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    family = Column(String(20))
    age = Column(Integer)
    salary = Column(Integer)

Base.metadata.create_all(engine)


app = dash.Dash(__name__)
myInputs=('First Name', 'Last Name', 'Age', 'Salary')

app.layout = html.Div([
    html.Div([
        html.H3('This is a Simple Dash App to be Connected with PostgreSQL Database',
        style={'color': 'red', 'fontSize': '25px', 'fontFamily': 'arial', })

    ], style={'backgroundColor': '#e8e6e6', 'margin':'0px 50px', 'textAlign': 'center', 'border': '2px blue solid'}),
    html.Div([
        dcc.Input(
            id='i-name',
            type='text',
            placeholder='First Name',
            style={'textAlign': 'center', 'height': '40px', 'marginTop': '50px', 'fontSize': '16px'}
        ),
        dcc.Input(
            id='i-family',
            type='text',
            placeholder='Last Name',
            style={'textAlign': 'center', 'height': '40px', 'marginTop': '50px', 'fontSize': '16px'}
        ),
        dcc.Input(
            id='i-age',
            type='number',
            placeholder='Age',
            style={'textAlign': 'center', 'height': '40px', 'marginTop': '50px', 'fontSize': '16px'}
        ),
        dcc.Input(
            id='i-salary',
            type='number',
            placeholder='Salary',
            style={'textAlign': 'center', 'height': '40px', 'marginTop': '50px', 'fontSize': '16px'}
        )
        
    ], style={'textAlign': 'center',}),

    html.Div([
         html.Button("Submit Data", id='btn-submit', n_clicks=0, 
         style={'backgroundColor':'#0abcf2', 'height':'35px','margin':'0px 5px', 'border':'.5px solid grey', 'borderRadius':'5px'}),
         html.Button("Fetch data from DataBase", id='btn-fetch', n_clicks=0, 
         style={'backgroundColor':'#0aeef2', 'height':'35px', 'margin':'0px 5px', 'border':'.5px solid grey', 'borderRadius':'5px'}),
         html.Button("Plot Graph", id='btn-graph', n_clicks=0, 
         style={'backgroundColor':'#f28d0a', 'height':'35px', 'margin':'0px 5px', 'border':'.5px solid grey', 'borderRadius':'5px'}),
    ], style={'margin':'20px 10px', 'textAlign': 'center',}),

    html.Div([html.H5('Insert New Data Or Fetch From PostgreSQL Data-Base', id='msg', 
    style={'margin':'auto', 'paddingTop':'5px'})], 
    style={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold',
    'textAlign': 'center', 'marginTop': '30px',
    'height':'25px', 'fontFamily': 'arial', 'fontSize': '16px', 'width': '30%', 'margin': 'auto',
    'borderRadius': '10px'}),

    
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in myInputs],
            # data=df.to_dict('records'),
            page_action='none',
            fixed_rows={'headers': True},
            style_table={'height': '300px', 'overflowY': 'auto', 'width': '70%', 'margin': 'auto', 'display':'inline-flex'},
            style_cell={'minWidth': '90px', 'width': '90px', 'maxWidth': '90px', 'textAlign': 'center'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'
    }
            ),], style={'textAlign': 'center', 'marginTop': '10px',}),

    html.Div([
        dcc.Graph(
            id='graph',
            style={'display': 'none'}
            )], style={'textAlign': 'center', 'marginTop': '50px'})

    

], style={'textAlign': 'center'})
# ------------------------------------------------------------------------------------------------

@app.callback(
    [Output("msg", "children"),
    Output("i-name", "value"),
    Output("i-family", "value"),
    Output("i-age", "value"),
    Output("i-salary", "value")],
    [Input("btn-submit", "n_clicks"),
    State("i-name", "value"),
    State("i-family", "value"),
    State("i-age", "value"),
    State("i-salary", "value")])
def submit_data(clk1, val1, val2, val3, val4):
    ctx = dash.callback_context
    flag = ctx.triggered[0]['prop_id'].split('.')[0]
    if clk1 is None:
        raise PreventUpdate
    else:
        if flag == 'btn-submit':
            if (val1 == '') or (val2 == '') or (val3 is None) or (val4 is None):
                return ['Please Fill All Fields then Try Again !','','', '','']                
                
            else:
                try:
                    person1=Person(name=val1, family=val2, age=val3, salary=val4)
                    session.add(person1)
                    session.commit()
                    return ['Your Data is Inserted to Data-Base Successfuly ...','','', '','']
                except:
                    session.rollback()
                    return ['Please Fill All Fields then Try Again !','','', '','']
                
        else:
            raise PreventUpdate

@app.callback(
    Output("table", "data"),
    [Input("btn-fetch", "n_clicks")])
def fetch_data(clk1):
    ctx = dash.callback_context
    flag = ctx.triggered[0]['prop_id'].split('.')[0]
    if clk1 is None:
        raise PreventUpdate
    else:
        if flag == 'btn-fetch':
            persons=session.query(Person)
            df=[]
            for person in persons:
                dff={'First Name': person.name, 'Last Name': person.family, 'Age': person.age, 'Salary': person.salary}
                df.append(dff)
            
            return df
        else:
            raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)