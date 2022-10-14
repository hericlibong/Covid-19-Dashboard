import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# Unpivot data frames
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date1, var_name='date', value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date2, var_name='date', value_name='death')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date3, var_name='date', value_name='recovered')

# Merging data frames
covid_data = total_confirmed.merge(right = total_deaths, how = 'left', on = ['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(right = total_recovered, how = 'left', on = ['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])

# Converting date column from string to proper date format
covid_data['date'] = pd.to_datetime(covid_data['date'])

#drop columns province/state and recovered
covid_data = covid_data.drop(columns=['Province/State', 'recovered'])

covid_data_1 = covid_data.groupby(['date'])[['confirmed', 'death',]].sum().reset_index()

# select african countries
covid_data_africa = covid_data.loc[covid_data['Country/Region'].isin(['Algeria', 'Angola', 'Benin', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo (Brazzaville)', 'Congo (Kinshasa)', "Cote d\\'Ivoire", 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Liberia', 'Libya', 'Lesotho', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Zambia', 'Zimbabwe'])]
covid_data_africa
covid_data_afr_1 = covid_data_africa.groupby(['date'])[['confirmed', 'death']].sum().reset_index()


# Create dictionary of list
covid_data_list = covid_data[['Country/Region', 'Lat', 'Long']]
dict_of_locations = covid_data_list.set_index('Country/Region')[['Lat', 'Long']].T.to_dict('dict')

#african dict of locations
covid_data_africa_list = covid_data_africa[['Country/Region', 'Lat', 'Long']]
dict_of_locations_afr = covid_data_africa_list.set_index('Country/Region')[['Lat','Long']].T.to_dict('dict') 


#Top ten country confirmed
top_ten_confirmed = covid_data_africa.groupby('Country/Region')['confirmed'].max().sort_values(ascending=False).reset_index().head(10)
# top ten confirmed fig 
fig = go.Figure(data = [go.Bar(x = top_ten_confirmed['Country/Region'], y = top_ten_confirmed['confirmed'],
                               marker = dict(color = 'orange'),
                               
                               )])
fig.update_layout(title = {'text': 'African Top ten Country confirmed Cases', 
                           'x': 0.5, 
                           'y': 0.93, 
                           'xanchor':'center', 
                           'yanchor': 'top'},
                  titlefont = {'color':'white',
                               'size': 20},
                  font = dict(family='sans-serif',
                              color = 'white',
                              size=12),
                  hovermode = 'closest',
                  paper_bgcolor='#1f2c56',
                  plot_bgcolor='#1f2c56',
                  legend = {'orientation': 'h',
                            'bgcolor':'#1f2c56',
                            'xanchor':'center',
                            'x':0.5, 
                            'y':-0.7},
                  margin=dict(r=0),
                  )


#Top ten country deaths
top_ten_death = covid_data_africa.groupby('Country/Region')['death'].max().sort_values(ascending=False).reset_index().head(10)

fig2 = go.Figure(data = [go.Bar(x = top_ten_death['Country/Region'], y = top_ten_death['death'],
                               marker = dict(color = 'orange'),
                               
                               )])
fig2.update_layout(title = {'text': 'African Top ten Country Deaths', 
                           'x': 0.5, 
                           'y': 0.93, 
                           'xanchor':'center', 
                           'yanchor': 'top'},
                  titlefont = {'color':'white',
                               'size': 20},
                  font = dict(family='sans-serif',
                              color = 'white',
                              size=12),
                  hovermode = 'closest',
                  paper_bgcolor='#1f2c56',
                  plot_bgcolor='#1f2c56',
                  legend = {'orientation': 'h',
                            'bgcolor':'#1f2c56',
                            'xanchor':'center',
                            'x':0.5, 
                            'y':-0.7},
                  margin=dict(r=0),
                  )


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),
                     id = 'corona-image',
                     style={'height': '60px',
                            'width': 'auto',
                            'margin-bottom': '25px'})


        ], className='one-third column'),

        html.Div([
            html.Div([
                html.H3('Covid - 19', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('Track Covid - 19 Cases', style={'margin-bottom': '0px', 'color': 'white'})
            ])

        ], className='one-half column', id = 'title'),

        html.Div([
            html.H6('Last Updated: ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (UTC)',
                    style={'color': 'orange'})

        ], className='one-third column', id = 'title1')

    ], id = 'header', className= 'row flex-display', style={'margin-bottom': '25px'}),

    html.Div([
        html.Div([
            html.H6(children='Global Cases',
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

html.Div([
            html.H6(children='Global Deaths',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_1['death'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': '#dd1e35',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]) /
                                   covid_data_1['death'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': '#dd1e35',
                          'fontSize': 15,
                          'margin-top': '-18px'})

        ], className='card_container three columns'),

html.Div([
            html.H6(children='Global Africa',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_afr_1['confirmed'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'green',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_afr_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_afr_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]) /
                                   covid_data_afr_1['confirmed'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': 'green',
                          'fontSize': 15,
                          'margin-top': '-18px'})

        ], className='card_container three columns'),

html.Div([
            html.H6(children='Global Africa Deaths',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_afr_1['death'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': '#e55467',
                           'fontSize': 40}),
            html.P('new: ' + f"{covid_data_afr_1['death'].iloc[-1] - covid_data_afr_1['death'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_afr_1['death'].iloc[-1] - covid_data_afr_1['death'].iloc[-2]) /
                                   covid_data_afr_1['death'].iloc[-1]) * 100, 2)) + '%)',
                   style={'textAlign': 'center',
                          'color': '#e55467',
                          'fontSize': 15,
                          'margin-top': '-18px'})

        ], className='card_container three columns'),

    ], className='row flex display'),
    
    html.Div([
        html.Div([
            
            dcc.Graph(figure = fig, className = 'dcc_compon',
                      style = {'margin-top': '20px'})
            
        ], className= 'create_container six columns'),
        html.Div([
             
            dcc.Graph(figure = fig2, className = 'dcc_compon',
                      style = {'margin-top': '20px'})
            
        ], className = 'create_container six columns')
    
    ], className = 'row flex-display'),

    html.Div([
        html.Div([
            html.P('Select an African Country:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id = 'w_countries',
                         multi = False,
                         searchable= True,
                         value='Algeria',
                         placeholder= 'Select Countries',
                         options= [{'label': c, 'value': c}
                                   for c in (covid_data_africa['Country/Region'].unique())], className='dcc_compon'),
            html.P('New Cases: ' + ' ' + str(covid_data_africa['date'].iloc[-1].strftime('%B %d, %Y')),
                   className='fix_label', style={'text-align': 'center', 'color': 'white'}),
            dcc.Graph(id = 'confirmed', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
dcc.Graph(id = 'death', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'})

        ], className='create_container three columns'),

        html.Div([
dcc.Graph(id = 'pie_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container four columns'),

html.Div([
dcc.Graph(id = 'line_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container five columns'),

    ], className='row flex-display'),

    html.Div([
html.Div([
dcc.Graph(id = 'map_chart', config={'displayModeBar': 'hover'}
                      )
        ], className='create_container1 twelve columns')

    ], className='row flex-display')

], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

@app.callback(Output('confirmed', 'figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data_africa.groupby(['date', 'Country/Region'])[['confirmed', 'death']].sum().reset_index()
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

@app.callback(Output('death', 'figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    covid_data_2 = covid_data_africa.groupby(['date', 'Country/Region'])[['confirmed', 'death']].sum().reset_index()
    value_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2]
    delta_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-3]

    return {
        'data': [go.Indicator(
               mode='number+delta',
               value=value_death,
               delta = {'reference': delta_death,
                        'position': 'right',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Death',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='#dd1e35'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }



@app.callback(Output('pie_chart', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    covid_data_2 = covid_data_africa.groupby(['date', 'Country/Region'])[['confirmed', 'death']].sum().reset_index()
    confirmed_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1]
    death_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1]
    colors = ['orange', '#dd1e35', 'green', '#e55467']

    return {
        'data': [go.Pie(
            labels=['Confirmed', 'Death'],
            values=[confirmed_value, death_value],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=45,
            # insidetextorientation= 'radial'

        )],

        'layout': go.Layout(
            title={'text': 'Total Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}


        )
    }

@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    covid_data_2 = covid_data_africa.groupby(['date', 'Country/Region'])[['confirmed', 'death']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == w_countries][['Country/Region', 'date', 'confirmed']].reset_index()
    covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()


    return {
        'data': [go.Bar(
            x=covid_data_3['date'].tail(30),
            y=covid_data_3['daily confirmed'].tail(30),
            name='Daily Confirmed Cases',
            marker=dict(color='orange'),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>' +
            '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'


        ),
            go.Scatter(
                x=covid_data_3['date'].tail(30),
                y=covid_data_3['Rolling Ave.'].tail(30),
                mode='lines',
                name='Rolling Average of the last 7 days - daily confirmed cases',
                line=dict(width=3, color='#FF00FF'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
                '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['Rolling Ave.'].tail(30)] + '<br>'


            )],

        'layout': go.Layout(
            title={'text': 'Last 30 Days Daily Confirmed Cases: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )
                       )


        )
    }

@app.callback(Output('map_chart', 'figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    covid_data_4 = covid_data_africa.groupby(['Lat', 'Long', 'Country/Region'])[['confirmed', 'death']].max().reset_index()
    covid_data_5 = covid_data_4[covid_data_4['Country/Region'] == w_countries]

    if w_countries:
        zoom=2
        zoom_lat = dict_of_locations_afr[w_countries]['Lat']
        zoom_long = dict_of_locations_afr[w_countries]['Long']



    return {
        'data': [go.Scattermapbox(
            lon=covid_data_5['Long'],
            lat=covid_data_5['Lat'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=covid_data_5['confirmed'] / 1500,
                                           color=covid_data_5['confirmed'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + covid_data_5['Country/Region'].astype(str) + '<br>' +
            '<b>Longitude</b>: ' + covid_data_5['Long'].astype(str) + '<br>' +
            '<b>Latitude</b>: ' + covid_data_5['Lat'].astype(str) + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['confirmed']] + '<br>' +
            '<b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_5['death']] + '<br>' 
            


        )],

        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            margin=dict(r=0, l =0, b = 0, t = 0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiaGVyaWMiLCJhIjoiY2lwcHh2cHpwMDA1aWhybnBqbHQzOXQydCJ9.4CM5ZOcHIkaSnKnXywwJlA',
                center = go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                zoom=zoom,
            ),
            autosize=True



        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)

