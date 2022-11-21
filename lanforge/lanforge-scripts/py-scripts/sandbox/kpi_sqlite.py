# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import sqlite3


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# load data
df = pd.read_csv('http://192.168.95.6/html-reports/2021-07-20-16-25-05_lf_check/dataplane-2021-07-20-04-28-42/kpi.csv', sep='\t')
append_df = pd.read_csv('http://192.168.95.6/html-reports/2021-07-24-03-00-01_lf_check/dataplane-2021-07-24-03-06-02/kpi.csv', sep='\t')
df = df.append(append_df, ignore_index=True)

# information on sqlite database
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html

# write to data base local for now 
conn = sqlite3.connect("qa_db") 

# can append
df.to_sql("dp_table",conn,if_exists='append')

conn.close()

conn = sqlite3.connect("qa_db")


#https://datacarpentry.org/python-ecology-lesson/09-working-with-sql/index.html
df2 = pd.read_sql_query("SELECT * from dp_table" ,conn)
print(df.head())
conn.close()
#print(df)
                 
fig = (px.scatter(df2, x="Date", y="numeric-score",
                 color="short-description", hover_name="short-description",
                 size_max=60)).update_traces(mode='lines+markers')

'''
fig = px.scatter(df, x="Date", y="numeric-score",
                 color="short-description", hover_name="short-description",
                 size_max=60)
'''              
'''
fig = px.scatter(df, x="short-description", y="numeric-score",
                 color="short-description", hover_name="short-description",
                 size_max=60)
'''
fig.update_layout(
    title="Throughput vs Packet size",
    xaxis_title="Packet Size",
    yaxis_title="Mbps",
    xaxis = {'type' : 'date'}
)


app.layout = html.Div([
    dcc.Graph(
        id='packet-size vs rate',
        figure=fig
    ),
    dcc.Graph(
        id='packet-size vs rate2',
        figure=fig
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
    