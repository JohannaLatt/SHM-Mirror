from kivy.garden.graph import Graph, SmoothLinePlot
from kivy.uix.widget import Widget


class GraphRenderer(Widget):

    def __init__(self, gui_base, **kwargs):
        # max number of points in a graph
        self.counter = 0
        self.max_points = 100

        # By default, there are three graphs available
        self.graphs = [None, None, None]
        self.standard_graph_size = (.3, .15)
        self.standard_graph_size_labelled = (.312, .2105)

        self.graphs[0] = self.create_basic_graph('X', 0, 600, size_hint=self.standard_graph_size, pos_hint={"top": .98, "left": 1}, x_grid_label=False, xlabel='')
        self.graphs[1] = self.create_basic_graph('Y', -600, 200, size_hint=self.standard_graph_size, pos_hint={"top": .845, "left": 1}, x_grid_label=False, xlabel='')
        self.graphs[2] = self.create_basic_graph('Z', 1500, 2500, size_hint=self.standard_graph_size_labelled, pos_hint={"top": .71, "left": 1})

        # Each graph has one plot
        self.plots = [None, None, None]

        self.plots[0] = SmoothLinePlot(color=[1, 0, 0, 1])
        self.plots[1] = SmoothLinePlot(color=[0, 1, 0, 1])
        self.plots[2] = SmoothLinePlot(color=[0.6, 1, 1, 1])

        # Link plots to graphs
        self.graphs[0].add_plot(self.plots[0])
        self.graphs[1].add_plot(self.plots[1])
        self.graphs[2].add_plot(self.plots[2])

        # Add the graphs to the root
        gui_base.root.add_widget(self.graphs[0])
        gui_base.root.add_widget(self.graphs[1])
        gui_base.root.add_widget(self.graphs[2])
        self.root = gui_base.root

        self.hide_graphs()
        self.ready = True

    def create_basic_graph(self, y_label, y_min, y_max, size_hint, pos_hint, x_grid_label=True, xlabel='frames'):
        return Graph(size_hint=size_hint, pos_hint=pos_hint,
            xlabel=xlabel, ylabel=y_label, x_ticks_minor=3,
            x_ticks_major=50, y_ticks_major=100,
            y_grid_label=True, x_grid_label=x_grid_label, padding=5,
            x_grid=False, y_grid=False, xmin=0, xmax=100, ymin=y_min, ymax=y_max)

    def add_data(self, values):
        if not self.ready:
            return

        if len(values) is 0 and not self.hidden:
            self.hide_graphs()
        else:
            if len(values) is not 3:
                return

            if self.hidden:
                self.show_graphs()

            # Only keep a total of 100 points
            if (self.counter >= self.max_points):
                for plot in self.plots:
                    plot.points.pop(0)
                    plot.points = map(lambda point: (point[0] - 1, point[1]), plot.points)
                self.counter = 99

            # print(self.plots[0].points)
            self.extend_plot_range_if_needed(values)
            self.plots[0].points.append((self.counter, values[0]))
            self.plots[1].points.append((self.counter, values[1]))
            self.plots[2].points.append((self.counter, values[2]))
            self.counter += 1

    def show_graphs(self):
        self.hidden = False
        for graphs in self.graphs:
            self.root.add_widget(graphs)

    def hide_graphs(self):
        self.hidden = True
        for graphs in self.graphs:
            self.root.remove_widget(graphs)
        self.reset_graphs()

    def reset_graphs(self):
        self.plots[0].points = [(0, 0)]
        self.plots[1].points = [(0, 0)]
        self.plots[2].points = [(0, 0)]
        self.counter = 0

    def extend_plot_range_if_needed(self, values):
        for i in range(0, len(self.graphs)):
            graph = self.graphs[i]
            if graph.ymin > values[i]:
                graph.ymin = values[i] - 20
            if graph.ymax < values[i]:
                graph.ymax = values[i] + 20
