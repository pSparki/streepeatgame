#----------------------------------------------------
#Title: Streepeat.py
#Purpose: A submission for the NPA class
#Author: Alex Vause
#Date: 25/04/2022
#----------------------------------------------------

#----------------------------------------------------
#Import Libraries
#----------------------------------------------------
import pygame, random, pygame.freetype
#----------------------------------------------------


#----------------------------------------------------
#Spawning Function
#----------------------------------------------------
def spawn_enemy():
    enemyRandomX = random.randint(0,4)
    newEnemyY = -enemyImage.get_height() #Barely above the screen
    if enemyRandomX == 0:
        newEnemyX = 155
    elif enemyRandomX == 1:
        newEnemyX = 265
    elif enemyRandomX == 2:
        newEnemyX = 375
    elif enemyRandomX == 3:
        newEnemyX = 485
    else:
        newEnemyX = 595
    enemyPosList.append([newEnemyX,newEnemyY])
#End funtion definition
#----------------------------------------------------

#----------------------------------------------------
#Initialisation and Setup
#----------------------------------------------------
#Initialise python so we can use it
pygame.init()

#Set yo tge game clock
mainClock = pygame.time.Clock()

#Set up the drawing Window
WINDOWWIDTH = 750
WINDOWHEIGHT = 750
screen = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
pygame.display.set_caption("Streepeat")

#Set up some variables to use later in the game
running = True

#Set up colors
LIGHTGRAY = (25, 25, 25)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Set up player
playerImage = pygame.image.load("Assets/Kathryn.png")
playerPos = (WINDOWWIDTH/2 - playerImage.get_width()/2, WINDOWHEIGHT - 100)
playerRect = pygame.Rect(playerPos[0], playerPos[1], playerImage.get_width(), playerImage.get_height())
playerAlive = True

#Set up enemies
enemyImage = pygame.image.load("Assets/Pedestrian.png")
enemyRect = pygame.Rect(0, 0, enemyImage.get_width(), enemyImage.get_height())
enemySpeed = 150
enemyPosList = []
NUM_ENEMIES = 3
for i in range(NUM_ENEMIES):
    spawn_enemy()
#END for loop for enemy spawning
SPAWNCOOLDOWN = 1.75
timeSinceSpawn = 0

#Set up Push
pushImage = pygame.image.load("Assets/Push.png")
pushRect = pygame.Rect(0,0, pushImage.get_width(), pushImage.get_height())
pushPosList = []
PUSHSPEED = 400
PUSHCOOLDOWN = 0.25
timeSincePush = 0

#Set up UI Font
UIFont = pygame.freetype.Font("Fonts/StreepeatFont.ttf"),24)

#Set up Score
score = 0
scorePerEnemy = 10

#Set up win condition
scoreToWin = 750
winGame = False

#Set up Lives
playerLives = 3
timeSinceHit = 0
gameSlowTime = 2.25

#----------------------------------------------------
#Game Loop
#----------------------------------------------------
#Run over and over until user asks to quit
while running:

    #----------------------------------------------------
    #Input
    #----------------------------------------------------
    #Did the user click the window close button?

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #----------------------------------------------------
    #Update
    #----------------------------------------------------
    #Get the frame time in milliseconds
    frameMS = mainClock.tick(60)
    frameSec = frameMS / 1000

    #Pause the game if we won or lost
    if not playerAlive or winGame:
        frameSec = 0
    #END if for game pause

    #Process Movement
    #Collect inputs and determine if lane needs to be changed or not
    if keys[pygame.K_LEFT or keys[pygame.K_a]:
        playerPos[0] -= playerPos[0] - 110
    if keys[pygame.K_RIGHT or keys[pygame.K_d]:
        playerPos[0] -= playerPos[0] + 110

    #Move the player's rectangle based on the position variable
    playerRect.left = playerPos[0]
    playerRect.top = playerPos[1]

    #Increase time since last push was used
    #based on how much time passed this frame
    timeSinceFire += frameSec

    #Pushing
    if keys[pygame.K_SPACE or keys[pygame.K_w]:
        #Push any pedestrians in the lane
        newPushX = playerPos[0] + 20
        newPushY = playerPos[1]
        pushPosList.append([newPushX,newPushY])
        timeSincePush = 0

        

    #End push

    #Update for push
    for pushPos in pushPosList:
        pushPos[1] -= PUSHSPEED * frameSec

        #Update push rectangle
        pushRect.left = pushPos[0]
        pushRect.top = pushPos [1]

        #Loop through all enemies and check if THIS
        #particular bullet has hit each enemy

        for enemyPos in enemyPosList[:]:

            #Update enemy rectangle
            enemyRect.left = enemyPos[0]
            enemyRect.top = enemyPos[1]

            #If a push collides with an enemy.
            if pygame.Rect.colliderect(pushRect,enemyRect):
                #Remove THIS enemy from the list
                enemyPosList.remove(enemyPos)

                score += scorePerEnemy

                #Check if we won:
                if score >= scoreToWin:
                    winGame = True
                #END if for checking if we won

            #END if for push/enemy collision

        #END enemy loop (for push/enemy collision)

    #END bullet loop

    # Add to time since last enemy spawned
    timeSinceSpawn += frameSec

    #Check if it is time to spawn a new enemy
    if timeSinceSpawn >= SPAWNCOOLDOWN:
        spawn_enemy()
        timeSinceSpawn = 0
    #END if for checking enemy spawn

    #Update enemies
    for enemyPos in enemyPosList:
        #Move enemy down
        enemyPos[1] += enemySpeed * frameSec

        #Update the enemy rectangle
        enemyRect.left = enemyPos[0]
        enemyRect.top = enemyPos[1]

        #Check if the enemy hit the player
        if pygame.Rect.colliderect(playerRect,enemyRect):

            #Deal damage to the player
            playerLives -= 1

            #Remove the enemy
            enemyPosList.remove(enemyPos)

            #Did they die?
            if health <= 0:
                #If so, kill the player
                playerAlive = False
            #END if for health
            
            #Slow down enemies temporarily
            enemySpeed = enemySpeed / 3
            timeSinceHit = 0

            #Check if enough time has passed
            #Since player lost a life
            if timeSinceHit >= gameSlowTime:
                #Increase Speed again
                enemySpeed = enemySpeed * 3

            #END if for enemy slow

        #END if for collision

        #Check if the enemy is off the screen
        if enemyPos[1] > WINDOWHEIGHT:
            #Remove the enemy
            enemyPosList.remove(enemyPos)

            #Lose a life
            playerLives -= 1

            #Did they die?
            if health <= 0:
                #If so, kill the player
                playerAlive = False
            #END if for health

            #Slow down enemies temporarily
            enemySpeed = enemySpeed / 3
            timeSinceHit = 0

            #Check if enough time has passed
            #Since player lost a life
            if timeSinceHit >= gameSlowTime:
                #Increase Speed again
                enemySpeed = enemySpeed * 3

            #END if for enemy slow

        #END if for enemy off screen check

    #END for loop for enemy update

    #Draw

    #Fill the background with a colour
    screen.fill(WHITE)

    #Draw Everything

    #Draw items based on the game state
    if winGame : #Player has "won"

        textRect = UIFont.get_rect("Escort complete!")

        UIFont.render_to(screen, (WINDOWWIDTH/2-textRect.width/2, WINDOWHEIGHT/2-textRect.height/2, "Escort complete!", BLACK )

    elif not playerAlive : #Player has lost

        textRect = UIFont.get_rect("Escort failed!")
        UIFont.render_to(screen, (WINDOWWIDTH/2-textRect.width/2, WINDOWHEIGHT/2-textRect.height/2, "Escort  failed!", BLACK )

    else:

        screen.blit(playerImage,playerPos)

        #Draw all of the enemies
        for enemyPos in enemyPosList:
            screen.blit(enemyImage,enemyPos)
        #End for loop for enemy drawing

        #Draw all of the "Pushes"
        for pushPos in pushPosList:
            screen.blit(bulletImage,bulletPos)
        #End for looop for bullet drawing

    #END if for game state drawing

    #Draw the UI Text
    UIFont.render_to(screen, (10,50), "Score: "+str(score), (0, 0, 0) )

    #Draw the UI Text
    UIFont.render_to(screen, (10,50), "Lives:", (0, 0, 0) )

    #Flip the display to put it all onscreen
    pygame.display.flip()

#END of game loop


#Program Exit
pygame.quit()
