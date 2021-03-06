Welcome to autocutpy!
===================


If you have many old pictures and a scanner, you can scan multiple photos at once, and use this program to cut and trim them into single image files.

![](https://github.com/MagicManLearnProgramming/autocutpy-project/raw/master/docs/illustrate_05.JPG)

***To be：***

![](https://github.com/MagicManLearnProgramming/autocutpy-project/raw/master/docs/illustrate_04.JPG)

----------


Super simple to use
-------------

> \>>> python autocutpy.py

Will start a server and launch a browser that points to that web server. 
![](https://github.com/MagicManLearnProgramming/autocutpy-project/raw/master/docs/illustrate_00.JPG)

If the browser does not start automatically, you can open the browser by yourself and enter the URL:   **localhost:9527/webui.py**

![](https://github.com/MagicManLearnProgramming/autocutpy-project/raw/master/docs/illustrate_02.JPG)
Select you file(s) and submit.

![](https://github.com/MagicManLearnProgramming/autocutpy-project/raw/master/docs/illustrate_03.JPG)

![](https://github.com/MagicManLearnProgramming/autocutpy-project/raw/master/docs/illustrate_04.JPG)

**You can also run on the command line:**
> \>>> python autocutpy.py -f c:\scan\myimg.jpg
>Description： -f take a image file name
>
> \>>> python autocutpy.py -p c:\scan -g 5
>Description：
> -f take a path, every image file in that path will be dealt. 
> -g The graininess of trimmer. range is (0, 5), the bigger the graininess , the larger the trimmed photos (Maybe). It's not very useful. The default value is 5 and work well.
> 
> \>>> python autocutpy.py -h
>  You can also use -h to get more help

----------


Requirement
-------------
Python 2.7
OpenCV-python
numpy
PIL

----------


Installation
-------------
You can download the entire directory  *"autocutpy "* and run from that directory.
There will be a **"pip install"** version soon.