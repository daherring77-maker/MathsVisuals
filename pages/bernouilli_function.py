import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template

st.title("🌀 Bernouilli Polynomials")
# Create meshgrid for 3D surface
x = np.linspace(0, 1, 50)
n_vals = np.arange(0, 6)
X, N = np.meshgrid(x, n_vals)

# Create the 3D surface data
Z = np.zeros_like(X)
for i, n in enumerate(n_vals):
    for j, x_val in enumerate(x):
        if n == 0:
            Z[i,j] = 1
        elif n == 1:
            Z[i,j] = x_val - 0.5
        elif n == 2:
            Z[i,j] = x_val**2 - x_val + 1/6
        elif n == 3:
            Z[i,j] = x_val**3 - 3*x_val**2/2 + x_val/2
        elif n == 4:
            Z[i,j] = x_val**4 - 2*x_val**3 + x_val**2 - 1/30
        elif n == 5:
            Z[i,j] = x_val**5 - 5*x_val**4/2 + 5*x_val**3/3 - x_val/6

# Create 3D surface plot
fig = go.Figure(data=[go.Surface(
    x=X, y=N, z=Z,
    colorscale='Viridis',
    opacity=0.8,
    colorbar=dict(title="Bₙ(x)")
)])

apply_plotly_template(fig)
fig.update_layout(
    title='Bernoulli Polynomials Surface',
    scene=dict(
        xaxis_title='x',
        yaxis_title='n (Polynomial Order)',
        zaxis_title='Bₙ(x)',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
    ),
    width=800,
    height=600
)
st.plotly_chart(fig, width='stretch', config=plotly_config())
#fig.show()
