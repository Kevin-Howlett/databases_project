from flask import Flask, render_template,request
import plotly
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import psycopg2

import pandas as pd
import json

app = Flask(__name__)

conn = psycopg2.connect("dbname=nullset user=wtien")
cur = conn.cursor()


cur.execute("""SELECT * FROM dat_sci_country;""")
dat_sci = pd.DataFrame(cur.fetchall())
cur.execute("""select * from dat_sci_country limit 0""")
colnames = [desc[0] for desc in cur.description]
dat_sci.columns = colnames


cur.execute("SELECT * FROM happy;""")
happy = pd.DataFrame(cur.fetchall())
cur.execute("""select * from happy limit 0""")
colnames = [desc[0] for desc in cur.description]
happy.columns = colnames

cur.execute("""SELECT * FROM wdi;""")
wdi = pd.DataFrame(cur.fetchall())
cur.execute("""select * from wdi limit 0""")
colnames = [desc[0] for desc in cur.description]
wdi.columns = colnames

df1 = wdi.join(happy.set_index('country'), on='country')
df = df1.join(dat_sci.set_index('country'), on='country')
df = df.drop(columns=['unempbenefits','afp_totlabforce','afp_total','cgd_total','peacekeepers','suic_mortalityrate_pop','suic_mortalityrate_female','suic_mortalityrate_male'])

@app.route('/')
def index():
    feature = 'Bar'
    bar = create_plot(feature)
    return render_template('index.html', plot=bar)

def create_plot(feature):

    if feature =='Bar':
          scaler = MinMaxScaler()
          df2 = df
          df2.loc[:, df2.columns != 'country'] = scaler.fit_transform(df2.loc[:, df2.columns != 'country'])
          df2['agg'] = df2[list(df2.columns[1:])].sum(axis=1)
          df2.sort_values(by=['agg'],ascending=False,inplace=True)
          df2 = df2.drop(columns=['agg'])


          l = []
          for i in range(len(df2.columns)-1):
              l.append(go.Bar(name = df2.columns[i+1], x = df2['country'][:20], y = df.iloc[:20,i+1].tolist()))


          fig = go.Figure(data=l)
 
          fig.update_layout(barmode='stack')

        
    else:
        fig = go.Figure()


        for column in df.columns[1:].to_list():
            fig.add_trace(
                go.Box(
                    y = df[column],
                    name = column,boxpoints='all',hovertext=df["country"]
                )
            )

        fig.update_layout(    
            updatemenus=[go.layout.Updatemenu(
                active=0,
                buttons=list(
                    [
                     dict(label = 'cureduexpen_pri',
                          method = 'update',
                          args = [{'visible': [True, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Primary Education Expenditure',
                                   'showlegend':True}]),
                     dict(label = 'cureduexpen_sec',
                          method = 'update',
                          args = [{'visible': [False, True,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]},
                                  {'title': 'Secondary Education Expenditure',
                                   'showlegend':True}]),
                     dict(label = 'cureduexpen_ter',
                          method = 'update',
                          args = [{'visible': [False, False,True,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Tertiary Education Expenditure',
                                   'showlegend':True}]),
                     dict(label = 'cureduexpen_total',
                          method = 'update',
                          args = [{'visible': [False, False,False,True,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]},
                                  {'title': 'Total Education Expenditure',
                                   'showlegend':True}]),
                     dict(label = 'eduattain_doctoral',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,True, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Doctoral Education Attainment',
                                   'showlegend':True}]),
                     dict(label = 'eduattain_bachelor',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, True,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]},
                                  {'title': "Bachelor's Education Attainment",
                                   'showlegend':True}]),
                     dict(label = 'eduattain_master',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,True,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': "Master's Education Attainment",
                                   'showlegend':True}]),
                     dict(label = 'eduattain_sec',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,True,False, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]},
                                  {'title': 'Secondary Education Attainment',
                                   'showlegend':True}]),
                     dict(label = 'eduattain_postsec',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,True, False,False,False,False, False,False,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Post-Secondary Education Attainment',
                                   'showlegend':True}]),
                     dict(label = 'eduattain_primary',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, True,False,False,False, False,False,False,False, False,False,False,False,False,False,False]},
                                  {'title': 'Primary Education Attainment',
                                   'showlegend':True}]),
                     dict(label = 'eduattain_tertiary',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,True,False,False, False,False,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Tertiary Education Attainment',
                                   'showlegend':True}]),
                     dict(label = 'eduattain_uppersec',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,True,False, False,False,False,False, False,False,False,False,False,False,False]},
                                  {'title': 'Upper Secondary Education Attainment',
                                   'showlegend':True}]),
                     dict(label = 'expense',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,True, False,False,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Total Expenses (% GDP)',
                                   'showlegend':True}]),
                     dict(label = 'life_expectatbirth_fem',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, True,False,False,False, False,False,False,False,False,False,False]},
                                  {'title': 'Life Expectancy, Female (Years)',
                                   'showlegend':True}]),
                     dict(label = 'life_expectatbirth_male',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,True,False,False, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Life Expectancy Male (Years)',
                                   'showlegend':True}]),
                     dict(label = 'life_expectatbirth_total',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,True,False, False,False,False,False,False,False,False]},
                                  {'title': 'Life Expectancy Total (Years)',
                                   'showlegend':True}]),
                     dict(label = 'milexp_gdp',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,True, False,False,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Military Expenditure (% GDP)',
                                   'showlegend':True}]),
                     dict(label = 'milexp_usd',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, True,False,False,False,False,False,False]},
                                  {'title': 'Military Expenditure (USD)',
                                   'showlegend':True}]),
                     dict(label = 'totalreserves',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,True,False,False,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Total Reserves (% external debt)',
                                   'showlegend':True}]),
                     dict(label = 'unemptotal_modeiloest',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,True,False,False,False,False]},
                                  {'title': 'Unemployment ILO (% Total Labor Force)',
                                   'showlegend':True}]),
                     dict(label = 'unemptotal_nationalest',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,True,False,False,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Unemployment National (% Total Labor Force)',
                                   'showlegend':True}]),
                     dict(label = 'happiness_score',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,True,False,False]},
                                  {'title': 'Happiness Score (1-10)',
                                   'showlegend':True}]),
                     dict(label = 'social_support',
                          method = 'update',
                          args = [{'visible': [False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False,False,True,False]}, # the index of True aligns with the indices of plot traces
                                  {'title': 'Social Support (1-10)',
                                   'showlegend':True}]),


                    ])
                )
            ])


              

    return  plotly.io.to_json(fig)


@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)

    return graphJSON



if __name__ == '__main__':
    app.run()
