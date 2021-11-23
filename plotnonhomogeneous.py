from pathlib import Path
import numpy as np
import pandas as pd
import typer
import plotly.graph_objects as go


def logistic(x, scale_factor, growth_factor, middle):
    return 1 + scale_factor/(1 + np.exp(-(x-middle)/growth_factor))

def main(csv: Path, output: Path, origin_date: int = 100, origin_height: int=1250, burnin:int =50, show: bool = False, subsample: int=20):
    df = pd.read_csv(csv, sep='\t', comment='#', )
    df = df[df.index > burnin/100 * len(df)]

    scale_factor = df['nonhomogeneousClockScaleFactor'].mean()
    growth_factor = df['nonhomogeneousClockGrowthFactor'].mean()
    middle = df['nonhomogeneousClockMiddle'].mean()

    x = np.arange(origin_height)
    y = 1 + scale_factor/(1 + np.exp(-(x-middle)/growth_factor))
    
    fig = go.Figure()
    for index, row in df.iterrows():
        if index % subsample == 0:
            y = logistic(x, row['nonhomogeneousClockScaleFactor'], row['nonhomogeneousClockGrowthFactor'], row['nonhomogeneousClockMiddle'])
            fig.add_trace(go.Scatter(x=(origin_height-x)+origin_date, y=y, opacity=0.1, line=dict(color='firebrick', width=4)))

    y = 1 + scale_factor/(1 + np.exp(-(x-middle)/growth_factor))
    fig.add_trace(go.Scatter(x=(origin_height-x)+origin_date, y=y))

    fig.update_layout(showlegend=False)
    fig.update_layout(
        width=800,
        height=400,
        xaxis_title='year',
        yaxis_title='rate of change',
        plot_bgcolor='white',
        font_family="Linux Libertine O",
        font_color="black",
    )
    fig.update_xaxes(showline=True, linewidth=0.5, mirror=True, ticks='outside', linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, mirror=True, ticks='outside', linecolor='black')

    if output:
        print(f"Outputting to {output}")
        fig.write_image(output)

    if show:
        fig.show()


if __name__ == "__main__":
    typer.run(main)

