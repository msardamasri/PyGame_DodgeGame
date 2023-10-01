import pygame
import time
import random
pygame.font.init()

#window configuration
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game")

#backgound variables
BG = pygame.image.load("background.png")

#player variables
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60
PLAYER_SPEED = 8
PLAYER_IMAGE = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("player.png"), 180), (PLAYER_WIDTH, PLAYER_HEIGHT))

#star variables
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_SPEED = 4

FONT = pygame.font.SysFont("roboto", 30)

def show_menu():
    title_font = pygame.font.SysFont("roboto", 70)
    title_text = title_font.render("Dodge Game", 1, (54, 184, 249, 255))
    menu_font = pygame.font.SysFont("roboto", 50)
    instructions_text = menu_font.render("Use 'A' 'D' keys to move", 1, "white")
    exit_font = pygame.font.SysFont("roboto", 20)
    exit_text = exit_font.render("Press SPACE to play", 1, "white")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False

        WIN.fill((0, 0, 0))
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/2 - title_text.get_height() - 100))
        WIN.blit(instructions_text, (WIDTH/2 - instructions_text.get_width()/2, HEIGHT/2 + 50))
        WIN.blit(exit_text, (WIDTH/2 - exit_text.get_width()/2, HEIGHT/2 + 250))

        pygame.display.update()

def show_end_menu(elapsed_time):
    title_font = pygame.font.SysFont("roboto", 70)
    title_text = title_font.render(f"Your score was: {elapsed_time:.2f} seconds", 1, "white")  # Usando f-string para formatear elapsed_time
    menu_font = pygame.font.SysFont("roboto", 50)
    result = ""
    if elapsed_time <= 20:
        result = "Uninstall the game"
    elif elapsed_time <= 40:
        result = "Not that bad"
    else:
        result = "AWESOME"
    menu_text = menu_font.render(result, 1, "white")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill((0, 0, 0))
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/2 - title_text.get_height() - 100))
        WIN.blit(menu_text, (WIDTH/2 - menu_text.get_width()/2, HEIGHT/2 + 50))

        pygame.display.update()
        pygame.time.delay(8000)
        run = False


#this function will fill the background with the image proportionally
def backgroundScale():
    bg_width, bg_height = BG.get_size()

    scale = max(WIDTH / bg_width, HEIGHT / bg_height)
    scaled_width = int(bg_width * scale)
    scaled_height = int(bg_height * scale)
    scaled_bg = pygame.transform.scale(BG, (scaled_width, scaled_height))

    bg_x = (WIDTH - scaled_width) // 2
    bg_y = (HEIGHT - scaled_height) // 2

    return scaled_bg, bg_x, bg_y

def draw(player, elapsed_time, stars, starTime_increment):
    scaled_bg, bg_x, bg_y = backgroundScale()
    WIN.blit(scaled_bg, (bg_x, bg_y))

    time_text = FONT.render(f"Score -> {round(elapsed_time)}", 1, "white")
    WIN.blit(time_text, (10, 10))
    
    adjusted_difficulty = (2000 - starTime_increment) / 200 + 1
    difficulty_text = FONT.render(f"Difficulty -> {round(adjusted_difficulty)}", 1, "white")
    WIN.blit(difficulty_text, (10, 60))

    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def playerMovement(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - PLAYER_SPEED >= 0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player.x + PLAYER_SPEED + player.width <= WIDTH:
        player.x += PLAYER_SPEED

def starMovement(stars, player):
    for star in stars[:]:
        star.y += random.randint(STAR_SPEED, STAR_SPEED+3)
        if star.y > HEIGHT:
            stars.remove(star)
        elif star.y + star.height >= player.y and star.colliderect(player):
            stars.remove(star)
            return True

def main():
    show_menu()

    run = True
    hit = False

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    starTime_increment = 2000
    starTime_count = 0
    stars = []

    while run:
        #ms since last clock tick
        starTime_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        #add stars randomly
        if starTime_count > starTime_increment:
            for _ in range(random.randint(2, 4)):
                newStar = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(newStar, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            #decreases time through stars creation
            starTime_increment = max(200, starTime_increment - 50)
            starTime_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        playerMovement(player)
        hit = starMovement(stars, player)

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            show_end_menu(elapsed_time)
            break

        draw(player, elapsed_time, stars, starTime_increment)

    pygame.quit()

if __name__ == "__main__":
    main()