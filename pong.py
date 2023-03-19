import pygame, sys
from time import sleep

pygame.init()
clock = pygame.time.Clock()

screen_width = 1400
screen_height = 800

font = pygame.font.SysFont(None, 50)

ping1 = pygame.mixer.Sound("D:\Personal Projects\pygame-pong\\assets\Ping1.wav")
ping2 = pygame.mixer.Sound("D:\Personal Projects\pygame-pong\\assets\Ping2.wav")
ping3 = pygame.mixer.Sound("D:\Personal Projects\pygame-pong\\assets\Ping3.wav")
ping4 = pygame.mixer.Sound("D:\Personal Projects\pygame-pong\\assets\Ping4.wav")
goal = pygame.mixer.Sound("D:\Personal Projects\pygame-pong\\assets\Goal.wav")

field_img = pygame.image.load('D:\Personal Projects\pygame-pong\\assets\\field.png')
field_img = pygame.transform.scale(field_img, (screen_width, screen_height))
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

pygame.display.set_icon(pygame.image.load('D:\Personal Projects\pygame-pong\\assets\icon.png'))


ball = pygame.Rect(screen_width/2-15,screen_height/2-15,30,30)
player = pygame.Rect(screen_width-20,screen_height/2-70,10,120)
opponent = pygame.Rect(10, screen_height/2-70,10,120)

player_score, opponent_score = 0,0
player_spd = 0
opponent_spd = 7
ball_dx, ball_dy = 7,7

state = 'play'
pa_b = pygame.rect.Rect((0,0,0,0))
def player_animation():
    global state
    if state == 'pause' or state == 'gameover': return
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
    player.y += player_spd

def opponent_animation():
    global state
    if state == 'pause' or state == 'gameover': return
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height
    if opponent.top < ball.y:
        opponent.top += opponent_spd
    if opponent.top >= ball.y:
        opponent.top -= opponent_spd

def reset_ball(direction):
    ball.x = (screen_width-ball.width)/2
    ball.y = (screen_height-ball.height)/2
    player.top = (screen_height/2)
    opponent.top = (screen_height/2)
    return 5*direction,5*direction

def ball_animation(ball_dx, ball_dy):
    global player_score, opponent_score, state
    if state == 'pause' or state == 'gameover':
        return ball_dx, ball_dy
    ball.x += ball_dx
    ball.y += ball_dy
    if ball.colliderect(player):
        ping1.play()
        ball_dx *= -1.5
        return ball_dx, ball_dy
    if ball.colliderect(opponent):
        ping2.play()
        ball_dx *= -1.5
        return ball_dx, ball_dy
    if ball.top <= 0:
        ping3.play()
        ball_dy *= -1.15
    if ball.bottom >= screen_height:
        ping4.play()
        ball_dy *= -1.15
    if ball.left <= 0:
        player_score += 1
        if player_score >= 5:
            state = 'gameover'
            return 3,3
        ball_dx, ball_dy = reset_ball(1)
        state = 'goal'
        goal.play()
    if ball.right >= screen_width:
        opponent_score += 1
        if opponent_score >= 5:
            state = 'gameover'
            return 0,0
        ball_dx, ball_dy = reset_ball(-1)
        state = 'goal'
        goal.play()
    ball_dx = min(ball_dx, 200)
    return ball_dx, ball_dy



def draw_shapes():
    global state, pa_b
    screen.blit(field_img,(0,0),)
    pygame.draw.aaline(screen, (255,255,255), (screen_width/2,0), (screen_width/2,screen_height))
    screen.blit(font.render(str(opponent_score),True, (0,0,255)), (20, 20))
    screen.blit(font.render(str(player_score),True, (255,0,0)), (screen_width-40, 20))
    if state == 'play':
        pygame.draw.ellipse(screen,(255,255,255),ball)
        pygame.draw.rect(screen,(255,255,255),player)
        pygame.draw.rect(screen,(0,0,0),opponent)
    if state == 'pause':
        pygame.draw.ellipse(screen,(255,255,255),ball)
        pygame.draw.rect(screen,(255,255,255),player)
        pygame.draw.rect(screen,(0,0,0),opponent)
        screen.blit(font.render(str("PAUSE!"),True, (255,0,255)), (screen_width/2 - 62, screen_height/2 - 15))
    if state == 'goal':
        screen.blit(font.render(str("GOAL!"),True, (255,0,255)), (screen_width/2 - 50, screen_height/2))
        pygame.display.flip()
        sleep(.2)
        state = 'play'
    if state == 'gameover':
        screen.blit(font.render(str("GAME OVER!"),True, (255,0,255)), (screen_width/2 - 100, screen_height/2-100))
        pa_b = screen.blit(font.render(str("PLAY AGAIN?"),True, (255,0,255)), (screen_width/2 - 100, screen_height/2))
        

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_spd = 7
            if event.key == pygame.K_UP:
                player_spd = -7
            if event.key == pygame.K_SPACE:
                if state == 'play':
                    state = 'pause'
                elif state == 'pause':
                    state = 'play'
            # Easy gameover state for testing
            # if event.key == pygame.K_w:
            #     state = 'gameover'
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if pa_b.collidepoint(pos):
                player_score,opponent_score = 0,0
                state = 'play'
                reset_ball(-1)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN): 
                player_spd = 0

        

    ball_dx, ball_dy = ball_animation(ball_dx, ball_dy)
    player_animation()
    opponent_animation()

    draw_shapes()
    pygame.display.flip()
    clock.tick(144)