from fastai.data.transforms import get_image_files
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize, aug_transforms
from fastai.vision.learner import cnn_learner
from fastai.metrics import error_rate
from fastai.interpret import Interpretation, ClassificationInterpretation
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
parser.add_argument("-c", "--csv", type=str, help="Where to store the labels", default="first_batches.csv")
parser.add_argument("feature", type=str, help="The feature to train", choices=Features.list)
args = parser.parse_args()

feature = Features.from_string(args.feature)
images = get_image_files(args.input)

seen = 0
while seen == 0 or messagebox.askquestion("Keep going ?", "Do you want to classify one more batch ?") == 'yes':
    batch = images[:args.batch_size]
    ask = Asker(feature, iter(batch))
    ask.show()
    seen += args.batch_size
    images = images[args.batch_size:]
    print("You have reviewed {} images, classified {} and marked {} as irrelevant".format(seen, len(feature), len(feature.not_visible)))
    is_visible = ImageDataLoaders.from_lists('.', *feature.boolean_training(), item_tfms=Resize(224), batch_tfms=aug_transforms(), bs=args.batch_size, valid_pct=0.25)
    guess_visible = cnn_learner(is_visible, resnet18, metrics=error_rate)
    guess_visible.fit(4)
    guess_visible.fit(4, lr=1e-4)
    Interpretation.from_learner(guess_visible).plot_top_losses(4)
    pyplot.show()

feature.to_csv(args.csv)

guess_visible.fit(4, lr=1e-4)
guess_visible.fit(8, lr=1e-5)

guess_visible.export(args.output)

interp = ClassificationInterpretation.from_learner(guess_visible)
interp.plot_top_losses(4)
interp.plot_confusion_matrix()
pyplot.show()

guess_visible.unfreeze()
guess_visible.fit(4, lr=1e-4)
guess_visible.fit(8, lr=1e-5)
guess_visible.fit(16, lr=1e-6)

guess_visible.export('thawed_' + args.output)

interp = ClassificationInterpretation.from_learner(guess_visible)
interp.plot_top_losses(4)
interp.plot_confusion_matrix()
pyplot.show()
