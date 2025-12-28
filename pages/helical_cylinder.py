import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template, add_download_buttons
from functools import lru_cache

st.title("🌀 Helical Cylinder")


def cylindrical_wire(radius=0.1, turns=3, height=4, steps=200, wire_radius=0.05):
    # Central helix
    t = np.linspace(0, turns * 2*np.pi, steps)
    x_center = np.cos(t)
    y_center = np.sin(t)
    z_center = (height / (turns * 2*np.pi)) * t

    # Create tube around helix (Frenet frame approximation)
    # Tangent, Normal, Binormal vectors
    dx = -np.sin(t)
    dy = np.cos(t)
    dz = height / (turns * 2*np.pi) * np.ones_like(t)
    
    # Normalize tangent
    T = np.vstack([dx, dy, dz])
    T_norm = np.linalg.norm(T, axis=0)
    T = T / T_norm

    # Approximate normal (avoiding |T| issues)
    N = np.vstack([-np.cos(t), -np.sin(t), np.zeros_like(t)])
    N_norm = np.linalg.norm(N, axis=0)
    N = N / N_norm

    # Binormal = T × N
    B = np.cross(T.T, N.T).T

    # Tube surface
    v = np.linspace(0, 2*np.pi, 30)
    X, V = np.meshgrid(x_center, v)
    Y, _ = np.meshgrid(y_center, v)
    Z, _ = np.meshgrid(z_center, v)

    # Add circular cross-section
    X_tube = X + wire_radius * (N[0] * np.cos(V) + B[0] * np.sin(V))
    Y_tube = Y + wire_radius * (N[1] * np.cos(V) + B[1] * np.sin(V))
    Z_tube = Z + wire_radius * (N[2] * np.cos(V) + B[2] * np.sin(V))

    return X_tube, Y_tube, Z_tube

# Generate
x, y, z = cylindrical_wire(wire_radius=0.08, turns=2.5, height=3)

fig = go.Figure(data=go.Surface(
    x=x, y=y, z=z,
    colorscale=[[0, 'gold'], [1, 'goldenrod']],  # metallic wire
    showscale=False,
    lighting=dict(
        ambient=0.4,
        diffuse=0.8,
        specular=0.9,
        roughness=0.1,
        fresnel=0.8
    ),
    lightposition=dict(x=5, y=5, z=5)
))
apply_plotly_template(fig)
fig.update_layout(
    title="🌀 Cylindrical Wire (3D Tube)",
    scene=dict(
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False,
        aspectmode='data',
        camera=dict(eye=dict(x=2, y=2, z=1.2)),
        bgcolor='rgb(20,30,50)'
    ),
    paper_bgcolor='rgb(10,15,30)',
    width=800, height=600
)
st.plotly_chart(fig, width='content', config=plotly_config())
#fig.show()