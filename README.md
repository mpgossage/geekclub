geekclub: Scratch style programming in Python
=============================================

An attempt to make Scratch style programming in Python possible -- in
response to the question: "What shall I try after Scratch". Inspired by MIT Scratch: http://scratch.mit.edu/

I'm aiming for a suite of libraries that:

* Makes it easy to get visual or audio effects
* Gives immediate results (like Scratch does), type some commands, press run, see results
* Runs easily on the Raspberry Pi
* Runs easily on Windows PCs in schools, to support my STEM Ambassador work
* Has depth with plenty to explore.

Screen shots
------------

![boulder screen shot](/images/boulder.png)

![pong screen shot](/images/pong.png)

![fractal trees screen shot](/images/fractal-trees.png)


Prerequesites
-------------

* Python 3
* A working tkinter library

Get the code
------------

You can use `git` or download a [zip file of the code](https://github.com/ericclack/geekclub/archive/master.zip):

    git clone https://github.com/ericclack/geekclub.git


Examples
--------

Start up `idle3` and create a new file, save it to the directory `my_work`, then add the following code...

```
from geekclub_packages import *
  
create_canvas()
sprite = ImageSprite('my_images/face.gif')
sprite.pen_down()

def move_sprite(event):
    sprite.move(10,10)

when_key_pressed('<space>', move_sprite)
mainloop()
```

Documentation
-------------

Check out the examples directory. You should be able to run the code straight
from that directory.

Have a look at the [wiki](https://github.com/ericclack/geekclub/wiki) to get started. There's some basic [documentation for the geekclub module](http://htmlpreview.github.io/?https://github.com/ericclack/geekclub/blob/master/geekclub/pyscratch.html) or you can [view the source code](https://github.com/ericclack/geekclub/blob/master/geekclub/pyscratch.py).

