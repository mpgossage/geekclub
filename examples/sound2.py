import sys
sys.path.append('..')
from geekclub.pyscratch import *
from geekclub.sound import *

create_canvas()

# Not really necessary for this example, but why not:
sprite = ImageSprite('images/face.gif')
sprite.centre()
   
set_bpm(180)
laser = load_sound('sounds/laser.wav')
drum = load_sound('sounds/bass-drum.wav')
hh = load_sound('sounds/hh-cymbal.wav')

def lasers():
    laser.play()

def drums():
    drum.play()
    rest(.5)
    hh.play()

forever(lasers, beat_ms() * 3)
forever(drums, beat_ms())

mainloop()