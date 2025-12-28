import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.plotting import plotly_config, apply_plotly_template, add_download_buttons
from functools import lru_cache

st.title("🌀 Archimedes Spiral")


# Create the figure
fig = go.Figure()

# Define the Archimedes spiral: r = a * theta
a = 0.2  # Controls the spacing between turns
theta = np.linspace(0, 6 * np.pi, 1000)  # Angle from 0 to 6π
r = a * theta  # Radius based on the spiral equation

# Convert to Cartesian coordinates
x = r * np.cos(theta)
y = r * np.sin(theta)

# Add the spiral trace
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='lines',
    line=dict(color='royalblue', width=2),
    name='Archimedes Spiral'
))

# Add a point at the start of the spiral
fig.add_trace(go.Scatter(
    x=[x[0]],
    y=[y[0]],
    mode='markers',
    marker=dict(color='red', size=8),
    name='Start Point'
))

# Add a point at the end of the spiral
fig.add_trace(go.Scatter(
    x=[x[-1]],
    y=[y[-1]],
    mode='markers',
    marker=dict(color='green', size=8),
    name='End Point'
))

apply_plotly_template(fig)
# Update layout
fig.update_layout(
    title='Archimedes Spiral',
    xaxis_title='X',
    yaxis_title='Y',
    xaxis=dict(showgrid=True, zeroline=True),
    yaxis=dict(showgrid=True, zeroline=True),
    width=600,
    height=600,
    showlegend=True,
    plot_bgcolor='white',
    hovermode='closest'
)

# Add grid lines
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
st.plotly_chart(fig, width='content', config=plotly_config())
# Show the plot
#fig.show()
