from matplotlib import pyplot
from matplotlib.widgets import Button
from PIL import Image as PIL_image

class Asker:

    def __init__(self, image_iterator, features):
        self.iterator = image_iterator
        self.current_image = next(self.iterator)
        self.features = features
        self.buttons = []
        self.selected = []
        self.labeled_images = []

    def reset(self):
        self.selected = []
        for button in self.buttons[:-1]:
            button.color = button.hovercolor

    def next(self, event):
        self.labeled_images += [(self.current_image, self.selected)]
        try:
            self.current_image = next(self.iterator)
            self.reset()
            self.draw()
        except StopIteration:
            pyplot.close()

    def draw(self):
        self.img_plt.clear()
        self.img_plt.axis('off')
        self.img_plt.imshow(PIL_image.open(self.current_image), animated=True)
        pyplot.draw()

    def show(self):
        self.figure, self.img_plt = pyplot.subplots()
        pyplot.subplots_adjust(left=0.5, bottom=0.1, top=0.95)
        self.figure.suptitle("What can you see ?")
        self.add_buttons()
        self.draw()
        pyplot.show()
        return self.labeled_images

    def select(self, label, button):
        def callback(event):
            print(label)
            self.selected += [label]
            button.color = (0.1, 0.8, 0.1)
        return callback

    def add_buttons(self):
        # Build the buttons panel : [x, y1, y2]
        N = len(self.features)
        total_size   = [0.5] + [1.] * N
        button_count = [N] + [len(feature) for feature in self.features]
        outer_margin = [0.01] * (N + 1)
        inter_margin = [0.005] * (N + 1)
        sizes = [(total - 2 * outer - (count - 1) * inter) / count for count, outer, inter, total in zip(button_count, outer_margin, inter_margin, total_size)]
        slots = [[outer + i * (button + inter) for i in range(count)] for count, outer, inter, button in zip(button_count, outer_margin, inter_margin, sizes)]
        width = sizes[0]
        colors = [(0.4, 0.4, 0.7), (0.4, 0.7, 0.4), (0.4, 0.7, 0.7), (0.6, 0.4, 0.7), (0.6, 0.7, 0.4)]
        for feature, height, x, slot, color in zip(self.features, sizes[1:], slots[0], slots[1:], colors):
            for label, y in zip(feature.values, slot):
                self.buttons += [Button(pyplot.axes([x, y, width, height]), label, color=color, hovercolor=color)]
                self.buttons[-1].on_clicked(self.select(label, self.buttons[-1]))
        self.buttons += [Button(pyplot.axes([0.5, 0.005, 0.5, 0.09]), 'Next', color=(0.9, 1, 0.9))]
        self.buttons[-1].on_clicked(self.next)
