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

To download the list of ads from the 15 first pages :
```bash
make leboncoin PAGES=15
```

To download and resize all known images, so that its smallest dimension is 450 :
```bash
make pics THUMB_SIZE=450
```
