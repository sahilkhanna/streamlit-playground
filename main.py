from dataclasses import dataclass
from typing import List

import numpy as np
import streamlit as st
from plotly import graph_objs as go
import pydeck as pdk


@dataclass
class AccelerometerData:
    x: float
    y: float
    z: float


def fake_random_accelerometer_data() -> AccelerometerData:
    t = len(st.session_state.coordinate_space)

    return AccelerometerData(
        x=np.sin(t * 0.1) * 0.01,
        y=np.cos(t * 0.1) * 0.01,
        z=t * 0.002,
    )


@st.fragment(run_every="100ms")
def create_live_plot(coordinate_space: List[AccelerometerData], fig):

    coordinate_space.append(fake_random_accelerometer_data())

    fig.data[0].y = [d.x for d in coordinate_space]
    fig.data[1].y = [d.y for d in coordinate_space]
    fig.data[2].y = [d.z for d in coordinate_space]

    fig.data[0].x = list(range(len(coordinate_space)))
    fig.data[1].x = list(range(len(coordinate_space)))
    fig.data[2].x = list(range(len(coordinate_space)))

    st.plotly_chart(fig, use_container_width=True)


@st.fragment(run_every="1s")
def create_3d_space(coordinate_space: List[AccelerometerData]):

    data = [
        {
            "lon": d.x,
            "lat": d.y,
            "z": d.z * 10000,
        }
        for d in coordinate_space
    ]

    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="z",
        elevation_scale=1,
        radius=500,
        get_fill_color=[255, 0, 0],
        pickable=True,
    )

    view_state = pdk.ViewState(
        longitude=0,
        latitude=0,
        zoom=12,
        pitch=60,
        bearing=30,
    )

    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

    st.pydeck_chart(deck)


def main():
    st.title("Streamlit Accelerometer Playground")

    if "coordinate_space" not in st.session_state:
        st.session_state.coordinate_space = []

    coordinate_space = st.session_state.coordinate_space

    col1, col2 = st.columns(2)

    play_line_chart = col1.button("Start Live Line Plot")
    play_3d_space = col2.button("Show 3D Space")

    fig = go.FigureWidget()
    fig.add_scatter(name="x", mode="lines")
    fig.add_scatter(name="y", mode="lines")
    fig.add_scatter(name="z", mode="lines")

    if play_line_chart:
        create_live_plot(coordinate_space, fig)

    if play_3d_space:
        create_3d_space(coordinate_space)


if __name__ == "__main__":
    main()