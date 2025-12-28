import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.plotting import plotly_config, apply_plotly_template
import random

st.title("❄️ Chaotic Snowflake Generator")

mode = st.radio("Mode", ["Explorer", "Lesson: Why Are Snowflakes Unique?"], 
                horizontal=True, label_visibility="collapsed")

if mode == "Lesson: Why Are Snowflakes Unique?":
    st.info("""
    🎯 Each snowflake’s path through the cloud is unique — tiny changes in temp/humidity → branching chaos.
    💡 Try:
      - Increase **Chaos** → more irregular arms  
      - Reduce **Stickiness** → sparse dendrites  
      - Toggle **Symmetry** → break nature’s 6-fold rule  
    📚 Real snowflakes obey physics — but *this* one obeys *your* parameters!
    """, icon="🔬")

# --- Controls ---
with st.expander("🎛️ Growth Parameters", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        n_particles = st.slider("Particles", 100, 5000, 1000, step=100)
        stickiness = st.slider("Stickiness", 0.1, 1.0, 0.8, step=0.05)
        chaos = st.slider("Chaos (per-step noise)", 0.0, 0.5, 0.1, step=0.02)
    with col2:
        symmetry = st.select_slider("Symmetry", options=[1, 2, 3, 6], value=6)
        twist = st.slider("Twist (radians)", 0.0, np.pi, 0.0, step=0.1)
        depth = st.slider("Max radius", 10, 50, 30, step=5)

# --- Generate snowflake (cached) ---
@st.cache_data(ttl=600)
def generate_snowflake(n_particles, stickiness, chaos, symmetry, twist, depth):
    # Seed at origin
    points = [(0.0, 0.0, 0.0)]
    occupied = set([(0, 0)])

    # Launch random walkers
    for _ in range(n_particles):
        # Start walker on circle of radius ~depth
        angle = random.uniform(0, 2*np.pi)
        r = depth * 0.9 + random.uniform(-2, 2)
        x, y = r * np.cos(angle), r * np.sin(angle)
        
        for _ in range(5000):  # max steps
            # Random step + chaos
            dx = random.uniform(-1, 1) + random.gauss(0, chaos)
            dy = random.uniform(-1, 1) + random.gauss(0, chaos)
            x, y = x + dx, y + dy
            
            # Reflect into 60° wedge (for 6-fold symmetry)
            theta = np.arctan2(y, x) % (2*np.pi/symmetry)
            r = np.hypot(x, y)
            x_wedge = r * np.cos(theta)
            y_wedge = r * np.sin(theta)
            
            # Snap to grid
            ix, iy = int(round(x_wedge)), int(round(y_wedge))
            if (ix, iy) in occupied:
                if random.random() < stickiness:
                    # Add all symmetric copies
                    for k in range(symmetry):
                        ang = 2*np.pi * k / symmetry + twist
                        x_out = x_wedge * np.cos(ang) - y_wedge * np.sin(ang)
                        y_out = x_wedge * np.sin(ang) + y_wedge * np.cos(ang)
                        points.append((x_out, y_out, 0.0))
                        # Optional: add slight Z variation for 3D effect
                        z = 0.2 * np.sin(5 * ang) * random.gauss(0, 0.1)
                        points[-1] = (x_out, y_out, z)
                    break
            if r > depth * 1.2 or r < 1:
                break  # escape or too close

    return np.array(points)

points = generate_snowflake(n_particles, stickiness, chaos, symmetry, twist, depth)
x, y, z = points[:,0], points[:,1], points[:,2]

# --- Plot ---
fig = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(
        size=3 + 2 * (z - z.min()),  # subtle size by height
        color=z,
        colorscale='Blues',
        opacity=0.9
    ),
    hoverinfo='skip'
))

apply_plotly_template(fig)
fig.update_layout(
    title=f"❄️ {symmetry}-Fold Chaotic Snowflake",
    scene=dict(
        xaxis_title='', yaxis_title='', zaxis_title='',
        aspectmode='data',
        camera=dict(eye=dict(x=0, y=0, z=2.5)),  # top-down view
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ),
    height=600,
    margin=dict(l=0, r=0, t=50, b=0),
    showlegend=False
)

st.plotly_chart(fig, width='stretch', config=plotly_config())

st.caption("🌀 Real snowflakes grow via diffusion-limited aggregation — this is a chaotic, interactive homage.")