# Optional input files and folders
MY_URLS   = $(wildcard my_urls.txt)
MY_PICS   = $(wildcard my_pics)
MY_ADS    = $(wildcard my_ads)

# Parameters
THUMB_SIZE= 448

# Files and folders that can be created by this makefile
DOWNLOADS = highres
THUMBS    = thumbs
ADS_URLS  = ads_urls.txt.tmp
ALL_URLS  = urls.txt.tmp

# Commands used
PYTHON    = python3 -c

$(THUMBS): $(DOWNLOADS) $(MY_PICS)
	$(PYTHON) "from fastai.vision.utils import resize_images $(foreach folder,$?,; resize_images('$(folder)', dest='$@', max_size=$(THUMB_SIZE)))"

$(DOWNLOADS): $(ALL_URLS)
	$(PYTHON) "from fastai.vision.utils import download_images ; from pathlib import Path ; download_images('$@', url_file=Path('$<'))"

$(ALL_URLS): $(MY_URLS) $(ADS_URLS)
	sort $^ | uniq > $@

$(ADS_URLS): $(wildcard $(MY_ADS)/*.html)
	cat $^ | perl leboncoin_get_urls.pl > $@

clean:
	$(RM) -r $(DOWNLOADS) $(ALL_URLS) $(ADS_URLS)

fclean: clean
	$(RM) -r $(THUMBS)

.PHONY: clean fclean
