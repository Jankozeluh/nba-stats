import plotly.express as px
import plotly.io as pio
import streamlit as st


def display_bar_chart(data, x, y):
    if y in data.columns:
        fig = px.bar(data, x=x, y=y, labels={y: y})
        fig.update_layout(title=f"{y} - Bar Chart")
        st.plotly_chart(fig)


def display_line_chart(data, x, y):
    if y in data.columns:
        fig = px.line(data, x=x, y=y, labels={x: x, y: y})
        fig.update_layout(title=f"{y} - Line Chart")
        st.plotly_chart(fig)


def display_scatter_chart(data, x, y):
    if x in data.columns and y in data.columns:
        fig = px.scatter(data, x=x, y=y, labels={x: x, y: y})
        fig.update_layout(title=f"{y} vs. {x} - Scatter Chart")
        st.plotly_chart(fig)


def set_plotly_layout(layout):
    pio.templates.default_layout = layout
