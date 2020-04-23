import plotly.graph_objects as go
from plotly.offline import iplot
import numpy as np

class Graph:
    figure = None

    def __init__(self):
        self.figure = go.Figure()

    def plot2DArray(self, array, name, start = 0, end = 100, steps = 100):
        self.figure.add_trace(
            go.Scatter(
                x = array[0],
                y = array[1],
                mode = 'markers',
                name = name
            )
        )

    def plot3DArray(self, array, name, start = 0, end = 100, steps = 100):
        self.figure.add_trace(
            go.Scatter3d(
                x = array[0],
                y = array[1],
                z = array[2],
                mode = 'markers',
                name = name
            )
        )

    def plotFunction(self, function, name, start = 0, end = 100, steps = 100):
        x = np.linspace(start, end, steps)
        y = np.vectorize(function)(x) # This is slow, check out https://stackoverflow.com/questions/35215161/most-efficient-way-to-map-function-over-numpy-array

        self.figure.add_trace(
            go.Scatter(x = x, y = y, mode = 'lines', name = name)
        )

    def __plot3DFunction(
        self, function,
        start = 0, end = 100, steps = 100,
        startY = None, endY = None, stepsY = None
    ):
        xs = np.linspace(start, end, steps)
        # If the parameters of the y space aren't defined we default to the parameters of the x space
        ys = np.linspace(startY or start, endY or end, stepsY or steps)

        zs = []
        for y in ys:
            arr = []

            for x in xs:
                arr.append(function(x, y))

            zs.append(arr)

        return xs, ys, zs

    def plot3DSurface(
        self, function,
        start = 0, end = 100, steps = 100,
        startY = None, endY = None, stepsY = None
    ):
        x, y, z = self.__plot3DFunction(function, start, end, steps, startY, endY, stepsY)

        self.figure.add_trace(
            go.Surface(
                x = x,
                y = y,
                z = z,
            )
        )

    def plotContourLine(
        self, function,
        start = 0, end = 100, steps = 100,
        startY = None, endY = None, stepsY = None
    ):
        x, y, z = self.__plot3DFunction(function, start, end, steps, startY, endY, stepsY)

        self.figure.add_trace(
            go.Contour(
                x = x,
                y = y,
                z = z,
                contours_coloring = 'lines',
                line_width = 2,
                contours=dict(
                    showlabels = True, # show labels on contours
                    labelfont = dict( # label font properties
                        size = 12,
                        color = 'white',
                    )
                )
            )
        )

    def render(self):
        iplot(self.figure)
