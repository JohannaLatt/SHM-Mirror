from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget


class GraphRenderer(Widget):

    def __init__(self, gui_base, **kwargs):
        # max number of points in a graph
        self.max_points = 100

        # By default, there are three graphs available
        self.graphs = [None, None, None]
        self.standard_graph_size = (.3, .15)

        self.graphs[0] = self.create_basic_graph('X', size_hint=self.standard_graph_size, pos_hint={"top": .98, "left": 1})
        self.graphs[1] = self.create_basic_graph('Y', size_hint=self.standard_graph_size, pos_hint={"top": .83, "left": 1})
        self.graphs[2] = self.create_basic_graph('Z', size_hint=self.standard_graph_size, pos_hint={"top": .68, "left": 1})

        # Each graph has one plot
        self.plots = [None, None, None]

        self.plots[0] = MeshLinePlot(color=[1, 0, 0, 1])
        self.plots[1] = MeshLinePlot(color=[0, 1, 0, 1])
        self.plots[2] = MeshLinePlot(color=[0, 0, 1, 1])

        # Link plots to graphs
        self.graphs[0].add_plot(self.plots[0])
        self.graphs[1].add_plot(self.plots[1])
        self.graphs[2].add_plot(self.plots[2])

        # Add the graphs to the root
        gui_base.root.add_widget(self.graphs[0])
        gui_base.root.add_widget(self.graphs[1])
        gui_base.root.add_widget(self.graphs[2])

    def create_basic_graph(self, y_label, size_hint, pos_hint):
        return Graph(size_hint=size_hint, pos_hint=pos_hint,
            xlabel='frames', ylabel=y_label, x_ticks_minor=3,
            x_ticks_major=50, y_ticks_major=100,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=False, y_grid=False, xmin=0, xmax=100, ymin=-200, ymax=200)

    def add_data(self, values):
        if (self.counter >= self.max_points):
            # We re-write our points list if number of values exceed 100. ie. Move each point to the left.
            for plot in self.plot:
                del(plot.points[0])
                plot.points[:] = [(i[0]-1, i[1]) for i in plot.points[:]]
            self.counter = 99

        self.plots[0].points.append((self.counter, values[0]))
        self.plots[1].points.append((self.counter, values[1]))
        self.plots[2].points.append((self.counter, values[2]))

    def show_graphs(self):
        self.graphs[0].size_hint = (0, 0)
        self.graphs[1].size_hint = (0, 0)
        self.graphs[2].size_hint = (0, 0)

    def hide_graphs(self):
        self.graphs[0].size_hint = self.standard_graph_size
        self.graphs[1].size_hint = self.standard_graph_size
        self.graphs[2].size_hint = self.standard_graph_size
        self.reset_graphs()

    def reset_graphs(self):
        self.plots[0].points = [(0, 0)]
        self.plots[1].points = [(0, 0)]
        self.plots[2].points = [(0, 0)]
