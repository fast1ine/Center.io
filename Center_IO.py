import sys
import math
import pygame
from pygame.locals import QUIT
import pygame.font

pygame.font.init()
PURPLE = (115, 103, 240)  # main color
BLACK = (0, 0, 0)
RED = (255, 0, 99)

pygame.mixer.init(44100, -16,2,2048)
pygame.display.set_caption('Center.io')
theme_sound = pygame.mixer.Sound("music.wav") #소리 불러오기 (배경 음악)
arrow_sound = pygame.mixer.Sound("arrow.wav") #소리 불러오기 (발사음)
hit_sound = pygame.mixer.Sound("hit.wav") #소리 불러오기 (타격음)
gameover_sound = pygame.mixer.Sound("gameover.wav") #소리 불러오기 (게임 오버)
theme_sound.play(-1) #배경 음악 소리 재생 (현재설정: 무한반복)
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((1280, 720))
font = pygame.font.Font(None, 36)
size = 100  # 원 반지름
score = 0  # 점수
TargetScore = 100  # 목표 점수 (달성시 가시 이동 속도 증가)
degree = 0  # 삼각함수 각도
speed = 0.5  # 삼각함수 각도 증가
bullets = []
bullet_speed = 10
FPSCLOCK.tick(60)
GameActive = True
CoolTime = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if GameActive == True:
      # 1프레임당 동작하는 코드 작성
      DISPLAYSURF.fill("white")
      core = pygame.draw.circle(DISPLAYSURF, PURPLE, (640, 370), 40)  # 코어
      pygame.draw.circle(DISPLAYSURF, BLACK, [640, 600], 30, 3)

      # 이동 속도 증가
      if score == TargetScore:
          speed += 0.1
          TargetScore = score + 100

      # 가시 이동
      degree = degree + speed
      rad = degree * math.pi / 180
      Thorn = pygame.draw.rect(
          DISPLAYSURF, RED,
          [math.cos(rad) * size + 640,
          math.sin(rad) * size + 360, 20, 20])

      for bullet in bullets:
          bullet.y -= bullet_speed
          if bullet.y < 0:
              bullets.remove(bullet)
          if bullet.colliderect(core):
              bullets.remove(bullet)
              hit_sound.play() #타격음 소리 재생 (현재설정: 1회 재생)
              score += 5
          if bullet.colliderect(Thorn):
            bullets.remove(bullet)
            GameActive = False
            print(GameActive)
            gameover_sound.play() #게임 오버 소리 재생 (현재설정: 1회 재생)
          pygame.draw.rect(DISPLAYSURF, BLACK, bullet)

      text = font.render("Score: " + str(score), True, (0, 0, 0))  # 점수 표시
      DISPLAYSURF.blit(text, (10, 10))

      # 발사부
      if event.type == pygame.MOUSEBUTTONDOWN and CoolTime == 0:
          bullet = pygame.Rect(640, 600, 4, 10)
          bullets.append(bullet)
          arrow_sound.play() #발사음 소리 재생 (현재설정: 1회 재생)
          CoolTime = 600
      if not CoolTime==0:
          CoolTime-= 1
    if GameActive == False:
      DISPLAYSURF.fill("white")
      GameOverText = font.render("Game Over!", True, (0, 0, 0))
      DISPLAYSURF.blit(GameOverText, (600, 320))
      DISPLAYSURF.blit(text, (600, 360))
    pygame.display.flip() 