import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Optional

class Plotter:
    def __init__(self):
        self.color_scheme = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'tertiary': '#2ca02c',
            'background': '#f8f9fa'
        }

    def create_time_series(self, 
                          data: pd.DataFrame,
                          title: str,
                          y_axis_title: str,
                          x_axis_title: str = "Date") -> go.Figure:
        """
        Create a basic time series plot
        """
        fig = go.Figure()
        
        for column in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[column],
                    name=column,
                    mode='lines'
                )
            )

        fig.update_layout(
            title=title,
            xaxis_title=x_axis_title,
            yaxis_title=y_axis_title,
            template='plotly_white',
            hovermode='x unified'
        )

        return fig

    def create_volatility_plot(self, 
                             vix_data: pd.DataFrame,
                             nifty_data: pd.DataFrame) -> go.Figure:
        """
        Create a plot showing VIX and Nifty price movement
        """
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add VIX line
        fig.add_trace(
            go.Scatter(
                x=vix_data.index,
                y=vix_data['Close'],
                name="India VIX",
                line=dict(color=self.color_scheme['primary'])
            ),
            secondary_y=True
        )

        # Add Nifty line
        fig.add_trace(
            go.Scatter(
                x=nifty_data.index,
                y=nifty_data['Close'],
                name="Nifty 50",
                line=dict(color=self.color_scheme['secondary'])
            ),
            secondary_y=False
        )

        fig.update_layout(
            title="Nifty 50 vs India VIX",
            template='plotly_white',
            hovermode='x unified'
        )

        fig.update_yaxes(title_text="Nifty 50", secondary_y=False)
        fig.update_yaxes(title_text="India VIX", secondary_y=True)

        return fig

    def create_fii_dii_plot(self, 
                           fii_dii_data: pd.DataFrame) -> go.Figure:
        """
        Create a plot showing FII/DII flows
        """
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=fii_dii_data.index,
                y=fii_dii_data['FII'],
                name="FII",
                marker_color=self.color_scheme['primary']
            )
        )

        fig.add_trace(
            go.Bar(
                x=fii_dii_data.index,
                y=fii_dii_data['DII'],
                name="DII",
                marker_color=self.color_scheme['secondary']
            )
        )

        fig.update_layout(
            title="FII/DII Flows",
            barmode='group',
            template='plotly_white',
            hovermode='x unified'
        )

        return fig

    def create_market_breadth_plot(self, 
                                 breadth_data: pd.DataFrame) -> go.Figure:
        """
        Create a plot showing market breadth indicators
        """
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=breadth_data.index,
                y=breadth_data['adv_dec_ratio'],
                name="Advance-Decline Ratio",
                line=dict(color=self.color_scheme['primary'])
            )
        )

        fig.update_layout(
            title="Market Breadth (Advance-Decline Ratio)",
            template='plotly_white',
            hovermode='x unified'
        )

        return fig 