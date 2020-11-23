from flask import Flask, render_template, request
import plotly
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import csv
import json

# ===========================
# INITIATE APP INSTANCE
# ===========================
app = Flask(__name__)

# ===========================
# IMPORT DATA
# ===========================
# TODO change when importing into flask
df = pd.read_csv('allData.csv', header=0)
val_desc = pd.read_csv('valdescs.csv', header=0)
with open('bycont.csv') as csvfile:
    by_continent = list(csv.reader(csvfile))[0]

# drop columns that are mostly empty
df = df.drop(columns=['unempbenefits', 'afp_totlabforce', 'afp_total', 'cgd_total', 'peacekeepers',
                      'suic_mortalityrate_pop', 'suic_mortalityrate_female', 'suic_mortalityrate_male'])


# ===========================
# APP CONTENT
# ===========================
@app.route('/')
def index():
    feature = 'Bar'
    bar = create_plot(feature)
    bar2 = create_plot2()
    return render_template('index.html',
                           plot=bar, plot2=bar2,
                           tables=[val_desc.to_html(classes='data')], titles=val_desc.columns.values)


def create_plot2():
    # PLOT DS SALARY DATA - BAR
    fig2 = px.bar(df, x="country", y="pay_usd", title="Data Science Job Salaries by Country")

    fig2.update_layout(
        barmode='stack',
        xaxis={'categoryorder':'array', 'categoryarray':by_continent},
        yaxis={'title': 'Yearly Income (USD)'})
    fig2.update_layout(
        autosize=False,
        width=1200,
        height=500)
    return plotly.io.to_json(fig2)


def create_plot(feature):
    # ===========================
    # BOX-SCATTER PLOT
    # ===========================
    if feature == "All Countries Box-Scatter Plot":

        fig = go.Figure()

        for column in df.columns[1:].to_list():
            fig.add_trace(
                go.Box(
                    y=df[column],
                    name=column, boxpoints='all', hovertext=df["country"]
                )
            )

        fig.update_layout(
            title="All Countries Box-Scatter Plot",
            updatemenus=[go.layout.Updatemenu(
                active=0,
                buttons=list(
                    [
                        dict(label='cureduexpen_pri',
                             method='update',
                             args=[{'visible': [True, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Primary Education Expenditure',
                                    'showlegend': True}]),
                        dict(label='cureduexpen_sec',
                             method='update',
                             args=[{'visible': [False, True, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': 'Secondary Education Expenditure',
                                    'showlegend': True}]),
                        dict(label='cureduexpen_ter',
                             method='update',
                             args=[{'visible': [False, False, True, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Tertiary Education Expenditure',
                                    'showlegend': True}]),
                        dict(label='cureduexpen_total',
                             method='update',
                             args=[{'visible': [False, False, False, True, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': 'Total Education Expenditure',
                                    'showlegend': True}]),
                        dict(label='eduattain_doctoral',
                             method='update',
                             args=[{'visible': [False, False, False, False, True, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Doctoral Education Attainment',
                                    'showlegend': True}]),
                        dict(label='eduattain_bachelor',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, True, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': "Bachelor's Education Attainment",
                                    'showlegend': True}]),
                        dict(label='eduattain_master',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, True, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': "Master's Education Attainment",
                                    'showlegend': True}]),
                        dict(label='eduattain_sec',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, True, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': 'Secondary Education Attainment',
                                    'showlegend': True}]),
                        dict(label='eduattain_postsec',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, True, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Post-Secondary Education Attainment',
                                    'showlegend': True}]),
                        dict(label='eduattain_primary',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, True,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': 'Primary Education Attainment',
                                    'showlegend': True}]),
                        dict(label='eduattain_tertiary',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                True, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Tertiary Education Attainment',
                                    'showlegend': True}]),
                        dict(label='eduattain_uppersec',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, True, False, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': 'Upper Secondary Education Attainment',
                                    'showlegend': True}]),
                        dict(label='expense',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, True, False, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Total Expenses (% GDP)',
                                    'showlegend': True}]),
                        dict(label='life_expectatbirth_fem',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, True, False, False, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': 'Life Expectancy, Female (Years)',
                                    'showlegend': True}]),
                        dict(label='life_expectatbirth_male',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, True, False, False, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Life Expectancy Male (Years)',
                                    'showlegend': True}]),
                        dict(label='life_expectatbirth_total',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, True, False, False, False, False,
                                                False, False, False, False]},
                                   {'title': 'Life Expectancy Total (Years)',
                                    'showlegend': True}]),
                        dict(label='milexp_gdp',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, True, False, False, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Military Expenditure (% GDP)',
                                    'showlegend': True}]),
                        dict(label='milexp_usd',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, True, False, False,
                                                False, False, False, False]},
                                   {'title': 'Military Expenditure (USD)',
                                    'showlegend': True}]),
                        dict(label='totalreserves',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, True, False,
                                                False, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Total Reserves (% external debt)',
                                    'showlegend': True}]),
                        dict(label='unemptotal_modeiloest',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, True,
                                                False, False, False, False]},
                                   {'title': 'Unemployment ILO (% Total Labor Force)',
                                    'showlegend': True}]),
                        dict(label='unemptotal_nationalest',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                True, False, False, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Unemployment National (% Total Labor Force)',
                                    'showlegend': True}]),
                        dict(label='happiness_score',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, True, False, False]},
                                   {'title': 'Happiness Score (1-10)',
                                    'showlegend': True}]),
                        dict(label='social_support',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, True, False]},
                                   # the index of True aligns with the indices of plot traces
                                   {'title': 'Social Support (1-10)',
                                    'showlegend': True}]),
                        dict(label='pay',
                             method='update',
                             args=[{'visible': [False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, False, False, False, False, False, False, False,
                                                False, False, False, True]},
                                   {'title': 'Pay (USD)',
                                    'showlegend': True}]),

                    ])
            )
            ])


    # ===========================
    # BAR PLOT
    # ===========================
    else:

        # scale all columns from 0-1
        scaler = MinMaxScaler()
        df2 = df.copy()
        df2.loc[:, df2.columns != 'country'] = scaler.fit_transform(df2.loc[:, df2.columns != 'country'])

        # PLOT DATA - BAR
        fig = px.bar(df2, x="country", y=list(df2.columns[1:]), title="All Countries Stacked Bar Plot by Attribute")

        fig.update_layout(
            barmode='stack',
            xaxis={'categoryorder':'array', 'categoryarray':by_continent})
        fig.update_xaxes(title={'text': None})

    # ===========================
    # RESIZE PLOT
    # ===========================
    fig.update_layout(
        autosize=False,
        width=1200,
        height=500)

    return plotly.io.to_json(fig)


# ===========================
# DROPDOWN FUNCTIONALITY
# ===========================
@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON = create_plot(feature)

    return graphJSON


if __name__ == '__main__':
    app.run()
