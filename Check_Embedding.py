import pandas as pd
import numpy as np

import holoviews as hv
hv.extension('bokeh')

import thisnotthat as tnt

import panel as pn
pn.extension('tabulator')

df = pd.read_csv('Ghent_RC_Full_Embedding_Info.csv', index_col=0)
# df.head()

with open('Embedding.npy', 'rb') as f:
    embedding = np.load(f)

map_plot = tnt.BokehPlotPane(
    embedding,
    labels=df.Archetype,
#     marker_size=numeric_vector,
    hover_text=df.Archetype,
    tools='pan,wheel_zoom,lasso_select,box_select,tap,save,reset,help',
    width=800,
)

data_view = tnt.DataPane(
    df[['Archetype', 'Player_Name', 'Decklist']],
    width=800,
    height=200,
)
data_view.link_to_plot(map_plot)

deck_info_view = tnt.InformationPane(
    df,
    """# {Archetype}
Player: {Player_Name}

Rank: {Rank}
# Decklist
{PpDecklist}
    """,
    height=800,
)
deck_info_view.link_to_plot(map_plot)

diff_info_view = tnt.InformationPane(
    df,
    """
# Differences From Archetype Median
{PpDiff}
    """,
    height=800,
)
diff_info_view.link_to_plot(map_plot)

app = pn.Row(pn.Column(map_plot, data_view), deck_info_view, diff_info_view)
app.servable()

