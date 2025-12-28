import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template, add_download_buttons, run_ollama_command
from functools import lru_cache

def snowflake_surface(u_steps=120, v_steps=120):
    # Higher resolution for crisp edges
    u = np.linspace(0, 2*np.pi, u_steps)
    v = np.linspace(0, 2*np.pi, v_steps)
    U, V = np.meshgrid(u, v)

    # 🌨️ Snowflake-inspired modulations:
    # - 6-fold symmetry in radial arm (sin(6V))
    # - Delicate branching (cos(12V) * exp(-|cos(U)|))
    # - Icicle tips (sin(U) sharpens at poles)
    
    R = 4 * (1 + 0.3 * np.sin(6 * V) + 0.1 * np.cos(12 * V) * np.exp(-np.abs(np.cos(U))))
    x = R * np.cos(2 * V)
    y = R * np.sin(2 * V)
    z = np.sin(U) * (1 + 0.4 * np.cos(6 * V))  # 6-point vertical ripple

    return x, y, z

# Generate
x, y, z = snowflake_surface()

# 🎨 Winter palette + realistic ice lighting
fig = go.Figure(data=[go.Surface(
    x=x, y=y, z=z,
    colorscale=[
        [0.0, 'rgb(200, 230, 255)'],   # pale sky blue (core)
        [0.4, 'rgb(180, 220, 255)'],
        [0.7, 'rgb(150, 200, 255)'],
        [1.0, 'rgb(255, 255, 255)']    # pure white tips
    ],
    showscale=False,
    lighting=dict(
        ambient=0.6,
        diffuse=0.8,
        specular=0.5,
        roughness=0.3,   # smooth ice
        fresnel=0.6      # glint at edges
    ),
    lightposition=dict(x=5, y=5, z=10),
    contours={
        "z": {"show": True, "start": -1.2, "end": 1.2, "size": 0.2, "color": "rgba(255,255,255,0.2)"},
        "x": {"show": False},
        "y": {"show": False}
    }
)])
apply_plotly_template(fig)
fig.update_layout(
    title=dict(
        text="❄️ 6-Fold Parametric Snowflake",
        font=dict(size=24, color='white'),
        x=0.5
    ),
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='data',
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.2),
            up=dict(x=0, y=0, z=1)
        ),
        bgcolor='rgb(10, 20, 40)'  # deep winter night
    ),
    paper_bgcolor='rgb(5, 10, 20)',
    plot_bgcolor='rgb(5, 10, 20)',
    margin=dict(l=0, r=0, t=50, b=0),
    width=900,
    height=700
)

# 🌀 Gentle auto-rotation for immersive view
fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[dict(
            label="▶️ Rotate",
            method="animate",
            args=[None, {
                "frame": {"duration": 50},
                "fromcurrent": True,
                "transition": {"duration": 0},
                "mode": "immediate"
            }]
        )]
    )]
)

# Generate frames for smooth rotation
frames = []
for i in range(0, 360, 5):
    frames.append(go.Frame(
        layout=dict(
            scene_camera=dict(
                eye=dict(
                    x=1.8 * np.cos(np.radians(i)),
                    y=1.8 * np.sin(np.radians(i)),
                    z=1.2
                )
            )
        )
    ))

fig.frames = frames
st.plotly_chart(fig, width='content', config=plotly_config())
#fig.show()