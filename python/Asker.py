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

    def not_visible(self, event):
        self.feature.add_not_visible(self.current_image)
        self.next(event)

    def next(self, event):
        try:
            self.current_image = next(self.iterator)
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
        pyplot.subplots_adjust(left=0.5)
        self.figure.suptitle("What {} can you see ?".format(self.feature.name))
        self.add_buttons()
        self.draw()
        pyplot.show()

    def add_buttons(self):
        # Build the buttons panel : [x, y1, y2]
        total_size   = [0.5, 1, 1]
        button_count = [2, len(self.feature.values), 2]
        outer_margin = [0.05, 0.1, 0.1]
        inter_margin = [0.01, 0.01, 0.01]
        size = [(total - 2 * outer - (count - 1) * inter) / count for count, outer, inter, total in zip(button_count, outer_margin, inter_margin, total_size)]
        slots = [[outer + i * (button + inter) for i in range(count)] for count, outer, inter, button in zip(button_count, outer_margin, inter_margin, size)]
        for slot, value in zip(slots[1], self.feature.values):
            self.buttons += [Button(pyplot.axes([slot[0][0], slot] + size[:2]), value, color=(0.3, 0.4, 0.7))]
            self.buttons[-1].on_clicked(self.add(value))
        self.buttons += [Button(pyplot.axes([slot[0][1], slot[2][1]] + size[::2]), 'Not visible', color=(0.6, 0.3, 0.3))]
        self.buttons[-1].on_clicked(self.not_visible)
        self.buttons += [Button(pyplot.axes([slot[0][1], slot[2][0]] + size[::2]), 'Discard', color=(0.8, 0.2, 0.2))]
        self.buttons[-1].on_clicked(self.next)

class TrainedAsker(Asker):

    def __init__(self, feature, image_iterator, model):
        super().__init__(feature, image_iterator)
        self.model = model

    def draw(self):
        super().draw()
        _, pred_index, coefs = self.model.predict(self.current_image)
        for i, confidence in enumerate(coefs):
            c = float(confidence)
            self.buttons[i].color = (0.1, c, 0.5) if i == pred_index else (0.5, c, c)
