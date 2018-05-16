# Module Rectangle Manager that is used by GUI


from matplotlib.patches import Rectangle

class RectCreator(object):

    def __init__(self, axis, image):
        self.axis = axis
        self.image = image
        self.rect = None
        self.colored = None
        self.off_center = None

    def make_rectangle(self, rect_id, colored='g'):
        self.rect = Rectangle((self.image.shape[0] / 2 - self.image.shape[1] / 8, self.image.shape[0] / 2 + self.image.shape[1] / 8),
                          self.image.shape[0] / 4, self.image.shape[1] / 4, color=colored, linewidth=3, fill=False)
        rect_artist=self.axis.add_artist(self.rect)
        rect_artist.set_gid(rect_id)
        self.axis.figure.canvas.draw()
        return Rectangle.get_gid(self.rect)

class RectEditor(object):

    def __init__(self, fig, axis, rectangle):
        self.fig = fig
        self.axis = axis
        self.rectangle = rectangle
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.done = 0
        self.cidpress = None
        self.cidrelease = None
        self.cidclose = None

    def connect(self):
        self.cidpress = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidclose = self.fig.canvas.mpl_connect('close_event', self.window_closed)

    def on_press(self, event):
        if event.inaxes == self.axis:
            self.done = 1
            self.x0, self.y0 = event.xdata, event.ydata
        else:
            return

    def on_release(self, event):
        if event.inaxes == self.axis:
            self.x1, self.y1 = event.xdata, event.ydata
            self.rectangle.remove()
            self.rectangle = Rectangle((min(self.x0, self.x1), min(self.y0, self.y1)),
                                       abs(self.x1-self.x0), abs(self.y1-self.y0), color='g', linewidth=3, fill=False)
            self.axis.add_artist(self.rectangle)
            self.fig.canvas.draw()
        else:
            return

    def window_closed(self, event):
        if event.canvas.figure == self.fig:
            self.fig.canvas.mpl_disconnect(self.cidpress)
            self.fig.canvas.mpl_disconnect(self.cidrelease)
            self.fig.canvas.mpl_disconnect(self.cidclose)
            self.fig = None

    def remove_rectangle(self):
        self.rectangle.remove()
        self.fig.canvas.draw()

    def create_rectangle(self, rec):
        self.rectangle = Rectangle(rec.get_xy(), rec.get_width(), rec.get_height(), color='g', linewidth=3, fill=False)
        self.axis.add_artist(self.rectangle)
        self.fig.canvas.draw()