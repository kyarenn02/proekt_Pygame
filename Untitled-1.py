import pygame, random, sys
from pygame.locals import *




WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0,0,0)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5





def terminate():
    pygame.quit()
    sys.exit()

def PressEscKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def Baddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def Text(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Космолотль')
pygame.mouse.set_visible(False)


font = pygame.font.SysFont(None, 48)


gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('zadniyfon.mp3')


playerImage = pygame.image.load('aks1.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('kam1.png')


Text('Спаси Аксолотля от камней!', font, windowSurface, (WINDOWWIDTH / 8), (WINDOWHEIGHT / 3))
Text('Нажми a, чтобы начать!', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
PressEscKey()


topScore = 0
while True:

    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:

                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)


        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)


        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)


        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)


        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)


        windowSurface.fill(BACKGROUNDCOLOR)


        Text('Рекорд: %s' % (score), font, windowSurface, 31, 0)
        Text('Лучший рекорд: %s' % (topScore), font, windowSurface, 31, 40)


        windowSurface.blit(playerImage, playerRect)


        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()


        if Baddie(playerRect, baddies):
            if score > topScore:
                topScore = score
            break

        mainClock.tick(FPS)


    pygame.mixer.music.stop()
    gameOverSound.play()

    Text('Аксолотлю больно:<,', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    Text('попробуй сначало!', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    PressEscKey()

    gameOverSound.stop()