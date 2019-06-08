from jet_pack_lib import *

"""Big Bang Fair demo - Thrust

TO DO:
- Place platforms in better places
- Aliens appear at RHS of screen too
- Take off w sprite = next level
- Take off w sprite = repeat level

Then:
- Introduce bugs or remove features
- Print score so can record on chart
- Fuel look better on rocket
- Take off results in next level (faster current level?)
- 

Bugs:
- Platforms in the wrong place  (160,200, 700,250),
- Reversed controls
- Too many aliens
"""

create_canvas(background="black")

# Mouse or keyboard
MOUSE_CONTROL = True

# ---------------------------------------------------------
# Create your sprite objects

sprite = Sprite(canvas().create_oval(10,10, 50,50, fill="yellow"))
sprite.centre()
sprite.max_speed = 7
sprite.in_rocket = False

platform_rectangles = [(50,150, 200,200, "white"),
                       (380, 500, 530,550, "yellow"),
                       (700,300, 800,350, "green"),
                       #(160,200, 700,250, "blue"),
                       (0,CANVAS_HEIGHT-50, CANVAS_WIDTH,CANVAS_HEIGHT, "white")]

platforms = make_platforms(platform_rectangles)

# Our world
world = Struct(lives=3, score=0, status='play',
               sprite = sprite,
               rocket_parts = [],
               aliens = [],
               fuel = [],
               flames = []
               )

# Variables and constants

LANDING_ZONE = 550
MAX_FUEL = 3
DROP_SPEED = 5
MAX_FLAMES = 5
MAX_ALIENS = 50

# How likely is next rocket part or fuel to appear each tick?
PROB_NEXT_PART = 0.5 

# ---------------------------------------------------------
# Define your functions to control the game and its sprites
# -- these must be defined before the event handlers

def key_control():
    old_speed_x = sprite.speed_x
    if is_key_down('z'):
        sprite.speed_x -= 1
    if is_key_down('x'):
        sprite.speed_x += 1
    if is_key_down(' '):
        sprite.speed_y -= 1
        
    if old_speed_x == sprite.speed_x:
        sprite.speed_x *= 0.9

def mouse_control():
    old_speed_x = sprite.speed_x
    if mousex() < sprite.x - sprite.width:
        sprite.speed_x -= 1
    if mousex() > sprite.x + 2 * sprite.width:
        sprite.speed_x += 1
    if mousey() < sprite.y:
        sprite.speed_y -= 1

    if old_speed_x == sprite.speed_x:
        sprite.speed_x *= 0.9

def move_sprite():
    # Gravity
    sprite.speed_y += 0.5

    # Platforms
    p = sprite.touching_any(platforms)
    if p:
        sprite.bounce_off(p)

    # Move
    sprite._limit_speed()
    sprite.move_with_speed()
    sprite.if_on_edge_wrap()

    # Hit an alien?
    if sprite.touching_any(world.aliens):
        banner("You hit an alien!", 2000, fill="white")
        world.lives -= 1
        if world.lives == 0:
            end_game("Game over!", fill="white")
        restart_level(world)

def fire():
    direction = sign(sprite.speed_x) or 1
    x = sprite.x + sprite.width / 2
    y = sprite.y + sprite.height / 2
    fsprite = Sprite(canvas().create_rectangle(
                        x + (direction * 30), y, x + (direction*500), y+3,
                        fill="yellow", outline=None))
    # Has the lazer hit any aliens?
    a = fsprite.touching_any(world.aliens)
    while a:
        a.delete()
        world.aliens.remove(a)
        world.score += 10
        # Has the lazer hit any other aliens?
        a = fsprite.touching_any(world.aliens)
        
    # Delete the lazer in 1/10th second
    future_action(lambda: fsprite.delete(), 100)

def new_alien():
    a = Sprite(canvas().create_oval(0,0, 50,50, fill="red"))
    a.max_speed = 3
    
    if random.random() < 0.5:
        a.move_to(random.randint(0, CANVAS_WIDTH * .9), 0)
    else:
        a.move_to(CANVAS_WIDTH, random.randint(0, CANVAS_HEIGHT *.6))
        
    a.speed_x = -random.randint(3,8)
    a.speed_y = 2
    return a

def move_aliens():
    if len(world.aliens) < MAX_ALIENS and random.random() < 0.1:
        world.aliens.append(new_alien())
        
    for a in world.aliens:
        #a.accelerate_towards(sprite.x, sprite.y, steps=0.2)
        
        a.move_with_speed()
        if a.y > CANVAS_HEIGHT or a.touching_any(platforms):
            a.delete()
            world.aliens.remove(a)
        else:
            a.if_on_edge_wrap()




     
def in_landing_zone(x):
    return (LANDING_ZONE-5) < x < (LANDING_ZONE+5)

def move_rocket_parts():
    if ready_for_next_rocket_part(world) and random.random() < PROB_NEXT_PART:
        world.rocket_parts.append(new_rocket_part(world))

    if world.rocket_parts:
        r = world.rocket_parts[-1]
        if not r.in_place:
            if r.touching(sprite) and not r.landing:
                r.move_to(sprite.x, sprite.y)
                if in_landing_zone(r.x):
                    world.score += 50
                    r.move_to(LANDING_ZONE, r.y)
                    r.landing = True
                    r.speed_y = DROP_SPEED
            elif r.landing and (r.touching_any(platforms)
                                or r.touching_any(world.rocket_parts[:-1])):
                r.in_place = True
                r.landing = False
            elif not r.touching_any(platforms):
                r.move_with_speed()

def new_fuel():
    f = Sprite(canvas().create_rectangle(0,0, 100,40, fill="purple"))
    f.move_to(random.randint(0, CANVAS_WIDTH), 0)
    f.speed_x = 0
    f.speed_y = 1
    f.in_place = False
    f.landing = False
    return f

def ready_for_next_fuel():
    return parts_complete(world.rocket_parts) and parts_left(world.fuel) and parts_in_place(world.fuel)

def move_fuel():
    if ready_for_next_fuel() and random.random() < PROB_NEXT_PART:
        world.fuel.append(new_fuel())

    if world.fuel:
        f = world.fuel[-1]
        if not f.in_place:
            if f.touching(sprite) and not f.landing:
                f.move_to(sprite.x, sprite.y)
                if in_landing_zone(f.x):
                    world.score += 50
                    f.move_to(LANDING_ZONE, f.y)
                    f.landing = True
                    f.speed_y = DROP_SPEED
            elif f.landing and (f.touching_any(platforms)
                                or f.touching_any(world.fuel[:-1])):
                f.in_place = True
                f.landing = False
            elif not f.touching_any(platforms):
                f.move_with_speed()

def new_flame():
    r = world.rocket_parts[0] # The base of the rocket
    size = 30 - len(world.flames) * 2
    x = LANDING_ZONE + r.width / 2 - size / 2
    y = r.y + r.height + len(world.flames) * size * .9
    return Sprite(canvas().create_oval(x,y, x+size,y+size,
                                       fill="red"))    
                
def ready_for_takeoff():
    return parts_complete(world.fuel) and parts_complete(world.rocket_parts)
                
def rocket_takeoff():
    if world.status not in ['readyfortakeoff', 'takeoff'] and ready_for_takeoff():
        banner("Ready for take off!", 1000, fill="white")
        world.status = 'readyfortakeoff'
        world.score += 100
        
    if world.status == 'readyfortakeoff':
        if sprite.touching_any(world.rocket_parts):
            sprite.in_rocket = True
            
        if len(world.flames) == MAX_FLAMES:
            world.status = 'takeoff'
            if sprite.in_rocket:
                banner("Take off!", 1000, fill="white")
            else:
                banner("You missed the rocket!", 1000, fill="white")
                world.lives -= 1
        
        elif random.random() < 0.02:
            world.flames.append(new_flame())

    if world.status == 'takeoff':
        for p in world.rocket_parts + world.fuel + world.flames:
            p.move(0, -5)

    if sprite.in_rocket:
        r = world.rocket_parts[0]
        sprite.move_to(r.x + r.width, r.y)

def update_score():
    show_variables([["Lives", world.lives],
                    ["Score", world.score]],
                   fill="white")

    
# ---------------------------------------------------------
# How will the user control the game? What will other
# sprites do? Add your event handlers here.

if MOUSE_CONTROL:
    forever(mouse_control, 25)
    when_button1_clicked(fire)
    
else:
    forever(key_control, 25)
    when_key_pressed('<Return>', fire)

forever(move_sprite, 25)
forever(move_aliens, 25)
forever(move_rocket_parts, 25)
forever(move_fuel, 25)
forever(rocket_takeoff, 25)
forever(update_score)

# ---------------------------------------------------------
# FINALLY
# Always call mainloop:

mainloop()
