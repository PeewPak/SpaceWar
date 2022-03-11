import pygame 
pygame.font.init()
from pygame import mixer
mixer.init()

#Dispaly
pygame.display.set_caption("Space War")             #Name of the window
width, height = 1200, 600                            #Size of window
win = pygame.display.set_mode((width, height))      #Set display

border = pygame.Rect((width/2)-5, 0, 10, height)

FPS = 120
space_width, space_height = 55, 40
vel = 5
bullet_vel = 7
max_bullet = 5

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

health_font = pygame.font.SysFont("Comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)

#Load files
background = pygame.image.load("Assets/space.png")                               #Load backbround
background = pygame.transform.scale(background, (width, height))                    #Specify size of background

yellow_space = pygame.image.load("Assets/spaceship_yellow.png")                     #Load spaceship
yellow_space = pygame.transform.scale(yellow_space, (space_width, space_height))    #Specify size of spaceship
yellow_space = pygame.transform.rotate(yellow_space, 90)                            #Rotate spaceship

red_space = pygame.image.load("Assets/spaceship_red.png")
red_space = pygame.transform.scale(red_space, (space_width, space_height))
red_space = pygame.transform.rotate(red_space, 270)

bullet_hit_sound = mixer.Sound("Assets/hit.wav")                                    #Load sounds
bullet_fire_sound = mixer.Sound("Assets/shoot.wav")

def handle_bullets(red_bullet, yelllow_bullet, red, yellow):
    for bullet in yelllow_bullet:                                                #Fire bullet                                 
        bullet.x += bullet_vel
        if red.colliderect(bullet):                                              #Bullet hits
            pygame.event.post(pygame.event.Event(red_hit))                       #HIT
            yelllow_bullet.remove(bullet)                                        #Remove one bullet
        elif bullet.x > width:
            yelllow_bullet.remove(bullet)

    for bullet in red_bullet:                                                #Fire bullet                                 
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):                                       #Bullet hits
            pygame.event.post(pygame.event.Event(yellow_hit))                #HIT
            red_bullet.remove(bullet)                                        #Remove one bullet
        elif bullet.x < 0:
            red_bullet.remove(bullet)



def yellow_movement(keys, yellow):
    if keys[pygame.K_a] and yellow.x - vel > 0:                                 #Go left
        yellow.x -= vel
    if keys[pygame.K_d] and yellow.x + vel + yellow.width < border.x:           #Go right
        yellow.x += vel
    if keys[pygame.K_w] and yellow.y - vel > 0:                                 #Go up
        yellow.y -= vel
    if keys[pygame.K_s] and yellow.y + vel + yellow.height < height-15:         #Go down
        yellow.y += vel

def red_movement(keys, red):
    if keys[pygame.K_LEFT] and red.x - vel > border.x + border.width:           #Go left
        red.x -= vel
    if keys[pygame.K_RIGHT] and red.x + vel + red.width < width:                #Go right
        red.x += vel
    if keys[pygame.K_UP] and red.y - vel > 0:                                   #Go up
        red.y -= vel
    if keys[pygame.K_DOWN] and red.y + vel + red.height < height - 15:          #Go down
        red.y += vel
    

def draw_winner(text):
    draw_text = winner_font.render(text, 1, (255, 255, 255))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health):
    win.blit(background, (0, 0))                            #Display background
    #win.fill((255,20,125))
    red_bar = health_font.render("Health: " + str(red_health), 1, (255,255,255))  
    yellow_bar = health_font.render("Health: " + str(yellow_health), 1, (255,255,255))
    win.blit(red_bar, (width-red_bar.get_width() - 10, 10))
    win.blit(yellow_bar, (10,10))

    pygame.draw.rect(win, (0,0,0), border)                  #Display middle border

    for bullet in red_bullet:                               #Display bullets
        pygame.draw.rect(win, (255, 0, 0), bullet)
    for bullet in yellow_bullet:
        pygame.draw.rect(win, (0, 255, 0), bullet)

    win.blit(yellow_space, (yellow.x, yellow.y))            #Dispaly spaceships
    win.blit(red_space, (red.x, red.y))
    pygame.display.update()                                 #Refresh

#endless loop
def main():

    red_position = pygame.Rect(700, 300, space_width, space_height)
    yellow_position = pygame.Rect(100, 300, space_width, space_height)

    yellow_bullet = []
    red_bullet = []

    red_health = 10 
    yellow_health = 10


    clock = pygame.time.Clock()                     #Initiation FPS
    run = True
    while run:
        clock.tick(FPS)                             #Set FPS
        for event in pygame.event.get():            #List of different events
            if event.type == pygame.QUIT:           
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullet) < max_bullet:
                    bullet = pygame.Rect(yellow_position.x + yellow_position.width, yellow_position.y + yellow_position.height/2 - 2, 10, 5 )
                    yellow_bullet.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RSHIFT and len(red_bullet) < max_bullet:
                    bullet = pygame.Rect(red_position.x, red_position.y + red_position.height/2 - 2, 10, 5 )
                    red_bullet.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()

            if event.type == yellow_hit:
                yellow_health -=1
                bullet_hit_sound.play()

        winner_text = ""
        if yellow_health == 0:
            winner_text = "Red wins"
        if red_health == 0:
            winner_text = "Yellow wins"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys = pygame.key.get_pressed()
        yellow_movement(keys, yellow_position)
        red_movement(keys, red_position)

        handle_bullets(red_bullet, yellow_bullet, red_position, yellow_position)

        draw_window(red_position, yellow_position, red_bullet, yellow_bullet, red_health, yellow_health)

main()