from matplotlib import pyplot
from matplotlib import image as MPL_image
from matplotlib.widgets import Button
from PIL import Image as PIL_image

from fastai.data.transforms import get_image_files
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.learner import cnn_learner
from fastai.vision.utils import resize_images, download_images
from fastai.vision.core import load_image
from fastai.metrics import error_rate
from fastai.interpret import Interpretation
from torchvision.models import resnet34

import csv
from pathlib import Path

class Feature:

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.label_from_string = {s:i for i,s in enumerate(values)}
        self.images_paths = []
        self.labels = []

    def add_image(self, path, label):
        self.images_paths += [path]
        self.labels += [label]

    def output_to_csv(self, file_name):
        print("Writing to {}".format(file_name))
        with open(file_name, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['Path', 'Label'])
            for path, label in zip(self.images_paths, self.labels):
                writer.writerow([path,label])

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

images_paths = get_image_files('thumbs')

rims = Feature("Rims", ["BBS", "Nautilus", "Hoggar", "Tacoma", "Other"])

REVIEW=33
first_batch = images_paths[:REVIEW]

ask = Asker(rims, iter(first_batch))
ask.show()

excluded = [pic for pic in first_batch if not pic in rims.images_paths]
labels = [True] * len(rims.images_paths) + [False] * len(excluded)

print("You have reviewed {} images, classified {} and excluded {}".format(len(first_batch), len(rims.images_paths), len(excluded)))

transform = Resize(224)

is_visible = ImageDataLoaders.from_lists('.', rims.images_paths + excluded, labels, item_tfms=transform, bs=16, valid_pct=0.25)
guess_visible = cnn_learner(is_visible, resnet34, metrics=error_rate)
guess_visible.fit(4)

Interpretation.from_learner(guess_visible).plot_top_losses(4)

for img in images_paths[REVIEW:REVIEW+10]:
    print(img, guess_visible.predict(img))

guess_visible.fit(4, lr=1e-4)

Interpretation.from_learner(guess_visible).plot_top_losses(4)
pyplot.show()

rest = []
for img in images_paths[REVIEW:]:
    pred, i, c = guess_visible.predict(img)
    conf = c[i]
    print(img, pred, conf)
    if int(i) == 1 or conf < 0.7:
        rest += [img]

print(rest)

ask = Asker(rims, iter(rest))
ask.show()

labeled_images = ImageDataLoaders.from_lists('.', rims.images_paths, rims.labels, item_tfms=transform, bs=16, valid_pct=0.25)
labeled_images.show_batch()
pyplot.show()

guess_rim = cnn_learner(labeled_images, resnet34, metric=error_rate)
guess_rim.fit(4)

Interpretation.from_learner(guess_rim).plot_top_losses(4)

guess_rim.fit(4, lr=1e-4)

Interpretation.from_learner(guess_rim).plot_top_losses(4)
pyplot.show()

for img in rest[30:]:
    print("{} : {}".format(img, guess_rim.predict(img)))

'''
labeled_images = ImageDataLoaders.from_csv(path='.', csv_fname='data.csv',
                                           fn_col=0, label_col=2,
                                           item_tfms=Resize(224))
labeled_images.show_batch()
pyplot.show()
'''
