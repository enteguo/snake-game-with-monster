import turtle
import math
import time, random

################ init ################################
#初始化参数
speed = 10  #蛇速度
monster_speed = 6 #怪兽速度
is_space = 0     #是否按空格暂停
num_food = 9     #食物数量
time_using = 0
flag_first = 1
# set up rhe screen
wn = turtle.Screen()
wn.title("Snake by Olive")
wn.bgcolor("white")
wn.setup(width=500, height=500)
wn.tracer(0)     # turns of the screen update

# manual，操作手册
manual = turtle.Turtle()
manual.penup()
manual.goto(-100, 100)
manual.hideturtle()
manual.write("Welcome to Olive's version snake\n "
             "you are going to us 4 arrow keys to move the snake\n "
             "around the screen, trying to consume all the food items\n"
             "before the monster catches you\n\n"
             "click any where on the screen to start game, have fun!!!", False, 'center')

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.shapesize(0.5, 0.5)
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# monster
x1 = random.randint(-230, -150)
y1 = random.randint(-230, -150)
x2 = random.randint(150, 230)
y2 = random.randint(-150, 230)
monster = turtle.Turtle()
monster.radians()
monster.shapesize(0.5, 0.5)
monster.speed(0)
monster.shape("square")
monster.color("blue")
monster.penup()
if abs(x1) < x2:
    x1 = x2
if abs(y1) < y2:
    y1 = y2
monster.goto(x1, y1)
monster.direction = "stop"
wn.update()
#####################################################

#monster move
def monster_move(x, y):
    theta = monster.towards(x,y)
    x = monster.xcor()
    y = monster.ycor()
    if abs(math.cos(theta)) > abs(math.sin(theta)):
        if math.cos(theta)>0:
            monster.setx(x + monster_speed)
            monster.sety(y)
        else:
            monster.setx(x - monster_speed)
            monster.sety(y)
    else:
        if math.sin(theta) > 0:
            monster.setx(x)
            monster.sety(y+ monster_speed)
        else:
            monster.setx(x)
            monster.sety(y - monster_speed)

# Snake move
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + speed)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - speed)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - speed)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + speed)


# keyboard handling
def go_up():
    global is_space
    is_space = 0
    head.direction = "up"


def go_down():
    global is_space
    is_space = 0
    head.direction = "down"


def go_left():
    global is_space
    is_space = 0
    head.direction = "left"


def go_right():
    global is_space
    is_space = 0
    head.direction = "right"

def do_stop():
    global is_space
    is_space = 1
    head.direction = "stop"

# check for collision with borders
def check_collision_borders():
    global flag_collision
    if head.xcor() > 235:
        y = head.ycor()
        head.sety(y)
        x = 235
        head.setx(x)
        flag_collision = 0
    elif head.xcor() < -235:
        y = head.ycor()
        head.sety(y)
        x = -235
        head.setx(x)
        flag_collision = 0
    elif head.ycor() > 235:
        y = 235
        head.sety(y)
        x = head.xcor()
        head.setx(x)
        flag_collision = 0
    elif head.ycor() < -235:
        y = -235
        head.sety(y)
        x = head.xcor()
        head.setx(x)
        flag_collision = 0
    else:
        flag_collision = 1

    return flag_collision

#设置食物初始位置
def set_food(num_food):
    # Food
    food = {}
    for idx in range(0, num_food):
        food.update({idx: turtle.Turtle()})
        food[idx].speed(0)
        x = random.randint(-230, 230)
        y = random.randint(-230, 230)
        food[idx].penup()
        food[idx].goto(x, y)
        food[idx].color("black")
        food[idx].hideturtle()
        food[idx].write(str(idx + 1), False, 'center')
    return food

def get_second():
    global time_using
    time_using = time_using + 1
    wn.ontimer(get_second, 1000)

#开始游戏
def start_game(x, y):
    global flag_first
    if flag_first == 1:
        global speed
        global monster_speed
        segments = []
        snake_positions = []
        delay = 0.2
        num_eat = 5
        flag_collision = 1
        is_win = 0
        is_lose = 0
        contacted_num = 0
        manual.clear()
        food = set_food(num_food)
        speed_backup = speed
        flag_first = 0
        # Main
        start = time.time()

        while True:
            wn.update()
            # 更新蛇的身体
            if flag_collision > 0 and is_win != 1 and is_lose != 1 and is_space != 1:
                if num_eat > 0:
                    head.color('red', 'black')
                    new_body = head.stamp()
                    segments.append(new_body)
                    num_eat = num_eat - 1
                    head.color('green')
                    snake_positions.append(head.pos())
                else:# 没吃食物的时候更新蛇的身体
                    head.color('red', 'black')
                    new_body = head.stamp()
                    segments.append(new_body)
                    head.clearstamp(segments[0])
                    del segments[0]
                    head.color('green')
                    snake_positions.append(head.pos())
                    del snake_positions[0]

            # 吃食物
            for idx in food:
                if head.distance(food[idx]) < 20:
                    food[idx].clear()
                    food[idx].isvisible()
                    del food[idx]
                    num_eat = num_eat + idx + 1
                    speed_backup = speed_backup - 0.1 * len(segments)
                    break
            move()
            monster_move(head.xcor(), head.ycor()) #怪兽的移动
            # is win?
            if len(food) == 0:
                is_win = 1
                win = turtle.Turtle()
                win.penup()
                win.goto(0, 0)
                win.hideturtle()
                win.write("win win win win win", False, 'center')

            #game over
            if head.distance(monster) < 10:
                is_lose = 1
                lose = turtle.Turtle()
                lose.penup()
                lose.goto(0, 0)
                lose.hideturtle()
                lose.write("Game over!", False, 'center')

            # 怪兽接触到蛇的身体
            for idx in snake_positions:
                if monster.distance(idx) < 10:
                    contacted_num = contacted_num + 1
                    break
            flag_collision = check_collision_borders()  # 是否碰到墙壁
            end = time.time()
            #改变蛇的速度
            if num_eat > 0 and is_win != 1 and is_lose != 1:
                wn.title("Snake game     " + "contacted:" + str(contacted_num) + "     " + "time:" + str(int(time_using)))
                speed = 6
            elif is_win == 1 or is_lose == 1:
                speed = 0
                monster_speed = 0
            else:
                wn.title("Snake game     " + "contacted:" + str(contacted_num) + "     " + "time:" + str(int(time_using)))
                speed = speed_backup
            time.sleep(delay)

wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(do_stop, "space")
wn.onscreenclick(start_game)
wn.ontimer(get_second, 1000)  # 定时1秒钟
wn.mainloop()