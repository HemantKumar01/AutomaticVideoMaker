# AutomaticVideoMaker
Creates beautiful drawing animation video from images.

# Demo

### Input Image
<img src="https://user-images.githubusercontent.com/71439585/205424913-47b4926c-c26f-4d89-895d-12287d7004d4.jpg" alt="harry-potter" width=500px>

### Output Video
### Play

https://user-images.githubusercontent.com/71439585/205424924-4d193c79-914b-41fb-82dc-3a999df44018.mp4




## Usage:

run `pip install -r requirements.txt` after cloning the repositories, after that run anime.py

you can edit arguments of createAnime function to use it according to following syntax (see last lines of `anime.py`)
```python
createAnime(inputImageName, outputVideoName)
'''
@PARAM: 
inputImageName : the image path(with extension) to be processed and made into a video
outputVideoName : the name of the video to be saved (with extension)
# note that if you are not having an outputVideoName with .avi extension then you have to change fourcc in createAnime function
backgroundColor="background_image_path" or BGR_color_tuple,
foregroundColor=bgr_color_tuple,
'''
```

then run anime.py

