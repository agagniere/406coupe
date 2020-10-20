# Optional input files and folders
MY_URLS   = $(wildcard my_urls.txt)
MY_PICS   = $(wildcard my_pics)
MY_ADS    = $(wildcard my_ads)

# Parameters
THUMB_SIZE= 448

# Files and folders that can be created by this makefile
THUMBS    = pics
CACHE     = cache
DOWNLOADS = $(CACHE)/highres
ADS_URLS  = $(CACHE)/ads_urls.txt
ALL_URLS  = $(CACHE)/urls.txt
MODELS    = models

# WIP
FEATURES  = rims front_bumper exterior interior
#CLASSIFIERS= $(FEATURES:%=$(MODELS)/%.pth)
#VISIBLE   = $(FEATURES:%=$(MODELS)/%_visible.pth)
#LABELS    = $(FEATURES:%=%.csv)
#PARTIALS  = $(FEATURES:%=%_partial.csv)

# Commands used
PYTHON    = python3

usage:
	@echo "make pics to download and resize all pictures"
	@echo "make rims to train the rims model"

.PHONY: $(FEATURES)
$(FEATURES): % : $(MODELS)/%.pth

%.csv: $(MODELS)/%.pth
	@echo Classify images for : $*

%.pth: %_visible.pth
	@echo Train model for : $*

# Manually classify a first batch of images
%_visible.pth: $(THUMBS)
	$(PYTHON) python/first_batch.py --input $< $*

$(THUMBS): $(DOWNLOADS) $(MY_PICS)
	$(PYTHON) -c "from fastai.vision.utils import resize_images$(foreach folder,$?,; resize_images('$(folder)', dest='$@', max_size=$(THUMB_SIZE)))"

$(DOWNLOADS): $(ALL_URLS)
	$(PYTHON) -c "from fastai.vision.utils import download_images ; from pathlib import Path ; download_images('$@', url_file=Path('$<'))"

$(ALL_URLS): $(MY_URLS) $(ADS_URLS)
	sort $^ | uniq > $@

$(ADS_URLS): $(wildcard $(MY_ADS)/*.html) | $(CACHE)
	cat $^ | perl perl/leboncoin_get_urls.pl > $@

$(CACHE):
	mkdir $@

clean:
	$(RM) -r $(CACHE)

fclean: clean
	$(RM) -r $(THUMBS)

.PHONY: clean fclean
