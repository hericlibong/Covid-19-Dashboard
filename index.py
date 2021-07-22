import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

#load data
confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)


#unpivot dataframes
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='date', value_name='confirmed')
total_deaths = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='date', value_name='deaths')
total_recovered = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='date', value_name='recovered')

#merge dataframes
covid_data = total_confirmed.merge(right=total_deaths, how='left', on=['Province/State', 'Country/Region','date', 'Lat', 'Long'])
covid_data = covid_data.merge(right=total_recovered, how='left', on=['Province/State', 'Country/Region','date', 'Lat', 'Long'])

#set date format
covid_data['date'] = pd.to_datetime(covid_data['date'])

#replace null values on recovered collumn with 0
covid_data['recovered']=covid_data['recovered'].fillna(0)

#add active case column
covid_data['active']= covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']

#calculate GLobals Cases
covid_data_1 = covid_data.groupby(['date'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
#global_cases = covid_data_1['confirmed'].iloc[-1]
#global_cases_string = "{: ,.0f}".format(global_cases)

#percentage rate rase per/day connfirmed cases
#rase_percentage_day = str(round(((covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2])/covid_data_1['confirmed'].iloc[-1])*100, 1))

#percentage rate raise per/day deaths cases
#rase_percentage_day_deaths = str(round(((covid_data_1['deaths'].iloc[-1] - covid_data_1['deaths'].iloc[-2])/covid_data_1['deaths'].iloc[-1])*100, 1))

#perceentage rate raise for recoveing cases
#rase_percentage_day_recovered = str(round(((covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2])/covid_data_1['recovered'].iloc[-1])*100, 1))

#perc rate raise for active cases
#rase_percentage_day_active = str(round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2])/covid_data_1['active'].iloc[-1])*100, 1))




#create dash layout

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),
                     id='corona-image',
                     style={'height':'60px',
                            'width':'auto',
                            'margin-bottom':'25px'})
            
        ], className='one-third column'),
        
        html.Div([
            html.Div([
                html.H3('Covid - 19', style={'color':'white'}),
                html.H5('Track Covid - 19 cases', style ={'margin-bottom':'opx', 'color':'white'})
            ])
            
        ], className='one-half column', id='title'),
        
        html.Div([
           html.H6('Last Updated :'  + ' ' + str(covid_data['date'].iloc[-1].strftime('%B %d , %Y')) +  ' 00:01(UTC)', #add string last date 
                   style={'color':'orange'}) 
            
        ], className='one-third column', id='title1')
        
    ], id='header', className='row flex-display', style={'margin-bottom':'25px'}),
   
   html.Div([
       html.Div([
           #confirmed card cases
            html.H6(children='Confirmed Cases',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_1['confirmed'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]) /
                                   covid_data_1['confirmed'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 15,
                          'margin-top': '-18px'})

        ], className='card_container three columns'),
       
       #deaths cases card
       html.Div([
           html.H6(children='Deaths Cases',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_1['deaths'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'red',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_1['deaths'].iloc[-1] - covid_data_1['deaths'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['deaths'].iloc[-1] - covid_data_1['deaths'].iloc[-2]) /
                                   covid_data_1['deaths'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': 'red',
                          'fontSize': 15,
                          'margin-top': '-18px'})

        ], className='card_container three columns'),
     
    #recovered card cases
       html.Div([
            html.H6(children= 'Recovered Cases',
                   style= {'textAlign':'center',
                           'color':'white'}),
           html.P(f"{covid_data_1['recovered'].iloc[-1]:,.0f}", 
                  style = {'textAlign':'center',
                           'color':'green',
                           'fontSize':40}),
          
           html.P('new: ' + f"{covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]) /
                                   covid_data_1['recovered'].iloc[-1]) * 100, 2)) + '%)', 
                  style = {'textAlign':'center',
                           'color':'green',
                           'fontSize': 15,
                           'margin-top':'-18px'}),
           
       ], className= 'card_container three columns'),
       
       #active card cases
       html.Div([
           html.H6(children='Global Active',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_1['active'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': '#e55467',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]) /
                                   covid_data_1['active'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': '#e55467',
                          'fontSize': 15,
                          'margin-top': '-18px'})

        ], className='card_container three columns'),
        
    ], className='row flex-display'),
   
   html.Div([
       html.Div([
           html.P('Select country : ', className='fix_label', style={'color':'white', 'fontSize':20}),
           dcc.Dropdown(id='w_countries',
                        multi=False,
                        searchable=True,
                        value= 'US',
                        placeholder='select countries',
                        options=[{'label': c, 'value':c} for c in covid_data['Country/Region'].unique()], 
                        className= 'dcc_compon'),
           html.P('New Cases: ' + '' + str(covid_data['date'].iloc[-1].strftime('%B %d , %Y')),
                  className= 'fix_label', style={'color':'white', 'textAlign':'center'}),
           dcc.Graph(id = 'confirmed', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'}),
           dcc.Graph(id = 'deaths', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'}),
           dcc.Graph(id = 'recovered', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'}),
           dcc.Graph(id = 'active', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'}),
           
           ], className='create_container three columns'),
       
       html.Div([
           dcc.Graph(id = 'pie_chart', config={'displayModeBar': 'hover'}),
           
           
       ], className = 'create_container four columns'),
       
       html.Div([
           dcc.Graph(id = 'line_chart', config={'displayModeBar': 'hover'}),
           
           
       ], className = 'create_container five columns'),
       
   ], className='row flex-display') 
   
], id = 'mainContainer', style={'display':'flex', 'flex-direction':'column'})

@app.callback(Output('confirmed', 'figure'),
              [Input('w_countries','value')])

def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-3]
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_confirmed,
               delta = {'reference': delta_confirmed,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Confirmed',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }
    
@app.callback(Output('deaths', 'figure'),
              [Input('w_countries','value')])

def update_deaths(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_deaths = covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-2]
    delta_deaths = covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-3]
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_deaths,
               delta = {'reference': delta_deaths,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Deaths',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='red'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }
    
@app.callback(Output('recovered', 'figure'),
              [Input('w_countries','value')])

def update_recovered(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2]
    delta_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-3]
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_recovered,
               delta = {'reference': delta_recovered,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New recovered',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='green'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }
    
@app.callback(Output('active', 'figure'),
              [Input('w_countries','value')])

def update_active(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-3]
    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_active,
               delta = {'reference': delta_active,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'Active Cases',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='#e55467'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    } 
    
@app.callback(Output('pie_chart', 'figure'),
              [Input('w_countries','value')])

def update_active(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    confirmed_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1] 
    deaths_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-1]
    recovered_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1] 
    active_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1]
    colors = ['orange', 'red', 'green', 'blue' ] 
    
    return {
        'data': [go.Pie(
            labels=['confirmed', 'deaths', 'recovered', 'active'],
            values = [confirmed_value, deaths_value, recovered_value, active_value],
            marker = dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo = 'label+value',
            hole = .7
            
            
            
               
        )],

        'layout': go.Layout(
            title={'text': 'Total Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont = {'color':'white',
                         'size':20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode = 'closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend = {'orientation': 'h',
                      'bgcolor':'#1f2c56',
                      'xanchor': 'center', 'x':0.5, 'y':-0.7}
            

        )
    }
    
@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries','value')])

def update_active(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region']==w_countries][['Country/Region', 'date', 'confirmed']].reset_index()
    covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    return {
        'data': [go.Bar(
            x = covid_data_3['date'].tail(30),
            y = covid_data_3['daily confirmed'].tail(30),
            name = 'daily confirmed cases',
            marker = dict(color='blue'),
            hoverinfo='text',
            hovertext = 
            '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>' +
            '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'
            
            
            
            
               
        )
                
            ],

        'layout': go.Layout(
            title={'text': 'Total Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont = {'color':'white',
                         'size':20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode = 'closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend = {'orientation': 'h',
                      'bgcolor':'#1f2c56',
                      'xanchor': 'center', 'x':0.5, 'y':-0.7},
            margin=dict(r=0),
            xaxis=dict(title = '<b>Date</>',
                       color = 'white',
                       showline=True,
                       showgrid=True),
            yaxis=dict(title = '<b>Daily Confirmed Cases</>',
                       color = 'white',
                       showline=True,
                       showgrid=True),
            

        )
    }      

    

if __name__== '__main__':
    app.run_server(debug=True)






