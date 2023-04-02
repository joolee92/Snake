import math
import random
import pygame


# Define class for each individual cube on the game board
class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    # Move the cube in a given direction
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # Draw the cube on the game surface
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            # Draw the eyes on the snake
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# Define class for the snake
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    # Move the snake in the appropriate direction based on keyboard input
    def move(self):
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            # Check for 'q' keypress and quit the game if detected
            if keys[pygame.K_q]:
                game_over = True

            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # Move the snake's body and turn the head as needed
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

        return game_over

    # Reset the snake to its starting position
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # Add a new cube to the end of the snake's body
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    # Draw the snake on the game surface
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

# Draw a grid on the game surface
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0, y), (w, y))

# Update the game window with the current score and high score
def redrawWindow(surface, score, high_score):
    global rows, width, s, snack
    surface.fill((0,0,0))

    # Create font object
    font = pygame.font.Font(None, 30)

    # Render score and high score text surfaces
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))

    # Blit text surfaces onto main game surface
    surface.blit(score_text, (10, 10))
    surface.blit(high_score_text, (width - high_score_text.get_width() - 10, 10))

    # Render quit text surface
    quit_text = font.render("Press 'q' to Quit", True, (255, 255, 255))
    quit_x = (width - quit_text.get_width()) / 2
    quit_y = rows * 23
    surface.blit(quit_text, (quit_x, quit_y))

    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

# Generate a random snack location for the snake to eat
def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)


# Main game loop
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True

    score = 0
    high_score = 0

    # Initialize font module
    pygame.font.init()

    clock = pygame.time.Clock()

    while flag:
        # Delay to control the game speed
        pygame.time.delay(50)

        # Tick method of clock object used to control the frames per second
        clock.tick(10)

        # Move the snake
        game_over = s.move()
        if game_over:
            break

        # Check if the snake eats a snack
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
            score += 1
            if score > high_score:
                high_score = score

        # Check if the snake has collided with itself or the game border
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                # Print the final score and change the high score if a new high score is achieved
                s.reset((10,10))
                if score > high_score:
                    high_score = score
                score = 0
                break

        # Update the game window
        redrawWindow(win, score, high_score)

        # Checks to see if 'q' has been pressed, ending the game if it has
        if game_over:
            try:
                pygame.quit()
            except pygame.error:
                pass

    pass

# Call the main function to run the game
main()

