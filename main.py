import pygame
import time
import random

black = (0, 0, 0)
white = (255, 255, 255)
green = (34, 139, 34)
blue = (64, 224, 208)

pygame.init()

surfaceWidth = 800
surfaceHeight = 500
surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
pygame.display.set_caption('Flappy Test')
clock = pygame.time.Clock()

img = pygame.image.load('bird.png')
img_width = img.get_size()[0]
img_height = img.get_size()[1]


def blocks(x_block, y_block, block_width, block_height, gap):
    pygame.draw.rect(surface, green, [x_block, y_block, block_width,
                                      block_height])
    pygame.draw.rect(surface, green, [x_block, y_block + block_height + gap,
                                      block_width,
                                      surfaceHeight])


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue
        return event.key

    return None


def makeTextObjs(msg, text):
    textSurface = text.render(msg, True, white)
    return textSurface, textSurface.get_rect()


def msg_surface(msg):
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    largeText = pygame.font.Font('freesansbold.ttf', 120)

    titleTextSurf, titleTextRect = makeTextObjs(msg, largeText)
    titleTextRect.center = surfaceWidth/2, surfaceHeight/2
    surface.blit(titleTextSurf, titleTextRect)

    typeTextSurf, typeTextRect = makeTextObjs('Restarting.....',
                                              smallText)
    typeTextRect.center = surfaceWidth/2, ((surfaceHeight/2) + 100)
    surface.blit(typeTextSurf, typeTextRect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit is None:
        clock.tick()

    main()


def show_score(score):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(f'Score: {str(score)}', True, white)
    surface.blit(text, [5, 5])


def gameOver():
    msg_surface('Game Over')
    time.sleep(5)


def bird(x, y, image):
    surface.blit(image, (x, y))


def main():
    x = 150
    y = 200
    y_move = 0

    x_block = surfaceWidth
    y_block = 0

    block_width = 50
    block_height = random.randint(0, surfaceHeight / 2)
    gap = img_height * 5

    block_move = 5

    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 8

        y += y_move

        surface.fill(blue)
        bird(x, y, img)
        show_score(score)

        blocks(x_block, y_block, block_width, block_height, gap)
        x_block -= block_move

        # stay in bounds
        if y > surfaceHeight - img_height or y < 0:
            gameOver()

        # blocks on screen
        if x_block < (-1 * block_width):
            x_block = surfaceWidth
            block_height = random.randint(0, surfaceWidth / 2)

        # collides with block
        if x + img_width > x_block and x < x_block + block_width:
            if y < block_height or y + img_height > block_height + gap:
                gameOver()

        # score handling
        if x > x_block + block_width and x < x_block+block_width+img_width/5:
            score += 1
            print(score)

        pygame.display.update()
        clock.tick(80)


main()
pygame.quit()
quit()
