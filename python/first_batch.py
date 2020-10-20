from fastai.data.transforms import get_image_files
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.learner import cnn_learner
from fastai.vision.core import load_image
from fastai.metrics import error_rate
from fastai.interpret import Interpretation
from torchvision.models import resnet18

import argparse

from Feature import *
from Asker import *

parser = argparse.ArgumentParser(description="Manually classify a few images")
parser.add_argument("-i", "--input", type=str, help="An image folder to train from", default="pics")
parser.add_argument("-n", type=int, help="Number of images to classify", default=32)
parser.add_argument("-b", "--batch-size", type=int, help="Learning batch size", default=16)
parser.add_argument("feature", type=str, help="The feature to train", choices=Features.list)
args = parser.parse_args()

feature = Features.from_string(args.feature)
images_paths = get_image_files(args.input)[:args.n]

ask = Asker(feature, iter(images_paths))
ask.show()

feature.to_csv("{}_partial.csv".format(args.feature))

excluded = [pic for pic in images_paths if not pic in feature.images_paths]
labels = [True] * len(feature.images_paths) + [False] * len(excluded)

print("You have reviewed {} images, classified {} and excluded {}".format(len(images_paths), len(feature.images_paths), len(excluded)))

is_visible = ImageDataLoaders.from_lists('.', feature.images_paths + excluded, labels, item_tfms=Resize(224), bs=args.batch_size, valid_pct=0.25)
is_visible.show_batch()
pyplot.show()

guess_visible = cnn_learner(is_visible, resnet18, metrics=error_rate)
print("LR:", guess_visible.lr)
guess_visible.fit(1)
guess_visible.fit(3, lr=1e-4)

Interpretation.from_learner(guess_visible).plot_top_losses(4)
guess_visible.fit(4, lr=1e-5)
Interpretation.from_learner(guess_visible).plot_top_losses(4)
pyplot.show()

guess_visible.save('{}_visible'.format(args.feature))
