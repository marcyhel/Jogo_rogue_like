import pygame
import random
import pygame as pg

import math
import json
import time
import sys 
sys.path.insert(0, '../testePlat1.py')
class Inimigo:

	def __init__(self,x,y):
		self.direct=[0,0]
		self.posi=[x,y]
		self.alt=70
		self.larg=70		
		self.color=[random.randint(0,50),random.randint(0,20),random.randint(0,50)]
		
		self.sprite=self.carregarSprite('../images/coelho_Idle/',7)
		self.paralax=1
		self.contFrameIdle=0
		self.contFrameHate=0
		self.vida=100
		self.veloMov=5
		self.velocidade=[0,1]
		self.gravidade=0.5
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
		self.right = False
		self.left = False
		self.up = False
		self.down = False
		
	def palette_swap(self,surf, old_c, new_c):
		img_copy = pygame.Surface(surf.get_size())
		img_copy.fill(new_c)
		surf.set_colorkey(old_c)
		img_copy.blit(surf, (0, 0))
		return img_copy
	def changColor(self,image, color):
		colouredImage = pygame.Surface(image.get_size())
		colouredImage.fill(color)
		
		finalImage = image.copy()
		finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
		return finalImage
	def carregarSprite(self,diretorio,num):
		aux=[]
		for i in range(num):
			aux2=pygame.image.load(diretorio+str(i+1)+'.png').convert_alpha()
			
			aux2=self.changColor(aux2,(255- self.color[0],255- self.color[1],255-self.color[2]))
			aux.append(pygame.transform.scale(aux2, (self.larg, self.alt)))
		return aux
	def collision_test(self,rect,tiles):
		collisions = []
		for tile in tiles:
			if rect.colliderect(tile.rect):
				collisions.append(tile.rect)
		return collisions
	def muve(self,rect,movement,tiles): # movement = [5,2]
		rect.x += movement[0]
		collisions = self.collision_test(rect,tiles)
		for tile in collisions:
			if movement[0] > 0:
				rect.right = tile.left
			if movement[0] < 0:
				rect.left = tile.right
		rect.y += movement[1]
		collisions = self.collision_test(rect,tiles)
		for tile in collisions:
			if movement[1] > 0:
				rect.bottom = tile.top
				if self.velocidade[1]>8:
					logica.criaParticula(15,rect.left+self.larg/2,rect.bottom)
				self.velocidade[1]=0
			if movement[1] < 0:
				rect.top = tile.bottom
				self.velocidade[1]=0
		return rect
 
	
	def mover(self):
		self.direct=[0,0]
		self.direct[1]+=self.velocidade[1]
		if self.left == True:
			#self.posi[0]-= self.veloMov
			self.direct[0]-=self.veloMov
		if self.right == True:
			self.direct[0]+=self.veloMov
			#self.posi[0]+= self.veloMov
	def update(self,cam,obj):
		self.rect = pygame.Rect(self.posi[0]+20,self.posi[1],self.larg-40,self.alt-5)
		self.velocidade[1]+=self.gravidade

		
		rect=self.muve(self.rect,self.direct,obj)
		self.posi[0]=rect.left-20
		self.posi[1]=rect.top
		self.contFrameHate+=1
		if(self.contFrameHate==10):
			self.contFrameIdle+=1
			self.contFrameHate=0
		if(self.contFrameIdle==7):
			self.contFrameIdle=0

		self.mover()
	def render(self,screen,cam):
		screen.blit(self.sprite[self.contFrameIdle],(self.posi[0]-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))