import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template, add_download_buttons, run_ollama_command
from functools import lru_cache

st.title("🌀 Trefoil Knot")

# Define the parametric equations
def parametric_surface(u_range=(0, 2*np.pi), v_range=(0, 2*np.pi), u_steps=50, v_steps=50):
    # Create parameter grids
    u = np.linspace(u_range[0], u_range[1], u_steps)
    v = np.linspace(v_range[0], v_range[1], v_steps)
    U, V = np.meshgrid(u, v)
    
    # Parametric equations
    x = (4 * (1 + 0.25 * np.sin(3 * V)) + np.cos(U)) * np.cos(2 * V)
    y = (4 * (1 + 0.25 * np.sin(3 * V)) + np.cos(U)) * np.sin(2 * V)
    z = np.sin(U) + 2 * np.cos(3 * V)
    
    return x, y, z

# Generate the surface
x, y, z = parametric_surface(u_steps=100, v_steps=100)

# Create the 3D surface plot
fig = go.Figure(data=[go.Surface(
    x=x, y=y, z=z,
    colorscale='Viridis',
    colorbar=dict(title="Z-Value"),
    showscale=True,
    lighting=dict(ambient=0.8, diffuse=0.8, specular=0.2),
    lightposition=dict(x=100, y=100, z=100)
)])

apply_plotly_template(fig)
# Update layout
fig.update_layout(
    title="Parametric Surface Plot",
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='data'
    ),
    width=800,
    height=600
)

# Show the plot
st.plotly_chart(fig, width='stretch', config=plotly_config())
#fig.show()
