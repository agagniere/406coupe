from matplotlib import pyplot
from matplotlib.widgets import Button
from PIL import Image as PIL_image

class Asker:

    def __init__(self, feature, image_iterator):
        self.feature = feature
        self.iterator = image_iterator
        self.current_image = next(self.iterator)
        self.buttons = []

    def add(self, label):
        def callback(event):
            self.feature.add_image(self.current_image, label)
            self.next(event)
        return callback

    def next(self, event):
        try:
            self.current_image = next(self.iterator)
            self.draw()
        except StopIteration:
            pyplot.close()

    def draw(self):
        self.img_plt.clear()
        self.img_plt.axis('off')
        self.img_plt.imshow(PIL_image.open(self.current_image))
        pyplot.draw()

    def show(self):
        self.figure, self.img_plt = pyplot.subplots()
        pyplot.subplots_adjust(left=0.3)
        self.figure.suptitle("What {} can you see ?".format(self.feature.name))
        self.add_buttons()
        self.draw()
        pyplot.show()

    def add_buttons(self):
        button_count = len(self.feature.values) + 1
        outer_margin = 0.1
        inter_margin = 0.01
        button_width = (1 - 2 * outer_margin - (button_count - 1) * inter_margin) / button_count
        button_slot  = (1 - 2 * outer_margin) / button_count
        for i, value in enumerate(self.feature.values):
            self.buttons += [Button(pyplot.axes([0.05, outer_margin + button_slot * (i + 1), 0.2, button_width]), value, color=(0.3,0.5,0.8))]
            self.buttons[-1].on_clicked(self.add(value))
        self.buttons += [Button(pyplot.axes([0.05, outer_margin, 0.2, button_width]), 'None', color=(0.8,0.2,0.2))]
        self.buttons[-1].on_clicked(self.next)
