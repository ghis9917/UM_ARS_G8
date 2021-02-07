import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

from src.OptimizationFunction import OptimizationFunction
from src.ParticleSwarmOptimization import PSO
import plotly.graph_objects as go

import Constants as Const
from colour import Color

from src.StackOverflowUtils import get_continuous_color

if __name__ == '__main__':
    repeats = 50
    func_name = 'Rosenbrock'
    test_name = 'Area'

    # to_be_tested_values = np.linspace(0, 4, 15)
    to_be_tested_values = [100, 50, 25, 10, 5]

    opti = OptimizationFunction(a=0, b=100)
    selected_function = opti.rosenbrock

    data = {to_be_tested_value: dict(
        avg_vel=[],
        avg_alt=[],
        best_alt=[],
    ) for to_be_tested_value in to_be_tested_values}

    for to_be_tested_value in to_be_tested_values:
        Const.C1 = to_be_tested_value
        # Const.C2 = to_be_tested_value
        # Const.MAX_POS = to_be_tested_value
        # Const.MIN_POS = -to_be_tested_value
        for repeat in range(repeats):
            # ---Create PSO object to be used in the animation frames
            pso = PSO(selected_function)
            pso.optimize()
            data.get(to_be_tested_value).get('avg_vel').append(pso.average_velocity_history)
            data.get(to_be_tested_value).get('avg_alt').append(pso.average_altitude_history)
            data.get(to_be_tested_value).get('best_alt').append(pso.best_altitude_history)

    fig = make_subplots(rows=2, cols=2, subplot_titles=("Average Velocity", "Average Altitude", "Best Altitude", ""))

    plotly_colors, _ = px.colors.convert_colors_to_same_type(px.colors.qualitative.Plotly)
    colorscale = px.colors.make_colorscale(plotly_colors)

    colors = [get_continuous_color(colorscale, intermed=i) for i in np.linspace(0, 1, len(to_be_tested_values))]

    for i, to_be_tested_value in enumerate(to_be_tested_values):
        fig.add_trace(go.Scatter(x=list(range(Const.N_ITERATIONS)),
                                 y=np.mean(data.get(to_be_tested_value).get('avg_vel'), axis=0),
                                 name=f'C1 = {np.round(to_be_tested_value, decimals=3)}',
                                 line=dict(color=colors[i], width=1)
                                 ),
                      row=1, col=1)

    for i, to_be_tested_value in enumerate(to_be_tested_values):
        fig.add_trace(go.Scatter(x=list(range(Const.N_ITERATIONS)),
                                 y=np.mean(data.get(to_be_tested_value).get('avg_alt'), axis=0),
                                 name=f'C2 = {to_be_tested_value}',
                                 showlegend=False,
                                 line=dict(color=colors[i], width=1)
                                 ),
                      row=1, col=2)

    for i, to_be_tested_value in enumerate(to_be_tested_values):
        fig.add_trace(go.Scatter(x=list(range(Const.N_ITERATIONS)),
                                 y=np.mean(data.get(to_be_tested_value).get('best_alt'), axis=0),
                                 name=f'C2 = {to_be_tested_value}',
                                 showlegend=False,
                                 line=dict(color=colors[i], width=1)
                                 ),
                      row=2, col=1)

    fig.update_layout(
        title_text=f"Testing {test_name} for {func_name} avg over {repeats} tries "
                   f"with N_SWARMS = {Const.N_SWARMS} and N_PARTICLES = {Const.N_PARTICLES}"
    )
    fig.show()
    fig.write_html(f"{test_name.replace(' ','_')}_{func_name}_{repeats}_{Const.N_SWARMS}_{Const.N_PARTICLES}.html",
                   include_plotlyjs='cdn', include_mathjax=False, auto_play=False)