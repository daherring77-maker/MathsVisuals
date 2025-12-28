import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template, add_download_buttons
from functools import lru_cache

st.title("🌀 Klein Bottle")

# --- Mode & Presets ---
mode = st.radio("Mode", ["Explorer", "Lesson: The Impossible Bottle"], 
                horizontal=True, label_visibility="collapsed")

if mode == "Lesson: The Impossible Bottle":
    st.info("""
    🎯 **Goal**: Understand why the Klein bottle *must* self-intersect in 3D.
    💡 Try: 
      - Reduce **Twist** → see symmetry emerge  
      - Switch to *Figure-8* → smoother neck  
      - Toggle *Wireframe* → see the "pinch"  
    📚 A true Klein bottle needs 4D to avoid self-intersection!
    """, icon="🔍")

# --- Parameter controls ---
with st.expander("🎛️ Geometry & Resolution", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        immersion = st.selectbox("Immersion type", ["Classic", "Figure-8"], index=0)
        twist = st.slider("Twist (phase offset)", 0.0, 2.0, 1.0 if immersion == "Classic" else 0.5, step=0.05)
        radius = st.slider("Main radius", 0.5, 3.0, 2.0, step=0.1)
        neck_scale = st.slider("Neck scale", 0.2, 2.0, 1.0, step=0.1)
    with col2:
        u_steps = st.slider("U resolution", 30, 200, 100, step=10)
        v_steps = st.slider("V resolution", 30, 200, 100, step=10)
        opacity = st.slider("Opacity", 0.3, 1.0, 0.85, step=0.05)

with st.expander("🎨 Visual Style", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        colorscale = st.selectbox("Colorscale", 
            ["Plasma", "Viridis", "Turbo", "Ice", "RdBu"], index=0)
        show_wireframe = st.toggle("Wireframe", value=True)
    with col2:
        show_contours = st.toggle("Contour lines", value=False)
        animate_rotation = st.toggle("🔄 Auto-rotate", value=False)

# --- Cached parametrisation ---
@lru_cache(maxsize=8)
def klein_bottle_cached(immersion, twist, radius, neck_scale, u_steps, v_steps):
    u = np.linspace(0, 2*np.pi, u_steps)
    v = np.linspace(0, 2*np.pi, v_steps)
    U, V = np.meshgrid(u, v)
    
    if immersion == "Classic":
        # Standard immersion (self-intersecting 'neck')
        x = (radius + np.cos(U/2 + twist*np.pi) * np.sin(V) - np.sin(U/2 + twist*np.pi) * np.sin(2*V)) * np.cos(U)
        y = (radius + np.cos(U/2 + twist*np.pi) * np.sin(V) - np.sin(U/2 + twist*np.pi) * np.sin(2*V)) * np.sin(U)
        z = neck_scale * (np.sin(U/2 + twist*np.pi) * np.sin(V) + np.cos(U/2 + twist*np.pi) * np.sin(2*V))
    else:  # Figure-8 immersion (Robert Israel parametrisation — smoother)
        R = radius
        a = neck_scale
        x = (R + a * np.cos(V/2) * np.sin(U) - a * np.sin(V/2) * np.sin(2*U)) * np.cos(V)
        y = (R + a * np.cos(V/2) * np.sin(U) - a * np.sin(V/2) * np.sin(2*U)) * np.sin(V)
        z = a * np.sin(V/2) * np.sin(U) + a * np.cos(V/2) * np.sin(2*U)
    
    return x, y, z

x, y, z = klein_bottle_cached(immersion, twist, radius, neck_scale, u_steps, v_steps)

# --- Build surface ---
surface_kwargs = dict(
    x=x, y=y, z=z,
    colorscale=colorscale,
    opacity=opacity,
    lighting=dict(ambient=0.7, diffuse=0.8, specular=0.3, roughness=0.5),
    lightposition=dict(x=100, y=200, z=0),
    showscale=False
)

if show_wireframe:
    surface_kwargs.update(
        contours=dict(
            x=dict(show=show_contours, color="rgba(255,255,255,0.3)", project=dict(x=True)),
            y=dict(show=show_contours, color="rgba(255,255,255,0.3)", project=dict(y=True)),
            z=dict(show=show_contours, color="rgba(255,255,255,0.3)", project=dict(z=True))
        )
    )

fig = go.Figure(data=go.Surface(**surface_kwargs))

# --- Animation: rotation ---
if animate_rotation:
    # Add smooth camera rotation
    frames = []
    for i, theta in enumerate(np.linspace(0, 2*np.pi, 48)):
        eye = dict(
            x=1.8 * np.cos(theta),
            y=1.8 * np.sin(theta),
            z=1.2 + 0.3 * np.sin(2*theta)
        )
        frames.append(go.Frame(layout=dict(scene_camera=dict(eye=eye))))
    
    fig.frames = frames
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="▶ Play", method="animate", args=[None, {"frame": {"duration": 60}}]),
                     dict(label="⏸ Pause", method="animate", args=[[None], {"frame": {"duration": 0}}])]
        )]
    )

# --- Layout ---
apply_plotly_template(fig)
fig.update_layout(
    title=f"Klein Bottle — {immersion} Immersion",
    scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
        aspectmode='data',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
    ),
    height=650,
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig, width='stretch', config=plotly_config())

# --- Export & info ---
st.divider()
st.subheader("📐 Geometry & Export")

# Sample a few points for metadata
n = min(5, len(x.ravel()))
sample_z = z.ravel()[:n]
add_download_buttons({
    "immersion": immersion,
    "twist": twist,
    "radius": radius,
    "neck_scale": neck_scale,
    "u_steps": u_steps,
    "v_steps": v_steps,
    "z_min": float(z.min()),
    "z_max": float(z.max()),
    "self_intersection": "Yes (in 3D)"  # always true here!
}, "klein")

# --- Fun fact / teaching note ---
st.caption("""
💡 **Fun fact**: The Klein bottle has *no inside or outside* — like a Möbius strip, but closed.
In 4D, it can exist without self-intersection. Here, the 'neck' passes through the 'body' — an artifact of 3D projection.
""")