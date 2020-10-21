from fastai.data.transforms import get_image_files
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize,RandomResizedCrop,aug_transforms
from fastai.vision.learner import cnn_learner
from fastai.vision.core import load_image
from fastai.metrics import error_rate
from fastai.interpret import Interpretation
from fastai.learner import load_model,Learner,load_learner
from torchvision.models import resnet34

import tkinter
from tkinter import messagebox
import argparse
from pathlib import Path

from Feature import *
from Asker import *

parser = argparse.ArgumentParser(description="Manually classify a few relevant images")
parser.add_argument("-b", "--batch-size", type=int, help="Learning batch size", default=32)
parser.add_argument("-m", "--model", type=argparse.FileType('r'), help="The boolean model to exclude images where the feature is not visible")
parser.add_argument("-c", "--csv", type=argparse.FileType('r'), help="Already classified images")
parser.add_argument("-i", "--input", type=str, help="An image folder to train from", default="pics")
parser.add_argument("-o", "--output", type=str, help="Where to store the model", default="export.pkl")
parser.add_argument("feature", type=str, help="The feature to train", choices=Features.list)
args = parser.parse_args()

is_visible = load_learner(args.model.name, cpu=False) if args.model else None
feature = Features.from_string(args.feature)

if args.csv:
    feature.from_opened_csv(args.csv)
    print("Using the {} labeled images from CSV".format(len(feature)))

# Keep only images we did not already classified, and that the boolean model thinks are relevant
images = [img for img in get_image_files(args.input) if not str(img) in feature.images_paths and (is_visible == None or is_visible.predict(img)[2][1] > 0.7)]

print("Left with", len(images), "images")

seen = 0
if len(feature) < args.batch_size:
    batch = images[:args.batch_size]
    ask = Asker(feature, iter(batch))
    ask.show()
    seen += args.batch_size
    feature.to_csv("{}.csv".format(args.feature))

labeled_images = ImageDataLoaders.from_lists('.', feature.images_paths, feature.labels,
                                             item_tfms=RandomResizedCrop(224, min_scale=0.6), batch_tfms=aug_transforms(),
                                             bs=args.batch_size, valid_pct=0.25)
classifier = cnn_learner(labeled_images, resnet34, metrics=error_rate)
classifier.fit(4)
while seen == 0 or messagebox.askquestion("Keep going ?", "Do you want to classify one more batch ?") == 'yes':
    batch = images[:args.batch_size]
    ask = TrainedAsker(feature, iter(batch), classifier)
    ask.show()
    seen += args.batch_size
    labeled_images = ImageDataLoaders.from_lists('.', feature.images_paths, feature.labels,
                                                 item_tfms=RandomResizedCrop(224, min_scale=0.6), batch_tfms=aug_transforms(),
                                                 bs=args.batch_size, valid_pct=0.25)
    classifier = cnn_learner(labeled_images, resnet34, metrics=error_rate)
    classifier.fit(4)
    Interpretation.from_learner(guess_visible).plot_top_losses(9)
    pyplot.show()

feature.to_csv("{}.csv".format(args.feature))

classifier.fit(4, lr=1e-4)
classifier.fit(8, lr=1e-5)
Interpretation.from_learner(guess_visible).plot_top_losses(9)
pyplot.show()

classifier.export(args.output)
