import pygame
import time
import random

pygame.init()  # initiate pygame

display_width = 800
display_height = 600 

black = (0,0,0)
white = (255,255,255)
red = (252, 61, 61)
bright_red = (235, 52, 95)
green = (52, 235, 98)
bright_green = (61, 252, 90)

car_width = 60


pause = False


gameDisplay = pygame.display.set_mode((display_width, display_height))  # passed a tuple to avoid fnc from treating w&h as separate params
pygame.display.set_caption('Dodge')
clock = pygame.time.Clock()

carImg = pygame.image.load('assets/racecar-000.png')
obstacleCarImg = pygame.image.load('assets/racecar-001.png')


def obstacles_dodged(count):
    font = pygame.font.Font('fonts/BalsamiqSans-Regular.ttf', 16)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text, (5,5))


def obstaclecars(obstaclex, obstacley, obstaclew, obstacleh):
    gameDisplay.blit(obstacleCarImg, (obstaclex, obstacley))


def maincar(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('fonts/BalsamiqSans-Regular.ttf', 115)
    TextSurface, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurface, TextRect)

    pygame.display.update()
    
    time.sleep(2)

    game_loop()


def button(msg, x, y, w, h, inactive_clr, active_clr, action=None):
    
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    

    if x+w > mouse_pos[0] > x and y+h > mouse_pos[1] > y:  # x_cord + button_width > x_cord... it happens that we are in the biubdary of our box
        pygame.draw.rect(gameDisplay, active_clr, (x, y, w, h)) # apply hover effect
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive_clr, (x, y, w, h))
    

    smallText = pygame.font.Font('fonts/BalsamiqSans-Regular.ttf', 20)
    TextSurface, TextRect = text_objects(msg, smallText)
    TextRect.center = ( (x+(w/2)), (y+(h/2))) # center text in the button 
    gameDisplay.blit(TextSurface, TextRect)


def quitgame():
    pygame.quit()
    quit()

def resume():
    global pause
    pause = False

def paused():
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('fonts/BalsamiqSans-Italic.ttf', 115)
        TextSurface, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurface, TextRect)

        button("Resume", 350, 400, 100, 50, green, bright_green, resume)
        button("Quit", 350, 460, 100, 50, red, bright_red, quitgame)
        
        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('fonts/BalsamiqSans-Italic.ttf', 115)
        TextSurface, TextRect = text_objects("Dodge", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurface, TextRect)

        button("Start", 350, 400, 100, 50, green, bright_green, game_loop)
        button("Quit", 350, 460, 100, 50, red, bright_red, quitgame)
        
        pygame.display.update()
        clock.tick(15)


def crash():
    message_display('You crashed')


def game_loop():

    global pause

    x = (display_width*0.45)
    y = (display_height*0.8)

    x_change = 0
    
    obstacle_startx = random.randrange(0,display_width)
    obstacle_starty = -600 
    obstacle_speed = 7
    obstacle_width = 60
    obstacle_height = 75

    dodged = 0

    gameExit = False

    # EVENT LOOP 

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            # print(event)  # event log

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    pause = True
                    paused()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        x += x_change 

        gameDisplay.fill(white)


        obstaclecars(obstacle_startx, obstacle_starty, obstacle_width, obstacle_height)

        obstacle_starty += obstacle_speed

        maincar(x,y)

        obstacles_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if obstacle_starty > display_height:
            obstacle_starty = 0 - obstacle_height 
            obstacle_startx = random.randrange(0,display_width)
            dodged += 1
            obstacle_speed += 0.1
        
        if y < obstacle_starty + obstacle_height:
            # print('y crossover')
            if x > obstacle_startx and x < obstacle_startx + obstacle_width or x + car_width > obstacle_startx and x + car_width < obstacle_startx + obstacle_width: # need to get rid of this redundancy...oof
                # print('x crossover')
                crash()


        pygame.display.update() # or flip()
        clock.tick(60)  # Update .. FPS



game_intro()
game_loop()
pygame.quit()  # uninitiate pygame when the user wants to quit
quit()
