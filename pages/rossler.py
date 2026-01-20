import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template

st.title("🌀 Rössler Attractor")

# Define parameters for the Rössler attractor
a = 0.2
b = 0.2
c = 5.7

# Time parameters
dt = 0.01
steps = 30000

# Initialize arrays for x, y, z coordinates
x = np.zeros(steps)
y = np.zeros(steps)
z = np.zeros(steps)

# Initial conditions
x[0] = 0.1
y[0] = 0.0
z[0] = 0.0

# Integration using Euler's method
for i in range(steps-1):
    dx = -y[i] - z[i]
    dy = x[i] + a * y[i]
    dz = b + z[i] * (x[i] - c)
    
    x[i+1] = x[i] + dx * dt
    y[i+1] = y[i] + dy * dt
    z[i+1] = z[i] + dz * dt

# Create 3D scatter plot
fig = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines',
    line=dict(width=1, color=z, colorscale='Viridis'),
    hovertemplate='<b>X:</b> %{x:.2f}<br><b>Y:</b> %{y:.2f}<br><b>Z:</b> %{z:.2f}<extra></extra>'
)])

# Update layout
apply_plotly_template(fig)
fig.update_layout(
    title='Rössler Attractor',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='cube'
    ),
    width=800,
    height=600,
    margin=dict(l=50, r=50, b=50, t=100)
)

# Show the plot
st.plotly_chart(fig, width='stretch', config=plotly_config())

