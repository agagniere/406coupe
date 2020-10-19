DOWNLOADS = highres
THUMBS    = thumbs
URLS      = urls.txt

PYTHON = python3 -c

SIZE_THUMB = 448
SIZE_IN_NN = 224

$(THUMBS): $(DOWNLOADS)
	$(PYTHON) "from fastai.vision.utils import resize_images ; resize_images('$<', dest='$@', max_size=$(SIZE_THUMB))"

$(DOWNLOADS): $(URLS)
	$(PYTHON) "from fastai.vision.utils import download_images ; from pathlib import Path ; download_images('$@', url_file=Path('$<'))"
