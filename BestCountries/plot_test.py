# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler
# import plotly.express as px
#
#
# # IMPORT DATA
# alldf = pd.read_csv('allData.csv', header = 0)
#
# # scale data and name as df2
# scaler = MinMaxScaler()
# df2 = alldf.copy()
# df2.loc[:, df2.columns != 'country'] = scaler.fit_transform(df2.loc[:, df2.columns != 'country'])
#
# # PLOT DATA - BAR
# fig = px.bar(df2, x="country", y=list(df2.columns[1:]), title="MERP")
# fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
# fig.show()