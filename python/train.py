from fastai.data.transforms import get_image_files
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize,RandomResizedCrop,aug_transforms
from fastai.vision.learner import cnn_learner
from fastai.vision.core import load_image
from fastai.metrics import error_rate
from fastai.interpret import Interpretation
from fastai.learner import load_model,Learner,load_learner
from torchvision.models import resnet34, resnet50

import csv
import tkinter
from tkinter import messagebox
import argparse
from pathlib import Path

from Feature import *
from Asker import *

parser = argparse.ArgumentParser(description="Manually classify a few relevant images")
parser.add_argument("-b", "--batch-size", type=int, help="Learning batch size", default=32)
parser.add_argument("-m", "--model", type=str, help="The output", default="model.pkl")
parser.add_argument("-c", "--csv", type=str, help="Already classified images", default="labels.csv")
parser.add_argument("-i", "--images", type=str, help="An image folder to train from", default="cache/images")
args = parser.parse_args()

labeled = []

# Import labels
try:
    with open(args.csv, mode='r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            labeled += [(row[0], row[1].split(';'))]
    print("Imported", len(labeled), "classified images")
except FileNotFoundError:
    print("Starting from scratch")

images = [fname for fname in get_image_files(args.images) if not str(fname) in [e[0] for e in labeled]]
print(len(images), "images left to categorize")

ask = Asker(iter(images), Features.list)
labeled += ask.show()
print(labeled[-5:])

# Export
with open(args.csv, mode='w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['Path','Labels'])
    for fname, labels in labeled:
        writer.writerow([fname, ';'.join(labels)])


dataloader = ImageDataLoaders.from_lists('.', [e[0] for e in labeled], [e[1] for e in labeled],
                                         item_tfms=RandomResizedCrop(224, min_scale=0.7), batch_tfms=aug_transforms(),
                                         bs=args.batch_size, valid_pct=0.25)
dataloader.show_batch()
pyplot.show()
classifier = cnn_learner(dataloader, resnet50, metrics=error_rate)
#classifier.lr_find()
#pyplot.show()
classifier.fit(4)
Interpretation.from_learner(classifier).plot_top_losses(9)
pyplot.show()
classifier.fit(4, lr=1e-4)
classifier.fit(8, lr=1e-5)
Interpretation.from_learner(classifier).plot_top_losses(9)
pyplot.show()


'''
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
    batch = images[seen:][:args.batch_size]
    ask = TrainedAsker(feature, iter(batch), classifier)
    ask.show()
    seen += args.batch_size
    labeled_images = ImageDataLoaders.from_lists('.', feature.images_paths, feature.labels,
                                                 item_tfms=RandomResizedCrop(224, min_scale=0.6), batch_tfms=aug_transforms(),
                                                 bs=args.batch_size, valid_pct=0.25)
    classifier = cnn_learner(labeled_images, resnet34, metrics=error_rate)
    classifier.fit(4)
    Interpretation.from_learner(classifier).plot_top_losses(9)
    pyplot.show()

feature.to_csv("{}.csv".format(args.feature))

classifier.fit(4, lr=1e-4)
classifier.fit(8, lr=1e-5)
Interpretation.from_learner(classifier).plot_top_losses(9)
pyplot.show()

classifier.export(args.output)
'''
