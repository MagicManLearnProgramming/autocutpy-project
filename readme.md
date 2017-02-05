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

↑Will launch a window to help you to do the cut and trim job.  
    
    
![](https://github.com/MagicManLearnProgramming/autocutpy-project/blob/master/docs/illustrate_1%20(1).jpg?raw=true)
![](https://github.com/MagicManLearnProgramming/autocutpy-project/blob/master/docs/illustrate_1%20(2).jpg?raw=true)

↑Select the image files that you want to cut and trim.  
  
  
![](https://github.com/MagicManLearnProgramming/autocutpy-project/blob/master/docs/illustrate_1%20(3).jpg?raw=true)
![](https://github.com/MagicManLearnProgramming/autocutpy-project/blob/master/docs/illustrate_1%20(4).jpg?raw=true)

↑Select a directory to save the trimmed photos.
  
  
![](https://github.com/MagicManLearnProgramming/autocutpy-project/blob/master/docs/illustrate_1%20(5).jpg?raw=true)
![](https://github.com/MagicManLearnProgramming/autocutpy-project/blob/master/docs/illustrate_1%20(6).jpg?raw=true)
   
↑Wait until the progress bar is full.   
   
   
![](https://github.com/MagicManLearnProgramming/autocutpy-project/blob/master/docs/illustrate_1%20(7).jpg?raw=true)
↑You get it.


**You can also start a server and launch a browser that points to that web server:**
> \>>> python autocutpy.py -w  
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
