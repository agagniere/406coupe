from fastai.data.transforms import get_image_files
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.learner import cnn_learner
from fastai.metrics import error_rate
from fastai.interpret import Interpretation
from torchvision.models import resnet18

import tkinter
from tkinter import messagebox
import argparse

from Feature import *
from Asker import *

parser = argparse.ArgumentParser(description="Manually classify a few images")
parser.add_argument("-b", "--batch-size", type=int, help="Learning batch size", default=16)
parser.add_argument("-i", "--input", type=str, help="An image folder to train from", default="pics")
parser.add_argument("-o", "--output", type=str, help="Where to store the model", default="is_visible.pkl")
parser.add_argument("feature", type=str, help="The feature to train", choices=Features.list)
args = parser.parse_args()

feature = Features.from_string(args.feature)

images = get_image_files(args.input)

seen = 0
while seen == 0 or messagebox.askquestion("Keep going ?", "Do you want to classify one more batch ?") == 'yes':
    batch = images[seen:][:args.batch_size]
    ask = Asker(feature, iter(batch))
    ask.show()
    seen += args.batch_size
    # Train with current data to test
    excluded = [pic for pic in images[:seen] if not pic in feature.images_paths]
    labels = [True] * len(feature.images_paths) + [False] * len(excluded)
    print("You have reviewed {} images, classified {} and excluded {}".format(seen, len(feature.images_paths), len(excluded)))
    is_visible = ImageDataLoaders.from_lists('.', feature.images_paths + excluded, labels, item_tfms=Resize(224), bs=args.batch_size, valid_pct=0.25)
    guess_visible = cnn_learner(is_visible, resnet18, metrics=error_rate)
    guess_visible.fit(3)
    guess_visible.fit(4, lr=1e-4)
    Interpretation.from_learner(guess_visible).plot_top_losses(4)

feature.to_csv("{}_partial.csv".format(args.feature))

guess_visible.fit(4, lr=1e-4)
guess_visible.fit(8, lr=1e-5)

Interpretation.from_learner(guess_visible).plot_top_losses(4)
pyplot.show()

guess_visible.export(args.output)
