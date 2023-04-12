# This Python file uses the following encoding: utf-8

import random
from numpy import ndarray
from numpy import max
from numpy import min
from numpy import unique
from numpy import full
from typing import Tuple
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QScatterSeries
from PySide6.QtCharts import QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QFrame

from src.explorer.profile_explorer.data_profile import ProfileData
from src.explorer.profile_explorer.view_search_user import \
    SearchUserView


def _CreateSeries(xs: ndarray,
                  ys: ndarray,
                  feature_name: str,
                  color: str) -> QScatterSeries:
    series = QScatterSeries()
    series.setName(feature_name)
    series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
    series.setMarkerSize(10)
    series.setPen(QColor(color))

    for i in range(xs.shape[0]):
        series.append(xs[i], ys[i])

    return series


def _RangeOf(xs: ndarray) -> Tuple[float, float]:
    min_x, max_x = min(xs), max(xs)
    room = 0.1*(max_x - min_x)

    return min_x - room, max_x + room


def _CreateChart(points: ndarray,
                 features: ndarray,
                 title: str) -> QChart:
    chart = QChart()

    chart.setTitle(title)
    chart.setDropShadowEnabled(False)
    chart.legend().setVisible(True)

    xs = points[:, 0]
    ys = points[:, 1]

    # Prepares teh axis
    axis_x = QValueAxis()
    min_x, max_x = _RangeOf(xs=xs)
    axis_x.setRange(min_x, max_x)

    axis_y = QValueAxis()
    min_y, max_y = _RangeOf(xs=ys)
    axis_y.setRange(min_y, max_y)

    chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

    # Prepares the scatter series for every feature group.
    groups = unique(features)
    groups.sort()
    random.seed(42)

    for i in range(groups.shape[0]):
        g_xs = xs[features == groups[i]]
        g_ys = ys[features == groups[i]]

        def r(): return random.randint(0, 255)
        color = '#%02X%02X%02X' % (r(), r(), r())

        series = _CreateSeries(xs=g_xs,
                               ys=g_ys,
                               feature_name=str(groups[i]),
                               color=color)
        chart.addSeries(series)

    return chart


class ProfileView(QChartView):
    """_summary_

    Args:
        QChartView (_type_): _description_
    """

    def __init__(self,
                 scatter_chart_frame: QFrame,
                 search_user_view: SearchUserView) -> None:
        """_summary_

        Args:
            scatter_chart_frame (QFrame): _description_
            search_user_view (SearchUserView): _description_
        """
        super().__init__()

        self.search_user_view = search_user_view

        self.setRenderHint(QPainter.Antialiasing)
        scatter_chart_frame.layout().addWidget(self)

    def Plot(self, profile_data: ProfileData, feature: str = None) -> None:
        """_summary_

        Args:
            profile_data (ProfileData): _description_
            feature (str, optional): _description_. Defaults to None.
        """
        vis_embed = profile_data.ComputeVisualizationEmbeddings()

        features = None
        if feature is not None:
            features = profile_data.GetFeatures(feature=feature)
        else:
            features = full(
                shape=(vis_embed.shape[0],),
                fill_value="NO FEATURE SELECTED")

        chart = _CreateChart(
            points=vis_embed,
            features=features,
            title="User Profile t-SNE Visualization")
        self.setChart(chart)
