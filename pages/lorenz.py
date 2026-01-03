import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template, add_download_buttons, run_ollama_command
#from functools import lru_cache

st.title("🌀 Lorenz Attractor")

# Sidebar control — but only if sidebar is used; otherwise, use tabs/expander
with st.expander("🎛️ Parameters", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        sigma = st.slider("σ (sigma)", 0.1, 30.0, 10.0, step=0.1)
    with col2:
        rho = st.slider("ρ (rho)", 0.0, 50.0, 28.0, step=0.5)
    with col3:
        beta = st.slider("β (beta)", 0.5, 5.0, 8/3, step=0.05)

    col4, col5 = st.columns(2)
    with col4:
        dt = st.select_slider("Δt", options=[0.001, 0.005, 0.01, 0.02], value=0.01)
    with col5:
        steps = st.slider("Steps", 500, 20_000, 10_000, step=500)

#@lru_cache(maxsize=16)
def solve_lorenz(sigma, rho, beta, dt, steps):
    x, y, z = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    x[0], y[0], z[0] = 0.1, 0.0, 0.0
    s, r, b = float(sigma), float(rho), float(beta)
    for i in range(steps - 1):
        dx = s * (y[i] - x[i])
        dy = x[i] * (r - z[i]) - y[i]
        dz = x[i] * y[i] - b * z[i]
        x[i+1] = x[i] + dx * dt
        y[i+1] = y[i] + dy * dt
        z[i+1] = z[i] + dz * dt
    return x, y, z

x, y, z = solve_lorenz(sigma, rho, beta, dt, steps)

# --- Animation toggle ---
animate = st.toggle("⏯️ Animate trajectory (slower)", value=False)

if animate:
    # Use frames for animation — efficient for ≤5k points
    max_frames = min(200, len(x) // 50)
    step_interval = len(x) // max_frames
    frames = []
    for i in range(1, max_frames + 1):
        end = i * step_interval
        frames.append(go.Frame(
            data=[go.Scatter3d(x=x[:end], y=y[:end], z=z[:end])],
            name=str(end)
        ))
    
    fig = go.Figure(
        data=[go.Scatter3d(
            x=x[:1], y=y[:1], z=z[:1],
            mode='lines',
            line=dict(color=z[:1], colorscale='Plasma', width=2),
            hovertemplate='X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>'
        )],
        frames=frames
    )
    
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="▶ Play",
                          method="animate",
                          args=[None, {"frame": {"duration": 30, "redraw": True},
                                       "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸ Pause",
                         method="animate",
                         args=[[None], {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate", "transition": {"duration": 0}}])]
        )],
        sliders=[{
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [{"args": [[f.name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                       "label": f.name, "method": "animate"} for f in frames]
        }]
    )
else:
    # Static (fast) version
    fig = go.Figure(data=go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=z, colorscale='Plasma', width=2),
        hovertemplate='X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>'
    ))

apply_plotly_template(fig)
fig.update_layout(
    title=f"Lorenz Attractor (σ={sigma}, ρ={rho}, β={beta:.2f})",
    scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
        aspectmode='data',
        camera=dict(eye=dict(x=1.2, y=1.2, z=0.8))
    ),
    height=600
)

st.plotly_chart(fig, width='stretch', config=plotly_config())
#fig.write_image("lorenz_thumb.png", width=300, height=200)

# --- Export & metadata ---
st.divider()
st.subheader("📁 Export & Info")
add_download_buttons({
    "sigma": sigma,
    "rho": rho,
    "beta": beta,
    "dt": dt,
    "steps": steps,
    "x_final": float(x[-1]),
    "y_final": float(y[-1]),
    "z_final": float(z[-1])
}, "lorenz")

# --- Ollama AI helper (optional toggle) ---
#if st.toggle("🤖 Ask AI for explanation (local Ollama)", value=False):
   # st.info("🚧 Currently offline — integration planned soon!", icon="💡")
    # User input
question = st.text_input("Ask about this visualisation...", key="ai_question")

if question and st.button("➤ Submit", type="primary"):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Add & show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # 🔥 Fast call — no spinner, instant result
    response = run_ollama_command(question)  # ← fast, blocking, direct

    # Show & store
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response}) 

    


