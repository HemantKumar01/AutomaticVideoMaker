# AutomaticVideoMaker
automatically creates videos on any topic you give by web scraping and image processing.
You just need to enter the topic and it will scrape information about it from wikipedia, find cc-images using google images, process images to make it look nice and can upload it on youtube;

## TODO:
- [ ] Scrape from wikipedia
- [ ] scrape cc-images from google
- [X] Process Image to create great looking drawing videos;
- [ ] upload to youtube


## Usage:

run `pip install -r requirements.txt` after cloning the repositories, after that run anime.py

you can edit arguments of createAnime function to use it according to following syntax
```python
createAnime(inputImageName, outputVideoName)
'''
@PARAM: 
inputImageName : the image path(with extension) to be processed and made into a video
outputVideoName : the name of the video to be saved (with extension)
note that if you are not having an outputVideoName with .avi extension then you have to change fourcc in createAnime function
'''
```

then run anime.py

