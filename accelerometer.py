import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass


@dataclass
class AccelerometerData:
    x: float
    y: float
    z: float


def fake_accelerometer_data(t):
    # create evolving trajectory patterns
    r = 1 + 0.3 * np.sin(t * 0.03)          # slowly expanding / shrinking radius
    spiral = t * 0.02                       # slow outward spiral

    x = r * np.sin(t * 0.15) + 0.2 * np.sin(t * 0.03)
    y = r * np.cos(t * 0.15) + 0.2 * np.cos(t * 0.05)
    z = 0.8 * np.sin(t * 0.07) + spiral

    # small noise so the path feels more "alive"
    noise = np.random.normal(0, 0.02, 3)

    return AccelerometerData(
        x=x + noise[0],
        y=y + noise[1],
        z=z + noise[2],
    )


if "data" not in st.session_state:
    st.session_state.data = []

if "t" not in st.session_state:
    st.session_state.t = 0

if "running" not in st.session_state:
    st.session_state.running = False

if "interval" not in st.session_state:
    st.session_state.interval = 0.1

st.title("3D Accelerometer Visualizer")

col1, col2, col3 = st.columns(3)

if col1.button("Start"):
    st.session_state.running = True

if col2.button("Pause"):
    st.session_state.running = False

st.session_state.interval = col3.slider(
    "Update interval (seconds)",
    min_value=0.05,
    max_value=1.0,
    value=st.session_state.interval,
    step=0.05,
)


@st.fragment(run_every=st.session_state.interval)
def live_visualizer():

    paused = not st.session_state.running

    data = st.session_state.data
    t = st.session_state.t

    # generate new data only when running
    if not paused:
        new_data = fake_accelerometer_data(t)
        data.append(new_data)
        st.session_state.t += 1
    else:
        new_data = data[-1] if data else fake_accelerometer_data(t)

    # trajectory arrays
    xs = [d.x for d in data]
    ys = [d.y for d in data]
    zs = [d.z for d in data]

    # current vector
    vx = new_data.x
    vy = new_data.y
    vz = new_data.z

    fig = go.Figure()

    # trajectory
    fig.add_trace(
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="markers+lines",
            marker=dict(size=3),
            line=dict(width=2),
            name="trajectory",
        )
    )

    # vector arrow
    fig.add_trace(
        go.Scatter3d(
            x=[0, vx],
            y=[0, vy],
            z=[0, vz],
            mode="lines",
            line=dict(width=6),
            name="acceleration",
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode="cube",
        ),
        margin=dict(l=0, r=0, t=40, b=0),
    )

    st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    live_visualizer()
