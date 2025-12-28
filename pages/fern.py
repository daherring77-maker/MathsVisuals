import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template, add_download_buttons, run_ollama_command
from functools import lru_cache

st.title("🌀 Barnsley Fern")

def barnsley_fern(n_points=50000):
    # Initialize arrays for x and y coordinates
    x = np.zeros(n_points)
    y = np.zeros(n_points)
    
    # Barnsley fern transformation probabilities and coefficients
    # Each transformation has a probability and 6 coefficients (a-f)
    transformations = [
        (0.01, [0, 0, 0, 0.16, 0, 0]),      # Stem (1%)
        (0.85, [0.85, 0.04, -0.04, 0.85, 0, 1.6]),  # Main stem (85%)
        (0.07, [0.2, -0.26, 0.23, 0.22, 0, 1.6]),   # Left side (7%)
        (0.07, [-0.15, 0.28, 0.26, 0.24, 0, 0.44])  # Right side (7%)
    ]
    
    # Generate points
    for i in range(1, n_points):
        # Choose transformation based on probabilities
        rand = np.random.random()
        cumulative = 0
        for prob, coeffs in transformations:
            cumulative += prob
            if rand <= cumulative:
                a, b, c, d, e, f = coeffs
                x[i] = a * x[i-1] + b * y[i-1] + e
                y[i] = c * x[i-1] + d * y[i-1] + f
                break
    
    return x, y

# Generate fern points
x, y = barnsley_fern(50000)

# Create the plot
fig = go.Figure()

# Add scatter plot with green color
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers',
    marker=dict(
        color='green',
        size=1,
        opacity=0.6
    ),
    showlegend=False
))

# Update layout for better visualization
apply_plotly_template(fig)
fig.update_layout(
    title="Green Fractal Fern",
    xaxis_title="X Coordinate",
    yaxis_title="Y Coordinate",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    width=800,
    height=600,
    plot_bgcolor='black'
)

# Show the plot
st.plotly_chart(fig, width='content', config=plotly_config())

#fig.show()
