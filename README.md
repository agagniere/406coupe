# 406 coupe

My first data science project:
* Collecting pictures of 406 coupe
* Labelling them (year, fuel, price, options, etc)
* Training a neural network
* ?????
* Profit !

## Training

### Data collection

* If you have pictures on your computer, put them in a folder called `my_pics`
* Urls of images can be put in a file called `my_urls.txt`
* Leboncoin ads you want to keep can be placed in a folder named `my_ads`

To download ads from the 15 first pages :
```bash
make leboncoin PAGES=15
make ads
```

To download and resize all known images, so that it fits in a 450x450 square :
```bash
make pics
make resize THUMB_SIZE=450
```

To check dataset status :
```bash
make status
```
```
Data set : 2504 images (143M)
You provided 45 images, 99 urls and 120 ads
Downloaded 688 out of 688 known ads from leboncoin
Ads (including yours) provide 2367 urls
```
