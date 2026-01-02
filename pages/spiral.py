import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template

st.title("🌀 3D Archimedes Spiral Surface")
# Generate data points
t = np.linspace(0, 4*np.pi, 100)
r = 1 + 0.5 * np.sin(3*t)
x = r * np.cos(t)
y = r * np.sin(t)
z = t / (2*np.pi)

# Create the 3D surface plot
fig = go.Figure(data=[go.Surface(
    x=x.reshape(10, 10),
    y=y.reshape(10, 10),
    z=z.reshape(10, 10),
    colorscale='Blues',
    colorbar=dict(title="Z-axis"),
    lighting=dict(ambient=0.8, diffuse=0.8, specular=0.5),
    lightposition=dict(x=100, y=100, z=100),
    showscale=True
)])

# Update layout
apply_plotly_template(fig)
fig.update_layout(
    title='3D Archimedean Spiral Surface',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    ),
    width=800,
    height=600
)

# Show the plot
st.plotly_chart(fig, width='stretch', config=plotly_config())
