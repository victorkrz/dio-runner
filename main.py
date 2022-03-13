import pygame
from sys import exit
from random import randint, choice
import os


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.player_walk = []
		for frame in range(0, 16):
			self.player_walk.append(pygame.transform.scale(pygame.image.load(os.path.join('images', 'dio_walk', f'{frame}.png')).convert_alpha(), (64, 120)))
		
		self.player_jump = []
		for frame in range(0, 13):
			self.player_jump.append(pygame.transform.scale(pygame.image.load(os.path.join('images', 'dio_jump', f'{frame}.png')).convert_alpha(), (64, 120)))

		self.player_index_walk = 0
		self.player_index_jump = 0

		self.image = self.player_walk[self.player_index_walk]
		self.rect = self.image.get_rect(midbottom = (80,305))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/ha.wav')
		self.jump_sound.set_volume(0.1)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 305:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 305:
			self.rect.bottom = 305

	def animation_state(self):
		if self.rect.bottom < 305:
			self.player_index_jump += 0.35
			if self.player_index_jump >= len(self.player_jump):self.player_index_jump = 0
			self.image = self.player_jump[int(self.player_index_jump)]
		else:
			self.player_index_walk += 0.2
			if self.player_index_walk >= len(self.player_walk):self.player_index_walk = 0
			self.image = self.player_walk[int(self.player_index_walk)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()


class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()

		if type == 'jotaro':
			self.frames = []
			for frame in range(0, 24):
				self.frames.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('images', 'jotaro', f'{frame}.png')).convert_alpha(), (64, 120)), True, False))			
			y_pos  = 305

		elif type == 'star_platinum':
			self.frames = []
			for frame in range(0, 22):
				self.frames.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('images', 'star_platinum', f'{frame}.png')).convert_alpha(), (100, 120)), True, False))
			y_pos = 170

		elif type == 'kakyoin':
			self.frames = []
			for frame in range(0, 16):
				self.frames.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('images', 'kakyoin', f'{frame}.png')).convert_alpha(), (64, 120)), True, False))			
			y_pos  = 305

		elif type == 'hierophant_green':
			self.frames = []
			for frame in range(0, 10):
				self.frames.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('images', 'hierophant_green', f'{frame}.png')).convert_alpha(), (100, 120)), True, False))
			y_pos = 170

		elif type == 'polnareff':
			self.frames = []
			for frame in range(0, 8):
				self.frames.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('images', 'polnareff', f'{frame}.png')).convert_alpha(), (64, 120)), True, False))
			y_pos = 305

		elif type == 'silver_chariot':
			self.frames = []
			for frame in range(0, 26):
				self.frames.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('images', 'silver_chariot', f'{frame}.png')).convert_alpha(), (100, 120)), True, False))
			y_pos = 170

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.3
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(255,255,255))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('DIO runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/Battle_Tendency_Opening.mp3')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('images/horizon.png').convert()
sky_x = 0
ground_surface = pygame.image.load('images/ground.png').convert()
ground_x = 0


# Intro screen
player_stand = pygame.image.load('images/dio_stance.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('DIO runner',False,(0,0,0))
game_name_rect = game_name.get_rect(center = (400,50))

game_message = test_font.render('Press space to start',False,(0,0,0))
game_message_rect = game_message.get_rect(center = (400,360))


# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['jotaro', 'star_platinum', 'kakyoin', 'hierophant_green', 'polnareff', 'silver_chariot'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		sky_x_rel = sky_x % sky_surface.get_rect().width
		screen.blit(sky_surface,(sky_x_rel - sky_surface.get_rect().width,0))
		if sky_x_rel < 800:
			screen.blit(sky_surface,(sky_x_rel, 0))
		sky_x -= 1

		ground_x_rel = ground_x % ground_surface.get_rect().width
		screen.blit(ground_surface,(ground_x_rel - ground_surface.get_rect().width,300))
		if ground_x_rel < 800:
			screen.blit(ground_surface,(ground_x_rel, 300))
		ground_x -= 6

		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill((169,169,169))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(0,0,0))
		score_message_rect = score_message.get_rect(center = (400,360))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)
