# Optional input files and folders
MY_URLS   = $(wildcard my_urls.txt)
MY_PICS   = $(wildcard my_pics)
MY_ADS    = $(wildcard my_ads)

# Parameters
THUMB_SIZE ?= 900
PAGES      ?= 10
AD_LIMIT   ?= 100
AD_COUNT   ?= 100

# Files and folders that can be created by this makefile
CACHE     = cache
IMAGES    = $(CACHE)/images
ADPIC_URLS= $(CACHE)/adpics.txt
ADLISTS   = $(CACHE)/pages
ADLIST    = $(CACHE)/ads.txt
ADS       = ads
ADS_CSV   = ads.csv

# Commands used
PYTHON    = python3

# ===== Colors =====
EOC   := "\033[0m"
BLACK := "\033[1;30m"
RED   := "\033[1;31m"
GREEN := "\033[1;32m"
YELLOW:= "\033[1;33m"
PURPLE:= "\033[1;35m"
CYAN  := "\033[1;36m"
WHITE := "\033[1;37m"
# ==================

PROVIDED=$(wildcard $(MY_PICS)/*.jpg $(MY_PICS)/*.png)
MOVED=$(PROVIDED:$(MY_PICS)/%=$(IMAGES)/%)

usage:
	@echo "make pics to download and resize all pictures"
	@echo "make leboncoin to download most recent ads list"

leboncoin: | $(ADLISTS)
	@echo $(CYAN)"Dowloading the $(PAGES) first pages"$(EOC)
	seq $(PAGES) | parallel --bar 'wget "https://www.leboncoin.fr/recherche/?category=2&brand=Peugeot&model=406&vehicle_type=coupe&page={}" --no-clobber -qO $|/{}.html' || true

pics: $(IMAGES) $(MOVED)

resize: $(IMAGES)
	imgp --mute --res $(THUMB_SIZE)x$(THUMB_SIZE) --overwrite $<

adcsv: $(ADS_CSV)

status: $(MY_ADS) $(MY_PICS) $(ADLIST) $(ADPIC_URLS)
	@cat $(ADLIST) | cut -d'/' -f3 > tmp.txt
	@echo -n $(WHITE)
	@printf "Data set : %i images (%s)\n" $$(ls $(IMAGES) | wc -l) $$(du -h $(IMAGES) | cut -f1)
	@printf "You provided %i images, %i urls and %i ads\n" $$(ls $(MY_PICS) | wc -l) $$(cat $(MY_URLS) | wc -l) $$(ls $(MY_ADS) | wc -l)
	@printf "Downloaded %i out of %i known ads from leboncoin\n" $$(ls $(ADS) | wc -l) $$(ls $(ADS) | cat - tmp.txt | sort --unique | wc -l)
	@printf "Ads (including yours) provide %i urls\n" $$(cat $(ADPIC_URLS) | wc -l)
	@echo -n $(EOC)
	@$(RM) tmp.txt

# -------------------------------------------

$(MOVED): $(IMAGES)/%: $(MY_PICS)/%
	cp $< $@

$(IMAGES): $(MY_URLS) $(ADPIC_URLS)
	cat $^ | parallel --bar wget {} --quiet --no-clobber -P $@ || true

$(ADS_CSV): $(wildcard $(MY_ADS)/*.html $(ADS)/*.htm)
	( ls $? | parallel --bar perl "perl/leboncoin_ad_parser.pl < {} 2>/dev/null" ) >> $@
	sort --unique $@ -o $@

$(ADPIC_URLS): $(wildcard $(MY_ADS)/*.html $(ADS)/*.htm) | $(CACHE)
	cat $? | perl perl/leboncoin_get_urls.pl >> $@
	sort --unique $@ -o $@

.PHONY: ads
ads: $(ADLIST)
	@echo $(CYAN)$(shell cat $< | wc -l ) "ads to download"$(EOC)
	cat $< | head -$(AD_COUNT) | tail -$(AD_LIMIT) | parallel --bar wget "https://www.leboncoin.fr{} --no-clobber -qP $(ADS)"

$(ADLIST): $(wildcard $(ADLISTS)/*.html)
	grep --no-filename --only-matching --perl-regexp '/voitures/\d+?.htm' $? >> $@
	sort --unique $@ -o $@

$(CACHE) $(ADLISTS) $(MY_PICS) $(MY_ADS):
	mkdir -p $@

clean:
	$(RM) -r $(ADLIST) $(ADPIC_URLS)

fclean: clean
	$(RM) -r $(IMAGES) $(ADLISTS)

.PHONY: clean fclean leboncoin pics adcsv
