from matplotlib import pyplot
from matplotlib import image as MPL_image
from matplotlib.widgets import Button
from PIL import Image as PIL_image
from fastai.data.transforms import get_image_files
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.learner import cnn_learner
from fastai.metrics import error_rate
from torchvision.models import resnet34
import csv

class Feature:
    images_paths = []
    labels = []
    name = ""
    values = []
    label_from_string = {}

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.label_from_string = {str:i for i,str in enumerate(values)}

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

    def __init__(self, feature, image_iterator, goal_n=30):
        self.feature = feature
        self.iterator = image_iterator
        self.current_image = next(self.iterator)
        self.goal_n = goal_n
        self.buttons = []

    def add(self, label):
        def callback(event):
            self.feature.add_image(self.current_image, label)
            self.next(event)
        return callback

    def next(self, event):
        try:
            self.current_image = next(self.iterator)
            if len(self.feature.images_paths) > self.goal_n:
                pyplot.close()
            else:
                self.draw()
        except StopIteration:
            pyplot.close()

    def draw(self):
        img = PIL_image.open(self.current_image)
        img.thumbnail((500, 500), PIL_image.ANTIALIAS)
        self.img_plt.imshow(img)
        pyplot.draw()

    def show(self):
        self.figure, self.img_plt = pyplot.subplots()
        pyplot.axis('off')
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

images_paths = get_image_files('.')

rims = Feature("Rims", ["BBS", "Nautilus", "Hoggar", "Tacoma", "Other"])
tst = Asker(rims, iter(images_paths), goal_n=9)
tst.show()

rims.output_to_csv("rims.csv")
if (len(rims.images_paths) > 8):
    labeled_images = ImageDataLoaders.from_lists('.', rims.images_paths, rims.labels, item_tfms=Resize(224), bs=8)
    labeled_images.show_batch()
    pyplot.show()

    learn = cnn_learner(labeled_images, resnet34, metrics=error_rate)
    learn.fit(3)

'''
labeled_images = ImageDataLoaders.from_csv(path='.', csv_fname='data.csv',
                                           fn_col=0, label_col=2,
                                           item_tfms=Resize(224))
labeled_images.show_batch()
pyplot.show()
'''
