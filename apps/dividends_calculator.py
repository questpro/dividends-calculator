# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import commonmodules

from app import app

meta_tags = [
    {'name':'description',
     'content':'Дивидендный калькулятор с учетом сложного процента'},
    {'name':'title',
     'content':'Дивидендный калькулятор'}
]

#app.external_stylesheets = external_stylesheets
app.meta_tags = meta_tags
app.title = 'Дивидендный калькулятор'

bottom_text = '''
1) Все суммы в долларах, проценты - в %  
2) По умолчанию, средний размер дивидентов при покупке акций устанавливаем в 4%, можно поменять  
3) По умолчанию, средний рост цены акций в год устанавливаем в 12.5% на основе статистики по S&P Dividends aristocrats   
4) Все дивиденды реинвестируем для осуществления скорейшего роста - сложный процент  
'''

default__divident_income_per_month = 1000
default__start_capital = 1000
default__regular_payment = 1000
default__start_divident_percent = 4
default__average_cost_grow_percent = 12.5

layout = html.Div([
    commonmodules.get_menu(),
    html.H1('Дивидендный калькулятор с учетом сложного процента'),
    html.Div([
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(children='Желаемый средний доход в месяц по дивидентам ($)', className="col-sm-4 col-form-label"),
            html.Div([
                dcc.Input(id='divident-income-per-month', value='1000', type='text', className="form-control-plaintext")
            ], className="col-sm-4")
        ], className="form-group row"),
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(children='Первоначальный взнос ($)', className="col-sm-4 col-form-label"),
            html.Div([
                dcc.Input(id='start-capital', value='1000', type='text', className="form-control-plaintext")
            ], className="col-sm-4")
        ], className="form-group row"),
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(children='Частота очередного поступления: 1 месяц', className="col-sm-4 col-form-label")
        ], className="form-group row"),
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(children='Размер очередного поступления ($)', className="col-sm-4 col-form-label"),
            html.Div([
                dcc.Input(id='regular-payment', value='1000', type='text', className="form-control-plaintext")
            ], className="col-sm-4")
        ], className="form-group row"),
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(children='Средний размер дивидентов в при покупке акций (%)', className="col-sm-4 col-form-label"),
            html.Div([
                dcc.Input(id='start-divident-percent', value='4', type='text', className="form-control-plaintext")
            ], className="col-sm-4")
        ], className="form-group row"),
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(children='Средний рост цены акций в год (%)', className="col-sm-4 col-form-label"),
            html.Div([
                dcc.Input(id='average-cost-grow-percent', value='12.5', type='text', className="form-control-plaintext")
            ], className="col-sm-4")
        ], className="form-group row"),
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(children='Отображаем на графиках максимум лет', className="col-sm-4 col-form-label"),
        ], className="form-group row"),
        dcc.Slider(
            id='maximum-years',
            min=10,
            max=50,
            marks={i: 'рассматриваем максимум лет {}'.format(i) if i == 1 else str(i) for i in range(5, 51)},
            value=11
        ),
        html.Div([
            html.Div([], className="col-sm-1"),
            html.Label(id='result', className="col-sm-8 col-form-label"),
        ], className="form-group row")
    ], className=""),
    html.Div([
        dcc.Graph(id='dividends-graph'),
        dcc.Graph(id='capital-graph')
    ]),
    html.Div([
        dcc.Markdown(children=bottom_text)
    ])
])

def create_dividends_graph(df, target, title):
    return {
        'data': [dict(
            x=df['month'],
            y=df['dividend_no_reinv'],
            mode='lines',
            name='Дивиденды - без реинвестиций и без роста цены акций'
        ), dict(
            x=df['month'],
            y=df['dividend_percent_reinv'],
            mode='lines',
            name='Дивиденды - рост за счет роста акций'
        ), dict(
            x=df['month'],
            y=df['dividend_all_reinv'],
            mode='lines',
            name='Дивиденды - рост цен акций и реинвестирование дивидендов'
        ), dict(
            x=[target['month'],],
            y=[target['dividend'],],
            mode='marks',
            name='Целевое значение дивидендов'
        )],
        'layout': {
            'annotations': [{
                'x': 0, 'y': 0, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear', 'title': 'Дивиденды в месяц, $'},
            'xaxis': {'showgrid': True, 'title': 'Месяцы'}
        }
    }

def create_capital_graph(df, target, title):
    return {
        'data': [dict(
            x=df['month'],
            y=df['cap_no_reinv'],
            mode='lines',
            name='Капитал - вложенные деньги'
        ), dict(
            x=df['month'],
            y=df['cap_percent_reinv'],
            mode='lines',
            name='Капитал - с ростом цены акций'
        ), dict(
            x=df['month'],
            y=df['cap_all_reinv'],
            mode='lines',
            name='Капитал - с ростом цены акций и реинвестицией дивидендов'
        )],
        'layout': {
            'annotations': [{
                'x': 0, 'y': 0, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear', 'title': 'Капитал, $'},
            'xaxis': {'showgrid': True, 'title': 'Месяцы'}
        }
    }

def total_result_div(result):
    if result['dividend'] <= 0:
        return "Желаемая дивидендная доходность не найдена в заданном промежутке времени, попробуйте выставить больше лет для графиков"
    return "Требуемый ежемесячный дивидендный результат будет достигнут через [ {} месяцев], при этом будет вложено: [ {}$ ], но ваш капитал достигнет к этому времени за счет сложного процента: [ {:.2f}$ ]".format(result['month'], result['current_capital_no_reinv'], result['current_capital_with_all_reinv'])

""" Var in input field might be not floar, but empty or string, in such case use default value """ 
def input_to_float(var, default):
    if var.isdigit():
        return float(var)
    else:
        return default   
           
@app.callback(
    [Output(component_id='dividends-graph',component_property='figure'),
     Output(component_id='capital-graph',component_property='figure'),
     Output(component_id='result', component_property='children')],
    [Input(component_id='maximum-years', component_property='value'),
     Input(component_id='divident-income-per-month', component_property='value'),
     Input(component_id='start-capital', component_property='value'),
     Input(component_id='regular-payment', component_property='value'),
     Input(component_id='start-divident-percent', component_property='value'),
     Input(component_id='average-cost-grow-percent', component_property='value')]
)
def update_output_div(maximum_years, divident_income_per_month, start_capital, regular_payment, start_divident_percent, average_cost_grow_percent):
    max_years_number = int(maximum_years)
    MONTH_COUNT_YEAR = 12
    
    divident_income_per_month = input_to_float(divident_income_per_month, default__divident_income_per_month)
    start_capital = input_to_float(start_capital, default__start_capital)
    regular_payment = input_to_float(regular_payment, default__regular_payment)
    start_divident_percent = input_to_float(start_divident_percent, default__start_divident_percent)
    average_cost_grow_percent = input_to_float(average_cost_grow_percent, default__average_cost_grow_percent)
    
    current_capital_no_reinv = current_capital_just_percent_reinv = current_capital_with_all_reinv = start_capital
    info = {}
    info['month'] = []
    info['dividend_no_reinv'] = []
    info['dividend_percent_reinv'] = []
    info['dividend_all_reinv'] = []
    info['cap_no_reinv'] = []
    info['cap_percent_reinv'] = []
    info['cap_all_reinv'] = []
    target = {'month': 0, 'dividend': 0, 'current_capital_no_reinv': 0, 'current_capital_with_all_reinv': 0}
    for month in range(max_years_number * MONTH_COUNT_YEAR):
        info['month'].append(month)
        current_capital_no_reinv += regular_payment
        info['cap_no_reinv'].append(current_capital_no_reinv)
        current_dividend_no_reinv = current_capital_no_reinv * start_divident_percent / 100 / MONTH_COUNT_YEAR
        info['dividend_no_reinv'].append(current_dividend_no_reinv)
        current_capital_just_percent_reinv = (current_capital_just_percent_reinv + regular_payment) * (1 + average_cost_grow_percent / 100 / MONTH_COUNT_YEAR)
        info['cap_percent_reinv'].append(current_capital_just_percent_reinv)
        current_dividend_just_percent_reinv = current_capital_just_percent_reinv * start_divident_percent / 100 / MONTH_COUNT_YEAR
        info['dividend_percent_reinv'].append(current_dividend_just_percent_reinv)
        current_dividend_with_all_reinv = current_capital_with_all_reinv * start_divident_percent / 100 / MONTH_COUNT_YEAR
        info['dividend_all_reinv'].append(current_dividend_with_all_reinv)
        current_capital_with_all_reinv = (current_capital_with_all_reinv + regular_payment + current_dividend_with_all_reinv) * (1 + average_cost_grow_percent / 100 / MONTH_COUNT_YEAR)
        info['cap_all_reinv'].append(current_capital_with_all_reinv)
        if((current_dividend_with_all_reinv >= divident_income_per_month) and not (target['month'])):
            target['month'] = month 
            target['dividend'] = current_dividend_with_all_reinv
            target['current_capital_no_reinv'] = current_capital_no_reinv
            target['current_capital_with_all_reinv'] = current_capital_with_all_reinv
    return create_dividends_graph(info, target, ''), create_capital_graph(info, target, ''), total_result_div(target)
