import turtle
import random

try:
    import playsound  # Not part of standard Library.

    SOUND = True
except ImportError:
    SOUND = False


NUM_TOWERS = 20
MAX_TOWER_HEIGHT = 10
GAME_DELAY = 20
PLANE_DX = 12
BOMB_DY = -20
WIDTH = 800
HEIGHT = 600
GAME_AREA_WIDTH = WIDTH - 50
GAME_AREA_HEIGHT = HEIGHT - 50
cell_colors = ["black", "dark green", "brown"]


def game_loop():
    move_plane()
    if bomb_dropping:
        __continue_bomb_drop()
    screen.update()
    turtle.ontimer(game_loop, GAME_DELAY)


def move_plane():
    new_pos = (plane.xcor(), plane.ycor())
    if new_pos[0] > GAME_AREA_WIDTH // 2:
        plane.goto(- GAME_AREA_WIDTH // 2, plane.ycor() - cell_size)
    else:
        plane.goto(plane.xcor() + PLANE_DX, plane.ycor())

    if check_plane_tower_collision():
        restart(new_level=False)
    elif check_player_wins_level():
        restart(new_level=True)


def check_player_wins_level():
    if score >= winning_score:
        player_wins_level()
        return True
    return False


def player_wins_level():
    update_score_display()
    if SOUND:
        playsound.playsound("victory.wav")


def check_plane_tower_collision():
    for tower in towers:
        for cell in tower:
            if plane.distance(cell) <= cell_size / 2 + 10:  # Half cell size + half plane height
                plane_tower_collision()
                return True
    return False


def plane_tower_collision():
    bomb.hideturtle()  # If present when plane crashes
    plane.color("red")
    screen.update()
    if SOUND:
        playsound.playsound("plane_crash.wav")


def check_bomb_tower_collision():
    if bomb_dropping:
        for tower in towers:
            for cell in tower:
                if bomb.distance(cell) <= cell_size / 2 + 5:  # Half cell size + half bomb size
                    bomb_tower_collision(cell)
                    return True
        return False


def bomb_tower_collision(cell):
    global score, high_score  # Needed as values modified in this function.
    if SOUND:
        playsound.playsound("bombed.wav", False)
    cell.setx(-1000)
    score += 10
    if score > high_score:
        high_score = score
    update_score_display()


def start_bomb_drop():
    global bomb_dropping  # Needed as value modified in this function.
    # Prevent further key presses until drop is finished tp prevent event stacking.
    screen.onkey(None, "space")
    bomb.goto(plane.xcor(), plane.ycor())
    bomb.showturtle()
    bomb_dropping = True


def __continue_bomb_drop():
    bomb.goto(bomb.xcor(), bomb.ycor() + BOMB_DY)
    if check_bomb_tower_collision() or bomb.ycor() < - GAME_AREA_HEIGHT // 2:
        stop_bomb_drop()


def stop_bomb_drop():
    global bomb_dropping  # Needed as value modified in this function.
    bomb.hideturtle()
    bomb_dropping = False
    # It's now safe to allow another bomb drop, so rebind keyboard event.
    screen.onkey(start_bomb_drop, "space")


def update_score_display():
    pen.clear()
    pen.write("Score:{:2} High Score:{:2}".format(score, high_score), align="center", font=("Courier", 24, "normal"))


def get_towers(offset):
    result = []
    for col in range(-NUM_TOWERS // 2, NUM_TOWERS // 2):
        tower = []
        for level in range(random.randrange(1, MAX_TOWER_HEIGHT + 1)):
            block = turtle.Turtle(shape="square")
            block.shapesize(cell_size / 20)  # 20 is the default size of the "square" shape.
            block.color(random.choice(cell_colors))
            block.penup()
            block.goto(col * cell_size + offset, - GAME_AREA_HEIGHT // 2 + level * cell_size + offset)
            tower.append(block)
        result.append(tower)
    return result


def restart(new_level=False):
    global screen, plane, bomb, pen, cell_size
    global score, towers, winning_score, bomb_dropping

    # Fixed screen values
    screen = turtle.Screen()
    screen.title("Fly Game")
    screen.setup(WIDTH, HEIGHT)

    # MISC.
    cell_size = GAME_AREA_WIDTH / NUM_TOWERS  # Size of tower cells in pixels
    offset = (NUM_TOWERS % 2) * cell_size / 2 + cell_size / 2  # Center even and odd cells

    # Screen values which need resetting each level/game
    screen.clear()
    screen.bgcolor("Green")
    screen.listen()
    screen.onkey(start_bomb_drop, "space")
    screen.tracer(0)

    # Plane
    plane = turtle.Turtle(shape="triangle", visible=False)
    plane.color("Pink")
    plane.shapesize(1, 2)
    plane.penup()
    plane.goto(- GAME_AREA_WIDTH // 2, GAME_AREA_HEIGHT // 2)
    plane.showturtle()

    # Bomb
    bomb = turtle.Turtle(shape="square")
    bomb.hideturtle()
    bomb.color("red")
    bomb.shapesize(0.5)
    bomb.penup()
    bomb_dropping = False

    # Score Display
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.color("Crimson")
    pen.penup()
    pen.goto(0, 250)
    score = 0
    update_score_display()

    # Build new towers
    towers = get_towers(offset)

    # Here we handle the score for different scenarios for restarting the game - crashed plane or completed level.
    if not new_level:
        score = 0
        winning_score = sum(len(row) for row in towers) * 10
    else:
        winning_score += sum(len(row) for row in towers) * 10

    # Initial positions for plane and bomb.
    plane.goto(- GAME_AREA_WIDTH // 2, GAME_AREA_HEIGHT // 2)
    bomb.goto(- GAME_AREA_WIDTH // 2, GAME_AREA_HEIGHT // 2)
    # print(len(screen.turtles()))  # Check no memory leak.


def main():
    global high_score
    high_score = 0
    restart()
    game_loop()


if __name__ == "__main__":
    main()
    turtle.done()