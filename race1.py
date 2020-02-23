from random import randint
import pgzrun


WIDTH = 700
HEIGHT = 800


car = Actor("racecar")
car.pos = 250, 700
SPEED = 5
trackLeft = []
trackRight = []
trackCount = 0
trackPosition = 250
trackWidth = 120
trackDirection = False
gameStatus = 0
score = 0
level = 1
left_key = 2
right_key = 2
lives = 3


def draw():
    global gameStatus, level, lives, score
    screen.fill((128, 128, 128))
    if gameStatus == 0:
        car.draw()
        b = 0
        while b < len(trackLeft):
            trackLeft[b].draw()
            trackRight[b].draw()
            b += 1
        screen.draw.text("Score: " + str(score), (50, 30), color="black")
        screen.draw.text("Level: " + str(level), (50, 50), color="black")
        screen.draw.text("Lives: " + str(lives), (50, 70), color="black")
    if gameStatus == 1:
        screen.blit('rflag', (318, 268))
        screen.draw.text("Score: " + str(score), (315, 350), color="black")
        screen.draw.text("Level: " + str(level), (315, 380), color="black")
    if gameStatus == 2:
        screen.blit('cflag', (318, 268))


def update():
    global gameStatus, trackCount
    if gameStatus == 0:
        if keyboard.left:
            car.x -= left_key
        if keyboard.right:
            car.x += right_key
        update_track()


def make_track():
    global trackCount, trackLeft, trackRight, trackPosition, trackWidth, score, lives, gameStatus
    trackLeft.append(Actor("barrier", pos=(trackPosition - trackWidth, 0)))
    trackRight.append(Actor("barrier", pos=(trackPosition + trackWidth, 0)))
    if trackLeft[0].y >= HEIGHT:
        del trackLeft[0]
    if trackRight[0].y >= HEIGHT:
        del trackRight[0]
    trackCount += 1
    score += 1
    if score % 100 == 0:
        check_levels()
    if lives < 1:
        gameStatus = 1


def update_track():
    global trackCount, trackPosition, trackDirection, trackWidth, gameStatus, lives
    b = 0
    while b < len(trackLeft):
        if car.colliderect(trackLeft[b]) or car.colliderect(trackRight[b]):
            lives -= 1
            reset()
            b = 0
            trackLeft.append(Actor("barrier", pos=(trackPosition - trackWidth, 0)))
            trackRight.append(Actor("barrier", pos=(trackPosition + trackWidth, 0)))

        trackLeft[b].y += SPEED
        trackRight[b].y += SPEED
        b += 1
    if trackLeft[len(trackLeft) - 1].y > 32:
        if not trackDirection:
            trackPosition += 16
        if trackDirection:
            trackPosition -= 16
        if randint(0, 4) == 1:
            trackDirection = not trackDirection
        if trackPosition > 700 - trackWidth:
            trackDirection = True
        if trackPosition < trackWidth:
            trackDirection = False
        make_track()


def check_levels():
    global level, gameStatus, SPEED, left_key, right_key, lives
    level += 1
    SPEED += 1
    left_key += 1
    right_key += 1


def reset():
    global trackLeft, trackRight, trackPosition, trackWidth
    trackLeft = []
    trackRight = []
    trackPosition = 250
    trackWidth = 120
    car.pos = 250, 700


make_track()


pgzrun.go()
