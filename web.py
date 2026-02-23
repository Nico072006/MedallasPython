import pandas as pd
from dash import html,Input,Output,dcc
import plotly.express as px
import dash


df =pd.read_csv("medallas.csv")
print (df)

def calcular_rendimiento(total):
    if total > 20: return 'Alto'
    elif total >= 10: return 'Medio'
    else: return 'Bajo'
df['nivel_rendimiento'] = df['Total'].apply(calcular_rendimiento)

app =dash.Dash(__name__)

app.layout=html.Div([
    html.H1("Análisis de Medallería Olímpica", style={
        "textAlign": "center",
        "color": "#ffffff", 
        "padding": "20px",
        "fontFamily": "Arial", 
        "backgroundColor": "#1a1a1a", 
        "margin": "0"
    }),
    html.Label("Selecionar Pais",style={"margin":"10px"}),
    dcc.Dropdown(id="filtro_pais",
                 options=[{"label": "Todos los Países", "value": "TODOS"}] + 
                    [{"label": p, "value": p} for p in sorted(df["Pais"].unique())],
                value="TODOS",
                style={"width": "100%", "margin": "auto"}
                 ),
    html.Br(),

    dcc.Tabs([
        dcc.Tab(label='Top 10 Países', children=[dcc.Graph(id='Barras_top')]),
        dcc.Tab(label="Distribución", children=[dcc.Graph(id='Histograma')]),
        dcc.Tab(label="Análisis Oro/Total", children=[dcc.Graph(id='Dispersion')]),
        dcc.Tab(label="Rendimiento", children=[dcc.Graph(id='Pie')])
    ],style={"fontWeight":"bold","color":"#ffffff"})

])
@app.callback(
    Output("Barras_top", "figure"),
    Output("Histograma", "figure"),
    Output("Dispersion", "figure"),
    Output("Pie", "figure"),
    Input("filtro_pais", "value")
)

def actualizar (filtro_pais):
    if filtro_pais=="TODOS":
        filtro=df
    else:
        filtro=df[df["Pais"]==filtro_pais]

    top_10=df.sort_values("Total",ascending=False).head(10)
    fig_barras=px.bar(top_10,x="Total",y="Pais",title="Top 10 Países con más Medallas",
                        color_discrete_sequence=["#ff0000"])
        
    fig_hist=px.histogram(df,x="Total",nbins=15,title="Frecuencia de Medallas Global")

    fig_disper=px.scatter(filtro,x="Oro",y="Total",size="Total",title=f"Relación Oro vs Total - {filtro_pais}" )

    fig_pie = px.pie(filtro, names="nivel_rendimiento", title=f"Nivel de Rendimiento: {filtro_pais}")

    return fig_barras, fig_hist, fig_disper, fig_pie

if __name__ =='__main__':
    app.run(debug=True)
