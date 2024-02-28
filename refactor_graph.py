import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class InteractiveGraphEditor:
    def __init__(self):
        self.graph = nx.Graph()
        self.fig, self.ax = plt.subplots()
        self.pos = {}
        self.node_colors = {}

        self.ax.set_title('Interactive Graph Editor')
        self.ax.set_axis_off()

        self.ax_add_node_button = plt.axes([0.01, 0.9, 0.1, 0.05])
        self.add_node_button = Button(self.ax_add_node_button, 'Add Node')
        self.add_node_button.on_clicked(self.add_node)

        self.ax_delete_node_button = plt.axes([0.01, 0.85, 0.1, 0.05])
        self.delete_node_button = Button(self.ax_delete_node_button, 'Delete Node')
        self.delete_node_button.on_clicked(self.delete_node)

        self.ax_draw_button = plt.axes([0.01, 0.8, 0.1, 0.05])
        self.draw_button = Button(self.ax_draw_button, 'Draw Graph')
        self.draw_button.on_clicked(self.draw_graph)

        self.ax_clear_button = plt.axes([0.01, 0.75, 0.1, 0.05])
        self.clear_button = Button(self.ax_clear_button, 'Clear Graph')
        self.clear_button.on_clicked(self.clear_graph)

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def add_node(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            node_name = f'Node_{len(self.graph.nodes)+1}'
            self.graph.add_node(node_name)
            self.pos[node_name] = (x, y)
            self.node_colors[node_name] = 'blue'
            self.draw_graph(event)

    def delete_node(self, event):
        node_to_remove = plt.ginput(1, timeout=0)
        if node_to_remove:
            node_to_remove = self.get_clicked_node(node_to_remove[0])
            if node_to_remove is not None:
                self.graph.remove_node(node_to_remove)
                self.draw_graph(event)

    def draw_graph(self, event):
        self.ax.clear()
        nx.draw(self.graph, pos=self.pos, ax=self.ax, with_labels=True,
                node_color=[self.node_colors[node] for node in self.graph.nodes()])
        plt.draw()

    def clear_graph(self, event):
        self.graph.clear()
        self.pos.clear()
        self.node_colors.clear()
        self.ax.clear()
        plt.draw()

    def on_click(self, event):
        if event.inaxes == self.ax:
            node_clicked = self.get_clicked_node((event.xdata, event.ydata))
            if node_clicked is not None:
                self.move_node(node_clicked, event)

    def move_node(self, node, event):
        self.pos[node] = (event.xdata, event.ydata)
        self.draw_graph(event)

    def get_clicked_node(self, point):
        for node, pos in self.pos.items():
            if (pos[0]-point[0])**2 + (pos[1]-point[1])**2 < 0.01:  # Adjust this threshold as needed
                return node
        return None

if __name__ == '__main__':
    editor = InteractiveGraphEditor()
    plt.show()
