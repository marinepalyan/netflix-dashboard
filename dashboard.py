import dash
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

data = pd.read_csv("netflix_titles_cleaned.csv")
app = dash.Dash(__name__)


fig1 = px.bar(data.type.value_counts())
obj1 = html.Div(
    children=[
        html.H1(children="Type Categories", ),
        html.P(
            children="Analysis of 2 categories of Netflix shows",
        ),
        dcc.Graph(figure=fig1)
    ]
)

fig2 = px.histogram(data, y='country', color='type', width=20)
fig2.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
obj2 = html.Div(
    children=[
        html.H1(children="Countries", ),
        html.P(
            children="Countries according to type",
        ),
        dcc.Graph(figure=fig2)
    ]
)

# Duration
obj3 = html.Div(children=[
    html.H1(children='duration Composition'),
    dcc.Dropdown(id='duration-dropdown',
                 options=[{'label': x, 'value': x}
                          for x in data.type.unique()],
                 multi=False, clearable=True),
    dcc.Graph(id='bar-chart')
])


# set up the callback function
@app.callback(
    Output(component_id="bar-chart", component_property="figure"),
    [Input(component_id="duration-dropdown", component_property="value")],
)
def display_duration_composition(selected_duration):
    filtered_duration = data[data.type == selected_duration]
    barchart = px.bar(
        data_frame=filtered_duration,
        y="duration",
        opacity=0.9)
    barchart.update_layout(xaxis={'categoryorder': 'total descending'})

    return barchart


fig4 = px.histogram(data, x='rating', color='type')
fig4.update_layout(barmode='stack')
obj4 = html.Div(
    children=[
        html.H1(children="Rating Types", ),
        html.P(
            children="Different Ratings of Netflix shows",
        ),
        dcc.Graph(figure=fig4)
    ]
)

obj5 = dash.dash_table.DataTable(data.to_dict('records'), [{"name": i, "id": i} for i in data.columns],
                                 filter_action='native',
                                 style_table={
                                     'height': 100,
                                 },
                                 style_data={
                                     'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                                     'overflow': 'hidden',
                                     'textOverflow': 'ellipsis',
                                 },
                                 page_size=10
                                 )

app.layout = html.Div(
    children=[obj1, obj2, obj3, obj4, obj5]
)

if __name__ == "__main__":
    app.run_server(debug=True)
