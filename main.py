import pygame
import random
import pygame as pg
import asyncio

import math
import json
import time
import copy



class Camera:
	def __init__(self,x,y):
		self.camera = [x,y]
		self.posiFinal =[x,y]
		self.velocidadex=0
		self.velocidadey=0
		self.delay=0.01
		self.maxvelo=1
		self.sacudir=-1
		
	def update(self,novax,novay):
		self.camera[0]+=(novax-self.camera[0]-400)/15
		self.camera[1]+=(novay-self.camera[1]-306)/20
		self.balanga()
	def trigaSacudir(self):
		self.sacudir=20
	def balanga(self):
		
		if(self.sacudir>=0):
			self.sacudir-=1
			if(self.sacudir%4):
			
				self.camera[0]+=(random.random()*20)-10
				self.camera[1]+=(random.random()*20)-10
		
class Rastro:
	def __init__(self,x,y,radial,cor=(150,50,50)):
		self.posi=[x,y]
		self.radial=radial
		self.velo=2
		self.cor=cor
	def update(self):
		self.radial-=self.velo
	def render(self,screen,cam):
		pygame.draw.circle(screen, self.cor, (self.posi[0]-cam.camera[0],self.posi[1]-cam.camera[1]), self.radial)

class Hit:
	def __init__(self,x,y,larg,alt,dano,tempo=1,display=False,tag="none"):
		self.posi=[x,y]
		self.alt=alt
		self.larg=larg
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
		self.tempo=tempo
		self.display=display
		self.podeUsar=True
		self.dano=dano
		self.tag=tag
	def update(self,screen,cam):
		self.tempo-=1
		
	def render(self,screen,cam):
		#pass
		if(self.display):
			
			pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect.left-cam.camera[0],self.rect.top-cam.camera[1],self.rect.width, self.rect.height))

class Coelho:
	def __init__(self,x,y):
		self.direct=[0,0]
		self.posi=[x,y]
		self.alt=70
		self.larg=70		
		self.color=[random.randint(0,50),random.randint(0,20),random.randint(0,50)]
		
		self.sprite=self.carregarSprite('images/coelho_Idle/',7)
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
class ParticulaQueda:
	def __init__(self,x,y,cor=[(200,150,100)],velocidade=1,taxaDiminui=0.3,radial=10):
		self.posi=[x,y]
		self.radial=random.random()*radial+3
		self.velocidade=[(random.random()*2*velocidade)-1*velocidade,(random.random()*2*velocidade)-1*velocidade]
		self.velo=taxaDiminui
		self.cor=random.sample(cor,1)[0]
	def update(self):
		self.radial-=self.velo
		self.posi[0] += self.velocidade[0]
		self.posi[1] += self.velocidade[1]
	def render(self,screen,cam):
		pygame.draw.circle(screen, self.cor, (self.posi[0]-cam.camera[0],self.posi[1]-cam.camera[1]), self.radial)

class Bomba:
	def __init__(self,x,y,forca):
		self.posi=[x,y]
		self.direct=[0,0]
		self.radial=20
		self.alt=self.radial*1.5
		self.larg=self.radial*1.5
		self.rect = pygame.Rect(self.posi[0]-self.larg,self.posi[1]-self.alt,self.larg,self.alt)
		self.veloMov=5
		self.velocidade=forca
		self.gravidade=0.5
		self.move=0
		self.comandoMove=0
		self.chave=0

		self.right = False
		self.left = False
		self.up = False
		self.down = False
		self.rastro=[]

		self.contExplode=100
		self.cor=(100,50,50)
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
				self.velocidade[0]=0
			if movement[0] < 0:
				rect.left = tile.right
				self.velocidade[0]=0
		rect.y += movement[1]
		collisions = self.collision_test(rect,tiles)
		for tile in collisions:
			if movement[1] > 0:
				rect.bottom = tile.top
				if self.velocidade[1]>8:
					logica.criaParticula(15,rect.left+self.larg/2,rect.bottom)
				self.velocidade[1]=0

				self.velocidade[0]+=2
				if(self.velocidade[0]>0):
					self.velocidade[0]=0
			if movement[1] < 0:
				rect.top = tile.bottom
				self.velocidade[1]=0
		return rect
	def mover(self):
		self.direct=[0,0]
		self.direct[1]+=self.velocidade[1]
		self.direct[0]+=self.velocidade[0]
	def explode(self,obj):
		self.radial=-50
		logica.criaParticula(50,self.posi[0]+self.larg/2,self.posi[1]+self.alt/2,cor=[(200,150,50),(150,50,50),(150,150,100)],taxaDiminui=0.2,velocidade=2,radial=10)
		cam.trigaSacudir()
		for i in obj:
			if(i.destroi):
				aux=self.distanciaEU(self.posi[0]+self.larg/2,self.posi[1]+self.alt/2,i.posi[0]+i.larg/2,i.posi[1]+i.alt/2)
			#print(aux)
				
				if(aux<100):
					i.vida-=50
					
					if(str(type(i))== "<class '__main__.Plataforma'>"):
						
						tileMapInte[i.cordenada[0]][i.cordenada[1]]=0

	def distanciaEU(self,x,y,x1,y1):
		return math.sqrt(((x-x1)**2)+((y-y1)**2))
	def update(self,cam,obj):
		self.contExplode-=1
		aux=self.cor[0]
		aux+=1
		self.cor=(aux,aux/3,50)
		if(self.contExplode<=0):
			self.explode(obj)

		self.rastro.append(Rastro(self.posi[0]+self.larg/2,self.posi[1]+self.alt/2,20,cor=self.cor))
		self.comandoMove=0

		#self.posi[0]+=self.velocidade[0]
		#self.posi[1]+=self.velocidade[1]
		
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
		self.velocidade[1]+=self.gravidade

		
		rect=self.muve(self.rect,self.direct,obj)
		self.posi[0]=rect.left
		self.posi[1]=rect.top
		
		
		for i in self.rastro:
			i.update()
			if(i.radial<10):
				self.rastro.remove(i)
		
		#if((self.posi[1]+self.alt)>600 ):
		#	self.posi[1]=600-self.alt
		#	self.velocidade[1]=0
		
		#self.colide(obj)
		self.mover()
	def render(self,screen,cam):
		for i in self.rastro:
			
			i.render(screen,cam)
		pygame.draw.circle(screen, self.cor, (self.posi[0]+self.larg/2-cam.camera[0],self.posi[1]+self.alt/2-cam.camera[1]), self.radial)
		#pygame.draw.rect(screen,(100,150,50), pygame.Rect(self.posi[0]-cam.camera[0], self.posi[1]-cam.camera[1], 2, 2))
class Flecha:
	def __init__(self,x,y,forca):
		self.posi=[x,y]
		self.direct=[0,0]
		self.radial=20/2
		self.alt=30
		self.larg=30
		self.rect = pygame.Rect(self.posi[0]-self.larg,self.posi[1]-self.alt,self.larg,self.alt)
		self.veloMov=5
		self.velocidade=forca
		self.gravidade=0.5
		self.move=0
		self.comandoMove=0
		self.chaveEncosta=False

		self.right = False
		self.left = False
		self.up = False
		self.down = False
		self.rastro=[]

		self.contExplode=100
		self.cor=(100,50,50)
		self.contSprait=0
		self.contTempoVivo=150
		self.frameRate=10
		self.totalSprite=7
		self.img=self.carregarSprite("images/",self.totalSprite,nome='flex')
		
		#self.img[self.contSprait] = pygame.transform.scale(self.img[self.contSprait], (self.larg, self.alt))
		
		self.auximg=self.img[self.contSprait].copy()
		self.angulo=0
	def carregarSprite(self,diretorio,num,nome=''):
		aux=[]
		for i in range(num):
			#print(i)
			aux2=pygame.image.load(diretorio+nome+str(i+1)+'.png')
			
			aux3=pygame.transform.scale(aux2, (self.larg, self.alt))
			
			aux.append(pygame.transform.rotate(aux3, 45))
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
				self.chaveEncosta=True
				self.velocidade[0]=0
				logica.criaParticula(15,rect.right,rect.center[1])
			if movement[0] < 0:
				rect.left = tile.right
				self.chaveEncosta=True
				self.velocidade[0]=0
				logica.criaParticula(15,rect.left,rect.center[1])
		rect.y += movement[1]
		collisions = self.collision_test(rect,tiles)
		for tile in collisions:
			if movement[1] > 0:
				rect.bottom = tile.top
				self.chaveEncosta=True
				
				logica.criaParticula(15,rect.left+self.larg/2,rect.bottom)
				self.velocidade[1]=0

				self.velocidade[0]+=2
				if(self.velocidade[0]>0):
					self.velocidade[0]=0
			if movement[1] < 0:
				self.chaveEncosta=True
				rect.top = tile.bottom
				self.velocidade[1]=0
				logica.criaParticula(15,rect.center[0],rect.top)
		return rect
	def mover(self):
		self.direct=[0,0]
		self.direct[1]+=self.velocidade[1]
		self.direct[0]+=self.velocidade[0]
	def explode(self,obj):
		self.radial=-50
		logica.criaParticula(50,self.posi[0]+self.larg/2,self.posi[1]+self.alt/2,cor=[(200,150,50),(150,50,50),(150,150,100)],taxaDiminui=0.2,velocidade=2,radial=10)
		cam.trigaSacudir()
		for i in obj:
			aux=self.distanciaEU(self.posi[0]+self.larg/2,self.posi[1]+self.alt/2,i.posi[0]+i.larg/2,i.posi[1]+i.alt/2)
			#print(aux)
			

	def distanciaEU(self,x,y,x1,y1):
		return math.sqrt(((x-x1)**2)+((y-y1)**2))
	def setMag(self,seg,mag):
		aux=[]
		aux1=[]
		#mag
		magentude=math.sqrt(seg[0]*seg[0] + seg[1]*seg[1]);
		#normalize
		if(magentude!=0 and magentude!=1):
			for i in seg:
				aux.append(i/magentude)
			
		else:
			aux=seg


		for i in aux:
				aux1.append(i*mag)
		return aux1
	def mult(self,seg,num):
		aux=[]
		for i in seg:
			aux.append(i*num)
		return aux
	def seguir(self, x,  y) :
		angulo=0
		dire = [x , y ];
		#angulo = (math.atan2(dire[1],dire[0]));
		angulo=math.degrees(math.atan2(x,y))
		dire=self.setMag(dire,50)
		dire=self.mult(dire,-1)
		return angulo
	def rot_center(self,image, angle):

		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image

	def angle_trunc(self,a):
		while a < 0.0:
			a += math.pi * 2
		return a

	def getAngleBetweenPoints(self,x_orig, y_orig, x_landmark, y_landmark):
		deltaY = y_landmark - y_orig
		deltaX = x_landmark - x_orig
		return self.angle_trunc(math.atan2(deltaY, deltaX))
	def update(self,cam,obj):
		#self.contExplode-=1
		#aux=self.cor[0]
		#aux+=1
		#self.cor=(aux,aux/3,50)
		#self.auximg=self.rot_center(self.img,math.radians(180))
		if(not self.chaveEncosta):
			self.angulo=self.seguir(self.posi[0]-(self.posi[0]+self.velocidade[0]),self.posi[1]-(self.posi[1]+self.velocidade[1]))
			#angulo=self.getAngleBetweenPoints(self.posi[0],self.posi[0],self.posi[0]+self.velocidade[0],self.posi[1]+self.velocidade[1])
			#print(math.radians(angulo))
			#self.auximg = pygame.transform.rotate(self.img, angulo)
			self.auximg=self.rot_center(self.img[self.contSprait],self.angulo)
			rect=self.muve(self.rect,self.direct,obj)
			self.posi[0]=rect.left-10
			self.posi[1]=rect.top-10
			self.rect = pygame.Rect(self.posi[0]+10,self.posi[1]+10,self.larg-10,self.alt-10)
			self.velocidade[1]+=self.gravidade
		else:
			self.contTempoVivo-=1
		if(self.contTempoVivo<=0):
			if(self.frameRate==0):
				self.frameRate=5
				self.contSprait+=1
				
				if(self.totalSprite-1==self.contSprait):
					self.radial=-5
				else:
					#self.angulo=self.seguir(self.posi[0]-(self.posi[0]+self.velocidade[0]),self.posi[1]-(self.posi[1]+self.velocidade[1]))
					self.auximg=self.rot_center(self.img[self.contSprait],self.angulo)
			self.frameRate-=1

		if(self.contExplode<=0):
			self.explode(obj)

		#self.rastro.append(Rastro(self.posi[0]+self.larg/2,self.posi[1]+self.alt/2,20,cor=self.cor))
		self.comandoMove=0

		#self.posi[0]+=self.velocidade[0]
		#self.posi[1]+=self.velocidade[1]
		
		

		
		
		
		
		for i in self.rastro:
			i.update()
			if(i.radial<10):
				self.rastro.remove(i)
		
		#if((self.posi[1]+self.alt)>600 ):
		#	self.posi[1]=600-self.alt
		#	self.velocidade[1]=0
		
		#self.colide(obj)
		self.mover()
	def render(self,screen,cam):
		for i in self.rastro:
			
			i.render(screen,cam)
		#pygame.draw.circle(screen, self.cor, (self.posi[0]+self.larg/2-cam.camera[0],self.posi[1]+self.alt/2-cam.camera[1]), self.radial)
		screen.blit(self.auximg,(self.posi[0]-cam.camera[0],self.posi[1]-cam.camera[1]))
		#pygame.draw.rect(screen,(100,150,50), pygame.Rect(self.posi[0]-cam.camera[0], self.posi[1]-cam.camera[1], 2, 2))
class Inimigo:

	def __init__(self,x,y):
		self.direct=[0,0]
		self.posi=[x,y]
		self.alt=100
		self.larg=120		
		self.color=[random.randint(0,50),random.randint(0,20),random.randint(0,50)]
		self.destroi=True
		self.chaveMorte=True
		self.sprite=self.carregarSprite('images/coelho_Idle/',7)
		self.iSpriteIdle = pygame.image.load('images/gothicvania patreon collection/Ghost-Files/PNG/ghost-idle.png')
		self.contSpriteIdle=7
		self.imageIdle = self.carregarSpriteSheet('images/gothicvania patreon collection/Ghost-Files/PNG/ghost-idle.png',self.contSpriteIdle,64,80)
		
		self.contSpriteAttak=4
		self.imageAttak = self.carregarSpriteSheet('images/gothicvania patreon collection/Ghost-Files/PNG/ghost-shriek.png',self.contSpriteAttak,64,80)
		self.imageAttak2= self.imageAttak[::-1]
		self.contSpriteMorte=7
		self.imageMorte = self.carregarSpriteSheet('images/gothicvania patreon collection/Ghost-Files/PNG/ghost-vanish.png',self.contSpriteMorte,64,64)
		
		self.paralax=1
		self.contFrameIdle=0
		self.contFrameHate=0
		self.vida=100
		self.morto=False
		self.veloMov=5
		self.velocidade=[0,1]
		self.gravidade=0.5
		self.rect = pygame.Rect(self.posi[0],self.posi[1],5,50)
		self.right = False
		self.left = False
		self.up = False
		self.down = False
		
		self.dir=0
		self.idSprite=1
		self.contSprite=0
		self.contfp=0

		self.sofreuDano=False
		self.contSofreuDano=0
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
	def carregarSpriteSheet(self,diretorio,num,x,y):
		aux=[]
		img = pygame.image.load(diretorio)
		xx=0
		yy=0
		xa=x
		for i in range(num):
		
			aux2=img.subsurface( pygame.Rect(xx,yy,x,y) )
			
			
			aux2=pygame.transform.scale(aux2, (self.alt, self.larg))
			aux.append(aux2)
			xx+=xa
			
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
		
		self.direct[1]+=self.velocidade[1]

		

	def update(self,cam,obj):
		self.rect = pygame.Rect(self.posi[0]+25,self.posi[1]+30,45,80)
		self.velocidade[1]+=self.gravidade

		
		rect=self.muve(self.rect,self.direct,obj)
		self.posi[0]=rect.left-25
		self.posi[1]=rect.top-30
		self.contFrameHate+=1
		

		if(self.contfp>=7):
			self.frameRate()
			self.contfp=0
		self.contfp+=1
		self.mover()
		if(self.contSofreuDano>=0):
			self.sofreuDano=True
		else:
			self.sofreuDano=False
		self.contSofreuDano-=1
		if(self.vida<=0):
			self.idSprite=3
			self.direct=[0,0]
			if(self.chaveMorte):
				if(random.random()<=0.5):
					logica.dropCard.append(DropCarta(self.rect.x,self.rect.y+50,carta=666))
				self.chaveMorte=False
				self.contSprite=0
	def dano(self,dano):
		self.sofreuDano=True
		self.vida-=dano
		self.contSofreuDano=10
	def attak(self):
		self.idSprite=1
		logica.inimigos.append(InimigoCaveira(self.rect.x,self.rect.y))
	def frameRate(self):
		if(self.vida>0):
			if(random.random()<=0.01):
				self.attak()
			if(random.random()<=0.08):
				if(self.dir==0):
					self.dir=1
					self.direct=[0,0]
				else:
					self.dir=0
					self.direct=[0,0]
			if(random.random()<=0.1):
				
				if(self.dir==0):
					self.direct=[-1,0]
					
				if(self.dir==1):
					self.direct=[1,0]
					
			if(random.random()<=0.1):
				
			
				self.direct=[0,0]
					
		self.contSprite+=1
		if(self.idSprite==0):
			
			if(self.contSprite>=self.contSpriteIdle):
				self.contSprite=0
		if(self.idSprite==1):
			if(self.contSprite>=self.contSpriteAttak):
				self.contSprite=0
				self.idSprite=2
		if(self.idSprite==2):
			if(self.contSprite>=self.contSpriteAttak):
				self.contSprite=0
				self.idSprite=0
		if(self.idSprite==3):
			if(self.contSprite>=self.contSpriteMorte):
				self.contSprite=0
				self.morto=True
				
				
		
				
	def renderiza(self,spriteList,cont,condicao=[[0,0],[0,0]]):
		try:
			aux2=spriteList[cont]
			if(self.sofreuDano):
				aux2=self.changColor(aux2,(255,100,100))
			if(self.dir==0):
				screen.blit(aux2, (self.rect.left+condicao[0][0]-25-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(aux2, True, False)
				screen.blit(aux, (self.rect.left+condicao[0][0]-25-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
		except:
			
			self.contSprite=0
			cont=0
			
			if(self.dir==0):
				screen.blit(aux2, (self.rect.left+condicao[0][0]-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(aux2, True, False)
				screen.blit(aux, (self.rect.left+condicao[0][0]-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
	def render(self,screen,cam):
		#screen.blit(self.sprite[self.contFrameIdle],(self.posi[0]-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
		#pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect.left-cam.camera[0],self.rect.top-cam.camera[1],self.rect.width, self.rect.height))
		if(self.idSprite==0):
			
			self.renderiza(self.imageIdle,self.contSprite,condicao=[[0,-30],[0,0]])
		elif(self.idSprite==1):
			self.renderiza(self.imageAttak,self.contSprite,condicao=[[0,-30],[0,0]])
		elif(self.idSprite==2):
			self.renderiza(self.imageAttak2,self.contSprite,condicao=[[0,-30],[0,0]])
		elif(self.idSprite==3):
			self.renderiza(self.imageMorte,self.contSprite,condicao=[[0,-30],[0,-50]])
		#screen.blit(pygame.transform.flip(self.imageIdle[self.contFrameIdle], True, False),(self.posi[0]-25-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
class InimigoCaveira:

	def __init__(self,x,y):
		self.direct=[0,0]
		self.posi=[x,y]
		self.alt=50
		self.larg=55		
		self.color=[random.randint(0,50),random.randint(0,20),random.randint(0,50)]
		self.destroi=True
		self.chaveMorte=True
		self.sprite=self.carregarSprite('images/coelho_Idle/',7)
		self.iSpriteIdle = pygame.image.load('images/gothicvania patreon collection/Ghost-Files/PNG/ghost-idle.png')
		self.contSpriteIdle=8
		self.imageIdle = self.carregarSpriteSheet('images/gothicvania patreon collection/Fire-Skull-Files/PNG/fire-skull.png',self.contSpriteIdle,96,112)
		self.paralax=1
		self.contFrameIdle=0
		self.contFrameHate=0
		self.vida=20
		self.morto=False
		self.veloMov=5
		self.velocidade=[0,1]
		self.gravidade=0.5
		self.rect = pygame.Rect(self.posi[0],self.posi[1],5,50)
		self.right = False
		self.left = False
		self.up = False
		self.down = False
		
		self.dir=1
		self.idSprite=0
		self.contSprite=0
		self.contfp=0

		self.sofreuDano=False
		self.contSofreuDano=0
		self.speed =1
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
	def carregarSpriteSheet(self,diretorio,num,x,y):
		aux=[]
		img = pygame.image.load(diretorio)
		xx=0
		yy=0
		xa=x
		for i in range(num):
		
			aux2=img.subsurface( pygame.Rect(xx,yy,x,y) )
			
			
			aux2=pygame.transform.scale(aux2, (self.alt, self.larg))
			aux.append(aux2)
			xx+=xa
			
		return aux

	def collision_test(self,rect,tiles):
		collisions = []
		for tile in tiles:
			if rect.colliderect(tile.rect):
				collisions.append(tile.rect)
		return collisions
	def muve(self,rect,movement,tiles): # movement = [5,2]
		'''rect.x += movement[0]
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
				self.velocidade[1]=0'''
		return rect
	def mover(self):
		
		self.direct[1]+=self.velocidade[1]

	def move_towards_player(self, player): 
		# find normalized direction vector (dx, dy) between enemy and player 
		dx, dy = player.rect.x-self.rect.x  ,  player.rect.y -self.rect.y 
		dist = math.hypot(dx, dy) 
		dx, dy = dx / dist, dy / dist # move along this normalized vector towards the player at current speed 
		self.rect.x += dx * self.speed 
		self.rect.y += dy * self.speed 
	def movePlay(self, speed,player): 
		# chase movement # Movement along x direction 
		if self.rect.x > player.rect.x: 
			self.rect.x -= speed 
			self.dir=0
		elif self.rect.x < player.rect.x: 
			self.rect.x += speed
			self.dir=1 # Movement along y direction 
		if self.rect.y < player.rect.y: 
			self.rect.y += speed 
		elif self.rect.y > player.rect.y: 
			self.rect.y -= speed 
	def update(self,cam,obj):
		self.rect = pygame.Rect(self.posi[0]-30,self.posi[1],30,30)
		#self.velocidade[1]+=self.gravidade

		#self.move_towards_player(play)
		self.movePlay(1,play)
		rect=self.muve(self.rect,self.direct,obj)
		self.posi[0]=rect.left+30
		self.posi[1]=rect.top
		self.contFrameHate+=1
		

		if(self.contfp>=10):
			self.frameRate()
			self.contfp=0
		self.contfp+=1
		self.mover()
		if(self.contSofreuDano>=0):
			self.sofreuDano=True
		else:
			self.sofreuDano=False
		self.contSofreuDano-=1
		if(self.vida<=0):
			self.idSprite=0
			self.direct=[0,0]
			self.morto=True
			logica.addBomba(self.posi[0]+self.larg/4,self.posi[1]+self.alt/4,self.posi[0]+self.larg/4,self.posi[1]+self.alt/4)
			if(random.random()<=0.5):
				logica.dropCard.append(DropCarta(self.rect.x,self.rect.y,carta=666))
			if(self.chaveMorte):
				logica.criaParticula(50,rect.left,rect.top+self.alt/2,porcentagem=0.15,taxaDiminui=0.2,cor=[(170,80,70),(180,100,90),(170,120,110)])
				self.chaveMorte=False
				self.contSprite=0
	def dano(self,dano):
		self.sofreuDano=True
		self.vida-=dano
		self.contSofreuDano=10
	def attak(self):
		self.idSprite=1
		logica.addBomba(self.posi[0]+self.larg/4,self.posi[1]+self.alt/4,self.posi[0]+self.larg/4,self.posi[1]+self.alt/4)
	def frameRate(self):
	
					
		self.contSprite+=1
		if(self.idSprite==0):
			
			if(self.contSprite>=self.contSpriteIdle):
				self.contSprite=0
		if(self.idSprite==1):
			if(self.contSprite>=self.contSpriteAttak):
				self.contSprite=0
				self.idSprite=2
		if(self.idSprite==2):
			if(self.contSprite>=self.contSpriteAttak):
				self.contSprite=0
				self.idSprite=0
		if(self.idSprite==3):
			if(self.contSprite>=self.contSpriteMorte):
				self.contSprite=0
				self.morto=True
				
				
		
				
	def renderiza(self,spriteList,cont,condicao=[[0,0],[0,0]]):
		try:
			aux2=spriteList[cont]
			if(self.sofreuDano):
				aux2=self.changColor(aux2,(100,255,100))
			if(self.dir==0):
				screen.blit(aux2, (self.rect.left+condicao[0][0]-25-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(aux2, True, False)
				screen.blit(aux, (self.rect.left+condicao[0][0]-25-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
		except:
			
			self.contSprite=0
			cont=0
			
			if(self.dir==0):
				screen.blit(aux2, (self.rect.left+condicao[0][0]-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(aux2, True, False)
				screen.blit(aux, (self.rect.left+condicao[0][0]-cam.camera[0],self.rect.top+condicao[0][1]-cam.camera[1]))
	def render(self,screen,cam):
		#screen.blit(self.sprite[self.contFrameIdle],(self.posi[0]-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
		#pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect.left-cam.camera[0],self.rect.top-cam.camera[1],self.rect.width, self.rect.height))
		if(self.idSprite==0):
			
			self.renderiza(self.imageIdle,self.contSprite,condicao=[[15,-20],[0,0]])
		elif(self.idSprite==1):
			self.renderiza(self.imageAttak,self.contSprite,condicao=[[0,0],[0,0]])
		elif(self.idSprite==2):
			self.renderiza(self.imageAttak2,self.contSprite,condicao=[[0,0],[0,0]])
		elif(self.idSprite==3):
			self.renderiza(self.imageMorte,self.contSprite,condicao=[[0,0],[0,0]])
class InimigoDemonio:

	def __init__(self,x,y):
		self.direct=[0,0]
		self.posi=[x,y]
		self.alt=150
		self.larg=150		
		self.color=[random.randint(0,50),random.randint(0,20),random.randint(0,50)]
		self.destroi=True
		self.chaveMorte=True
		self.sprite=self.carregarSprite('images/coelho_Idle/',7)
		self.iSpriteIdle = pygame.image.load('images/gothicvania patreon collection/Ghost-Files/PNG/ghost-idle.png')
		self.contSpriteIdle=5
		self.imageIdle = self.carregarSpriteSheet('images/gothicvania patreon collection/demon-Files/PNG/demon-idle.png',self.contSpriteIdle,160,144)
		
		self.contSpriteAttak=11
		self.imageAttak = self.carregarSpriteSheet('images/gothicvania patreon collection/demon-Files/PNG/demon-attack.png',self.contSpriteAttak,240,192,scala=[50,50])
		self.imageAttak2= self.imageAttak[::-1]
		self.contSpriteMorte=7
		self.imageMorte = self.carregarSpriteSheet('images/gothicvania patreon collection/Ghost-Files/PNG/ghost-vanish.png',self.contSpriteMorte,64,64)
		
		self.paralax=1
		self.contFrameIdle=0
		self.contFrameHate=0
		self.vida=200
		self.morto=False
		self.veloMov=5
		self.velocidade=[0,1]
		self.gravidade=0.5
		self.rect = pygame.Rect(self.posi[0],self.posi[1],5,50)
		self.rectSprite = pygame.Rect(self.posi[0],self.posi[1],5,50)
		self.sensorDir = pygame.Rect(self.posi[0],self.posi[1],5,50)
		self.sensorEsq = pygame.Rect(self.posi[0],self.posi[1],5,50)
		self.right = False
		self.left = False
		self.up = False
		self.down = False
		
		self.dir=0
		self.idSprite=0
		self.contSprite=0
		self.contfp=0

		self.sofreuDano=False
		self.contSofreuDano=0
		self.timeAttak=0
		self.poder=0.03
		
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
	def carregarSprite(self,diretorio,num,scala=[0,0]):
		aux=[]
		for i in range(num):
			aux2=pygame.image.load(diretorio+str(i+1)+'.png').convert_alpha()
			
			aux2=self.changColor(aux2,(255- self.color[0],255- self.color[1],255-self.color[2]))
			aux.append(pygame.transform.scale(aux2, (self.larg+scala[0], self.alt+scala[1])))
		return aux
	def carregarSpriteSheet(self,diretorio,num,x,y,scala=[0,0]):
		aux=[]
		img = pygame.image.load(diretorio)
		xx=0
		yy=0
		xa=x
		for i in range(num):
		
			aux2=img.subsurface( pygame.Rect(xx,yy,x,y) )
			
			
			aux2=pygame.transform.scale(aux2,  (self.larg+scala[0], self.alt+scala[1]))
			aux.append(aux2)
			xx+=xa
			
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
		
		self.direct[1]+=self.velocidade[1]

		

	def update(self,cam,obj):
		self.rect = pygame.Rect(self.posi[0]+40,self.posi[1]+50,45,80)
		self.rectSprite=pygame.Rect(self.posi[0]+25,self.posi[1]+30,45,80)
		self.velocidade[1]+=self.gravidade

		self.timeAttak+=1
		rect=self.muve(self.rect,self.direct,obj)
		self.posi[0]=rect.left-40
		self.posi[1]=rect.top-50
		self.contFrameHate+=1
		
		self.sensorDir=pygame.Rect(self.posi[0]-50,self.posi[1]+80,80,50)
		self.sensorEsq=pygame.Rect(self.posi[0]+95,self.posi[1]+80,80,50)
		if(self.contfp>=7):
			self.frameRate()
			self.contfp=0


		if((self.idSprite==1 or self.idSprite==2)and self.dir==0):
			self.rectSprite.x-=50
			self.rectSprite.y-=50
		if((self.idSprite==1 or self.idSprite==2)and self.dir==1):
			
			self.rectSprite.y-=50
		if(self.dir==1):
			self.rectSprite.x-=20
		self.contfp+=1
		self.mover()




		if((self.idSprite==1 and self.contSprite>6)and self.dir==0):
			logica.hitPlay.append(Hit(self.rect.x-75,self.rect.y+35,70,40,self.poder,display=False,tag="inimigo",tempo=30))
		if((self.idSprite==1 and self.contSprite>6)and self.dir==1):
			logica.hitPlay.append(Hit(self.rect.x+50,self.rect.y+35,70,40,self.poder,display=False,tag="inimigo",tempo=30))

		if(self.contSofreuDano>=0):
			self.sofreuDano=True
		else:
			self.sofreuDano=False
		self.contSofreuDano-=1
		if(self.vida<=0):
			self.idSprite=3
			self.direct=[0,0]
			if(self.chaveMorte):
				if(random.random()<=0.5):
					logica.dropCard.append(DropCarta(self.rect.x,self.rect.y+50,carta=666))
				self.chaveMorte=False
				self.contSprite=0
	def dano(self,dano):
		self.sofreuDano=True
		self.vida-=dano
		self.contSofreuDano=10
	def attak(self):
		if(self.timeAttak>200):
			self.contSprite=0
			self.idSprite=1
			self.timeAttak=0
			self.direct=[0,0]
	def frameRate(self):
		
		if(self.vida>0):
			if(random.random()<=0.0003):
				self.attak()
			if(random.random()<=0.08 and self.idSprite!=1 and self.idSprite!=2):
				if(self.dir==0):
					self.dir=1
					self.direct=[0,0]
				else:
					self.dir=0
					self.direct=[0,0]
			if(random.random()<=0.01 and self.idSprite!=1 and self.idSprite!=2):
				
				if(self.dir==0):
					self.direct=[-1,0]
					
				if(self.dir==1):
					self.direct=[1,0]
					
			if(random.random()<=0.05):
				
			
				self.direct=[0,0]
		if(play.rect.colliderect(self.sensorDir) and self.idSprite!=1 and self.idSprite!=2):
			self.dir=0
			self.attak()
		elif(play.rect.colliderect(self.sensorEsq)and self.idSprite!=1 and self.idSprite!=2):
			self.dir=1
			self.attak()
				
		self.contSprite+=1
		if(self.idSprite==0):
			
			if(self.contSprite>=self.contSpriteIdle):
				self.contSprite=0
		if(self.idSprite==1):
			if(self.contSprite>=self.contSpriteAttak):
				self.contSprite=0
				self.idSprite=2
		if(self.idSprite==2):
			if(self.contSprite>=self.contSpriteAttak):
				self.contSprite=0
				self.idSprite=0
		
		if(self.idSprite==3):
			if(self.contSprite>=self.contSpriteMorte):
				self.contSprite=0
				self.morto=True
				
				
		
				
	def renderiza(self,spriteList,cont,condicao=[[0,0],[0,0]]):
		try:
			aux2=spriteList[cont]
			if(self.sofreuDano):
				aux2=self.changColor(aux2,(100,100,50))
			if(self.dir==0):
				screen.blit(aux2, (self.rectSprite.left+condicao[0][0]-25-cam.camera[0],self.rectSprite.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(aux2, True, False)
				screen.blit(aux, (self.rectSprite.left+condicao[0][0]-25-cam.camera[0],self.rectSprite.top+condicao[0][1]-cam.camera[1]))
		except:
			
			self.contSprite=0
			cont=0
			
			if(self.dir==0):
				screen.blit(aux2, (self.rectSprite.left+condicao[0][0]-cam.camera[0],self.rectSprite.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(aux2, True, False)
				screen.blit(aux, (self.rectSprite.left+condicao[0][0]-cam.camera[0],self.rectSprite.top+condicao[0][1]-cam.camera[1]))
	def render(self,screen,cam):
		#screen.blit(self.sprite[self.contFrameIdle],(self.posi[0]-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
		#pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect.left-cam.camera[0],self.rect.top-cam.camera[1],self.rect.width, self.rect.height))
		#pygame.draw.rect(screen,(100,150,50), pygame.Rect(self.sensorDir.left-cam.camera[0],self.sensorDir.top-cam.camera[1],self.sensorDir.width, self.sensorDir.height))

		#pygame.draw.rect(screen,(100,150,50), pygame.Rect(self.sensorEsq.left-cam.camera[0],self.sensorEsq.top-cam.camera[1],self.sensorEsq.width, self.sensorEsq.height))
		if(self.idSprite==0):
			
			self.renderiza(self.imageIdle,self.contSprite,condicao=[[0,-30],[0,0]])
		elif(self.idSprite==1):
			self.renderiza(self.imageAttak,self.contSprite,condicao=[[0,-30],[0,0]])
		elif(self.idSprite==2):
			self.renderiza(self.imageAttak2,self.contSprite,condicao=[[0,-30],[0,0]])
		elif(self.idSprite==3):
			self.renderiza(self.imageMorte,self.contSprite,condicao=[[0,-30],[0,-50]])
		
		#screen.blit(pygame.transform.flip(self.imageIdle[self.contFrameIdle], True, False),(self.posi[0]-25-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
class Play:
	def __init__(self,x,y):
		self.posi=[x,y]
		self.direct=[0.5,0]
		self.alt=50
		self.larg=25
		self.rect = pygame.Rect(self.posi[0]+5,self.posi[1],self.larg,self.alt)
		self.rectSprite = pygame.Rect(self.posi[0]-25,self.posi[1]-27,self.larg+78,self.alt+25)
		self.veloMov=5
		self.velocidade=[0,0]
		self.gravidade=0.5
		self.move=0
		self.comandoMove=0
		self.chave=0

		self.right = False
		self.left = False
		self.up = False
		self.down = False

		self.rastro=[]

		self.vida=100
		self.dano=10
		self.modificadorDano=0

		

		self.itemEquipado=1
		self.totalItens=2
		self.tempoAtirar=20
		
		self.contSpriteIdle=6
		self.spritesIdle=self.carregarSprite("images/Individual Sprite/idle/",self.contSpriteIdle,nome='Warrior_Idle_')
		
		self.contSpriteRun=8
		self.spritesRun=self.carregarSprite("images/Individual Sprite/Run/",self.contSpriteRun,nome='Warrior_Run_')
		self.contSpriteFall=3
		self.spritesFall=self.carregarSprite("images/Individual Sprite/Fall/",self.contSpriteFall,nome='Warrior_Fall_')
		self.contSpriteJump=3
		self.spritesJump=self.carregarSprite("images/Individual Sprite/Jump/",self.contSpriteJump,nome='Warrior_Jump_')
		self.contSpriteWall=3
		self.spritesWall=self.carregarSprite("images/Individual Sprite/WallSlide/",self.contSpriteWall,nome='Warrior_WallSlide_')
		self.contSpriteAttack=21
		self.spritesAttack=self.carregarSprite("images/Individual Sprite/Attack/",self.contSpriteAttack,nome='Warrior_Attack_')
		self.contSpriteDash=7
		self.spritesDash=self.carregarSprite("images/Individual Sprite/Dash/",self.contSpriteDash,nome='Warrior_Dash_')
		
		self.contSprite=0
		self.contfp=0
		self.idSprite=0
		self.dir=0
		self.chao=False
		self.attack=0
		self.desh=False
		self.timedesh=0
		self.gatilhoAttak=False
		self.rastroDash=0
		self.dirpassado=0
		self.posipassdo=0

	def attacar(self):
		self.idSprite=5
		if(self.attack==0 and self.idSprite!=1):
			self.attack=1
			self.contSprite=0
			self.contSpriteAttack=8
			self.gatilhoAttak=True
			
		elif(self.attack==1):
			self.attack=2
			self.contSpriteAttack=12
			self.gatilhoAttak=True
		elif(self.attack==2):
			self.attack=3
			self.contSpriteAttack=21
			self.gatilhoAttak=True
		elif(self.attack==3):
			self.attack=1
			self.timedesh=20
			self.gatilhoAttak=True
			
	def carregarSprite(self,diretorio,num,nome=""):
		aux=[]
		for i in range(num):
			aux2=pygame.image.load(diretorio+nome+str(i+1)+'.png').convert_alpha()
			
			#aux2=self.changColor(aux2,(255- self.color[0],255- self.color[1],255-self.color[2]))
			aux.append(pygame.transform.scale(aux2, (self.rectSprite.width, self.rectSprite.height)))
		return aux
	def curar(self,numcura):
		self.vida+=numcura
		logica.criaParticula(50,self.rect.center[0],self.rect.center[1],taxaDiminui=0.2,cor=[(50,100,50),(20,100,60),(70,120,40)])
	def dash(self):
		if(self.timedesh<=0):
		#self.deshdire=self.dire
			self.contSprite=0
			self.idSprite=6
			self.desh=True
			self.timedesh=30
			self.rastroDash=0
			self.dirpassado=self.dir
			self.posipassdo=copy.deepcopy(self.posi)
	def jump(self):
		self.posi[1]-=0.01
		self.velocidade[1]= -10
		self.chao=False
		self.idSprite=3
		self.attack=0
	def ativarItem(self,pos):

		if(self.itemEquipado==1 and self.tempoAtirar<=0):
			logica.addBomba(self.posi[0]+self.larg/4,self.posi[1]+self.alt/4,pos[0]+cam.camera[0],pos[1]+cam.camera[1])
			self.tempoAtirar=20
		if(self.itemEquipado==2 and self.tempoAtirar<=0):
			logica.addFlecha(self.rect.center[0],self.rect.center[1],pos[0]+cam.camera[0],pos[1]+cam.camera[1])
			self.tempoAtirar=20
	def RolarItem(self,dire):
		if(dire=='baixo'):
			self.itemEquipado+=1
			if(self.itemEquipado>self.totalItens):
				self.itemEquipado=1
		if(dire=='cima'):
			self.itemEquipado-=1
			if(self.itemEquipado==0):
				self.itemEquipado=self.totalItens
	def collision_test(self,rect,tiles):
		collisions = []
		for tile in tiles:
			if rect.colliderect(tile.rect):
				collisions.append(tile.rect)
		return collisions
	def muve(self,rect,movement,tiles): # movement = [5,2]
		rect.y += movement[1]
		collisions = self.collision_test(rect,tiles)
		for tile in collisions:
			if movement[1] > 0:
				rect.bottom = tile.top
				if self.velocidade[1]>8:
					logica.criaParticula(15,rect.left+self.larg/2,rect.bottom)
				self.velocidade[1]=0
				self.chao=True
			if movement[1] < 0:
				rect.top = tile.bottom
				self.velocidade[1]=0
				

		rect.x += movement[0]
		collisions = self.collision_test(rect,tiles)
		for tile in collisions:
			if movement[0] > 0:
				if(self.velocidade[1]>1  ):
					#print(self.velocidade[1])
					self.velocidade[1]=1
					self.idSprite=4
					self.attack=0
					logica.criaParticula(1,rect.right,rect.top+self.alt/2,porcentagem=0.15,taxaDiminui=0.4,cor=[(100,80,70),(120,100,90),(140,120,110)])
				rect.right = tile.left
			if movement[0] < 0:
				if(self.velocidade[1]>1):
					#print(self.velocidade[1])
					self.velocidade[1]=1
					self.idSprite=4
					self.attack=0
					logica.criaParticula(1,rect.left,rect.top+self.alt/2,porcentagem=0.15,taxaDiminui=0.4,cor=[(100,80,70),(120,100,90),(140,120,110)])
				rect.left = tile.right
		
		return rect
	def mover(self,dire):
		self.direct=dire
		if(not self.desh):
			self.direct[1]+=self.velocidade[1]
		else:
			self.velocidade[1]=0

			
		if self.left == True:
			#self.posi[0]-= self.veloMov
			self.direct[0]-=self.veloMov
			if(self.chao and self.idSprite!=6):
				self.idSprite=1
				self.attack=0
			self.dir=1
		if self.right == True:
			self.direct[0]+=self.veloMov
			if(self.chao and self.idSprite!=6):
				self.idSprite=1
				self.attack=0
			self.dir=0
			#self.posi[0]+= self.veloMov	
		if(not self.left and not self.right and self.attack==0 and not self.desh and self.velocidade[1]<2 and self.velocidade[1]>-2 ):
			self.idSprite=0
			
	def update(self,cam,obj):
		self.rastro.append(Rastro(self.posi[0]+self.larg/2,self.posi[1]+self.alt/2,25))
		self.comandoMove=0
		self.tempoAtirar-=1
		self.timedesh-=1
		#self.posi[0]+=self.velocidade[0]
		#self.posi[1]+=self.velocidade[1]
		
		self.rect = pygame.Rect(self.posi[0]+5,self.posi[1],self.larg-10,self.alt-5)
		self.rectSprite = pygame.Rect(self.posi[0]-34,self.posi[1]-27,self.larg+78,self.alt+25)
		self.velocidade[1]+=self.gravidade

		
		rect=self.muve(self.rect,self.direct,obj)
		self.posi[0]=rect.left-5
		self.posi[1]=rect.top
		
		if((self.attack==1 or self.attack==2 or self.attack==3) and self.contSprite==5 and self.gatilhoAttak):
			if(self.dir==1):
				logica.hitPlay.append(Hit(self.posi[0]-40,self.posi[1],40,50,self.dano,tag="play"))
			if(self.dir==0):
				logica.hitPlay.append(Hit(self.posi[0]+30,self.posi[1],40,50,self.dano,tag="play"))
			self.gatilhoAttak=False
		if((self.attack==1 or self.attack==2 or self.attack==3 ) and self.contSprite==9 and self.gatilhoAttak):
			if(self.dir==1):
				logica.hitPlay.append(Hit(self.posi[0]-40,self.posi[1],40,50,self.dano,tag="play"))
			if(self.dir==0):
				logica.hitPlay.append(Hit(self.posi[0]+30,self.posi[1],40,50,self.dano,tag="play"))
			self.gatilhoAttak=False
		if((self.attack==1 or self.attack==2 or self.attack==3 ) and self.contSprite==15 and self.gatilhoAttak):
			if(self.dir==1):
				logica.hitPlay.append(Hit(self.posi[0]-40,self.posi[1],40,50,self.dano,tag="play"))
			if(self.dir==0):
				logica.hitPlay.append(Hit(self.posi[0]+30,self.posi[1],40,50,self.dano,tag="play"))
			self.gatilhoAttak=False
			
		for i in self.rastro:
			i.update()
			if(i.radial<10):
				self.rastro.remove(i)
		
		#if((self.posi[1]+self.alt)>600 ):
		#	self.posi[1]=600-self.alt
		#	self.velocidade[1]=0
		
		#self.colide(obj)
		
		
		
		# -------dash --------
		if(self.contSprite<2):
			self.rastroDash+=7
		else:
			self.rastroDash-=7
		if((self.desh and self.contSprite<3) or (self.desh and self.attack==1)):
			if(self.dir==0):
				self.mover([10,0])
			if(self.dir==1):
				self.mover([-10,0])
		else:
			self.desh=False
			self.mover([0,0])
		if(self.velocidade[1]>3 and self.attack==0):
			self.chao=False
			self.idSprite=2
			
			
			#self.contSprite=0
		if(self.contfp>=5):
			self.frameRate()
			self.contfp=0
		self.contfp+=1
		
	def alterIdFp(self,num):
		self.contfp=num
		self.contSprite=0
	def frameRate(self):
		self.contSprite+=1
		if(self.idSprite==2):
			
			if(self.contSprite>=self.contSpriteFall):
				self.contSprite=0
				self.desh=False
		if(self.idSprite==3):
			self.desh=False
			if(self.contSprite>=self.contSpriteJump):
				self.contSprite=0
				self.desh=False
		if(self.idSprite==4):
			self.desh=False
			if(self.contSprite>=self.contSpriteWall):
				self.contSprite=0
				self.desh=False
		if(self.idSprite==5):
			self.desh=False
			if(self.contSprite>=self.contSpriteAttack):
				self.contSprite=0
				self.attack=0
		if(self.idSprite==6):
			if(self.contSprite>=self.contSpriteDash):
				self.contSprite=0
				self.attack=0
				self.desh=False
				self.idSprite=0
				
		if(self.idSprite==0):
			self.desh=False
			if(self.contSprite>=self.contSpriteIdle):
				self.contSprite=0
				
				
		elif(self.idSprite==1):
			if(self.contSprite>=self.contSpriteRun):
				self.contSprite=0
				
		
	def renderiza(self,spriteList,cont,condicao=[[0,0],[0,0]]):
		try:
			
			if(self.dir==0):
				screen.blit(spriteList[cont]  , (self.rectSprite.left+condicao[0][0]-cam.camera[0],self.rectSprite.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(spriteList[cont]  , True, False)
				screen.blit(aux, (self.rectSprite.left-10+condicao[1][0]-cam.camera[0],self.rectSprite.top+condicao[1][1]-cam.camera[1]))

		except:
			
			self.contSprite=0
			cont=0
			
			if(self.dir==0):
				screen.blit(spriteList[cont], (self.rectSprite.left+condicao[0][0]-cam.camera[0],self.rectSprite.top+condicao[0][1]-cam.camera[1]))
			if(self.dir==1):
				aux=pygame.transform.flip(spriteList[cont], True, False)
				screen.blit(aux, (self.rectSprite.left-10+condicao[1][0]-cam.camera[0],self.rectSprite.top+condicao[1][1]-cam.camera[1]))
	def render(self,screen,cam):
		#for i in self.rastro:
			
		#	i.render(screen,cam)
		#pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rectSprite.left-cam.camera[0],self.rectSprite.top-cam.camera[1],self.rectSprite.width, self.rectSprite.height))
		#pygame.draw.rect(screen,(150,50,50), pygame.Rect(self.posi[0]-cam.camera[0], self.posi[1]-cam.camera[1], self.larg, self.alt))
		if(self.desh and self.dir==self.dirpassado and self.posi != self.posipassdo):
			self.renderiza(self.spritesDash,self.contSprite,condicao=[[-self.rastroDash,0],[self.rastroDash,0]])
			self.renderiza(self.spritesDash,self.contSprite,condicao=[[-self.rastroDash/1.5,0],[self.rastroDash/1.5,0]])
			self.renderiza(self.spritesDash,self.contSprite,condicao=[[-self.rastroDash/2,0],[self.rastroDash/2,0]])
			self.renderiza(self.spritesDash,self.contSprite,condicao=[[-self.rastroDash/4,0],[self.rastroDash/4,0]])
		if(self.idSprite==0):
			self.renderiza(self.spritesIdle,self.contSprite)
		elif(self.idSprite==1):
			self.renderiza(self.spritesRun,self.contSprite)
		elif(self.idSprite==2):
			self.renderiza(self.spritesFall,self.contSprite)
		elif(self.idSprite==3):
			self.renderiza(self.spritesJump,self.contSprite)
		elif(self.idSprite==4):
			self.renderiza(self.spritesWall,self.contSprite,condicao=[[10,0],[-10,0]])
		elif(self.idSprite==5):
			self.renderiza(self.spritesAttack,self.contSprite)
		elif(self.idSprite==6):
			self.renderiza(self.spritesDash,self.contSprite)



img = pygame.image.load('images/grass.png')
img_crk = pygame.image.load('images/grass_crk.png')

img1 = pygame.image.load('images/grass1.png')
img_crk1 = pygame.image.load('images/grass1_crk.png')

img2 = pygame.image.load('images/grass2.png')
img_crk2 = pygame.image.load('images/grass2_crk.png')  	

img3 = pygame.image.load('images/grass3.png')
img_crk3 = pygame.image.load('images/grass3_crk.png')

img4 = pygame.image.load('images/grass4.png')
img_crk4 = pygame.image.load('images/grass4_crk.png')

img5 = pygame.image.load('images/grass5.png')
img_crk5 = pygame.image.load('images/grass5_crk.png')

img6 = pygame.image.load('images/grass6.png')
img_crk6 = pygame.image.load('images/grass6_crk.png')

img7 = pygame.image.load('images/grass7.png')
img_crk7 = pygame.image.load('images/grass7_crk.png')

img8 = pygame.image.load('images/grass8.png')
img_crk8 = pygame.image.load('images/grass8_crk.png')
img9 = pygame.image.load('images/grass9.png')
img_crk9 = pygame.image.load('images/grass9_crk.png')
img10 = pygame.image.load('images/grass10.png')
img_crk10 = pygame.image.load('images/grass10_crk.png')


img11 = pygame.image.load('images/grass11.png')
img_crk11 = pygame.image.load('images/grass11_crk.png')
img12 = pygame.image.load('images/grass12.png')
img_crk12 = pygame.image.load('images/grass12_crk.png')
img13 = pygame.image.load('images/grass13.png')
img_crk13 = pygame.image.load('images/grass13_crk.png')

img14 = pygame.image.load('images/grass14.png')
img_crk14 = pygame.image.load('images/grass14_crk.png')

img15 = pygame.image.load('images/grass15.png')
img_crk15 = pygame.image.load('images/grass14_crk.png')
img16 = pygame.image.load('images/grass16.png')
img_crk16 = pygame.image.load('images/grass14_crk.png')
img17 = pygame.image.load('images/grass17.png')
img_crk17 = pygame.image.load('images/grass14_crk.png')
img18 = pygame.image.load('images/grass18.png')
img_crk18 = pygame.image.load('images/grass14_crk.png')

img19 = pygame.image.load('images/grass19.png')
img_crk18 = pygame.image.load('images/grass14_crk.png')
img20 = pygame.image.load('images/grass20.png')
img_crk18 = pygame.image.load('images/grass14_crk.png')
img21 = pygame.image.load('images/grass21.png')
img_crk18 = pygame.image.load('images/grass14_crk.png')
img22 = pygame.image.load('images/grass22.png')
img_crk18 = pygame.image.load('images/grass14_crk.png')
img23 = pygame.image.load('images/grass23.png')
img24 = pygame.image.load('images/grass24.png')
img25 = pygame.image.load('images/grass25.png')
img26 = pygame.image.load('images/grass26.png')

imgdirt = pygame.image.load('images/dirt.png')
imgdirt_crk = pygame.image.load('images/dirt_crk.png')
imgNuvem1 = pygame.image.load('images/background_2.png')
imgNuvem2 = pygame.image.load('images/background_1.png')
class Plataforma:
	def __init__(self,x,y,larg=50,alt=50,cores=(20,100,20),paralax=1,tipo=0,cordenada=[0,0],destroi=True):
		self.posi=[x,y]
		self.alt=alt
		self.larg=larg
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
		self.cor=cores
		self.paralax=paralax
		self.tipo=tipo
		self.cordenada=cordenada
		self.destroi=destroi
		if(tipo==1):
			self.img = pygame.transform.scale(img, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk, (self.larg, self.alt))
		if(tipo==2):
			self.img = pygame.transform.scale(img1, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk1, (self.larg, self.alt))
		if(tipo==3):
			self.img = pygame.transform.scale(img2, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk2, (self.larg, self.alt))
		if(tipo==4):
			self.img = pygame.transform.scale(img3, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk3, (self.larg, self.alt))
		if(tipo==5):
			self.img = pygame.transform.scale(img4, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk4, (self.larg, self.alt))
		if(tipo==6):
			self.img = pygame.transform.scale(img5, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk5, (self.larg, self.alt))
		if(tipo==7):
			self.img = pygame.transform.scale(img6, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk6, (self.larg, self.alt))
		if(tipo==8):
			self.img = pygame.transform.scale(img7, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk7, (self.larg, self.alt))

		if(tipo==9):
			self.img = pygame.transform.scale(imgdirt, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(imgdirt_crk, (self.larg, self.alt))

		if(tipo==10):
			self.img = pygame.transform.scale(img8, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk8, (self.larg, self.alt))
		if(tipo==11):
			self.img = pygame.transform.scale(img9, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk9, (self.larg, self.alt))
		if(tipo==12):
			self.img = pygame.transform.scale(img10, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk10, (self.larg, self.alt))
		if(tipo==13):
			self.img = pygame.transform.scale(img11, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk11, (self.larg, self.alt))
		if(tipo==14):
			self.img = pygame.transform.scale(img12, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk12, (self.larg, self.alt))
		if(tipo==15):
			self.img = pygame.transform.scale(img13, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk13, (self.larg, self.alt))
		if(tipo==16):
			self.img = pygame.transform.scale(img14, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==17):
			self.img = pygame.transform.scale(img15, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==18):
			self.img = pygame.transform.scale(img16, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==19):
			self.img = pygame.transform.scale(img17, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==20):
			self.img = pygame.transform.scale(img18, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))

		if(tipo==21):
			self.img = pygame.transform.scale(img19, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==22):
			self.img = pygame.transform.scale(img20, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==23):
			self.img = pygame.transform.scale(img21, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==24):
			self.img = pygame.transform.scale(img22, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))

		if(tipo==25):
			self.img = pygame.transform.scale(img23, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==26):
			self.img = pygame.transform.scale(img24, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==27):
			self.img = pygame.transform.scale(img25, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))
		if(tipo==28):
			self.img = pygame.transform.scale(img26, (self.larg, self.alt))
			self.img_crk = pygame.transform.scale(img_crk14, (self.larg, self.alt))

		if(tipo==100):
		
			self.img = pygame.transform.scale(imgNuvem1, (self.larg, self.alt))
		if(tipo==101):
			self.img = pygame.transform.scale(imgNuvem2, (self.larg, self.alt))
		
		self.vida=2
	def render(self,screen,cam):
		if(self.tipo==0):
			pygame.draw.rect(screen,self.cor, pygame.Rect(self.posi[0]-cam.camera[0]/self.paralax, self.posi[1]-cam.camera[1]/self.paralax, self.larg, self.alt))
		elif(self.tipo==1 or self.tipo==2 or self.tipo==3 or self.tipo==4 or self.tipo==5 or self.tipo==6 or self.tipo==7 or self.tipo==8 or self.tipo==9 or self.tipo==10 
			or self.tipo==11 or self.tipo==12 or self.tipo==13 or self.tipo==14 or self.tipo==15 or self.tipo==16 or self.tipo==17 or self.tipo==18 or self.tipo==19 or self.tipo==20 
			or self.tipo==21 or self.tipo==22 or self.tipo==23 or self.tipo==24 or self.tipo==25 or self.tipo==26 or self.tipo==27 or self.tipo==28):
			
			
			screen.blit(self.img,(self.posi[0]-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
	
		elif(self.tipo==100):
			screen.blit(self.img,(self.posi[0]-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
		elif(self.tipo==101):
			screen.blit(self.img,(self.posi[0]-cam.camera[0]/self.paralax,self.posi[1]-cam.camera[1]/self.paralax))
			
class Texto:
	def __init__(self,text,x,y,color,tamanho,shadow=[False,(50,50,50),2,2]):
		self.text=text
		self.posi=[x,y]
		self.tam=tamanho
		self.color=color
		self.shadow=shadow
	def render(self,screen,cam):
		fonte=pygame.font.get_default_font()              
		fontesys=pygame.font.Font("images/fontes/BitPotion.ttf", self.tam)   
		if(self.shadow[0]):
			
			txttela = fontesys.render(self.text, False, self.shadow[1])  
			screen.blit(txttela,(self.posi[0]+self.shadow[2],self.posi[1]+self.shadow[3])) 

		txttela = fontesys.render(self.text, False, self.color)  
		screen.blit(txttela,(self.posi[0],self.posi[1])) 
class DropCarta:
	def __init__(self,x,y,carta=666):
		self.posi=[x,y+(random.random()*5)-2.5]
		self.larg=30
		self.alt=30
		self.cor=[(170,80,70),(5,100,20),(150,100,20),(150,50,20),(100,100,150),]
		if(carta==666):
			self.carta=random.randint(0,len(self.cor)-1)
		else:
			self.carta=carta

		
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
		self.pego=False

		self.imgItem = pygame.image.load('images/cardIten.png')
		self.imgItem=pygame.transform.scale(self.imgItem, (self.larg, self.alt))

		self.colidiu=False
		self.maxalt=y+5
		self.minalt=y-5
		self.chaveSobeDece=True
		self.velo=0.2


		self.alpha=0
		self.maxalpha=500
		self.s = pygame.Surface((50,70))  # the size of your rect
		self.s.set_alpha(self.alpha)                # alpha level
		self.s.fill(self.cor[self.carta]) 

		self.rectCard = pygame.Rect(self.posi[0]-10,self.posi[1],50,70)
		self.maxSobe=80
		self.contSobe=60
	def sobeCard(self):
		if(self.alpha<self.maxalpha):
			self.alpha+=10
		if(self.contSobe<self.maxSobe):
			self.contSobe+=1
			self.rectCard = pygame.Rect(self.posi[0]-10,self.posi[1]-self.contSobe,50,70)
	def update(self):
		if(self.chaveSobeDece):
			self.posi[1]+=self.velo
			#print('dddddd')
		else:
			self.posi[1]-=self.velo
		if(self.posi[1]>self.maxalt):
			self.chaveSobeDece=False
		elif(self.posi[1]<self.minalt):
			self.chaveSobeDece=True
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
		
		if(play.rect.colliderect(self.rect)):
			self.colidiu=True
			self.sobeCard()
		else:
			self.colidiu=False
			self.alpha=0
			self.contSobe=60
		self.s.set_alpha(self.alpha) 
	def render(self,screen,cam):
		#pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect.left-cam.camera[0],self.rect.top-cam.camera[1],self.rect.width, self.rect.height))
		screen.blit(self.imgItem,(self.posi[0]-cam.camera[0],self.posi[1]-cam.camera[1]))
		if(self.colidiu):
			#pygame.draw.rect(screen,self.cor[self.carta], pygame.Rect(self.rectCard.left-cam.camera[0],self.rectCard.top-cam.camera[1],self.rectCard.width, self.rectCard.height))
			screen.blit(self.s, (self.rectCard[0]-cam.camera[0],self.rectCard[1]-cam.camera[1]))
class PerguntaHud:
	def __init__(self,hud):
		self.hud=hud

		self.rect=[pygame.Rect(170,280,150,50),pygame.Rect(170,400,150,50),pygame.Rect(470,280,150,50),pygame.Rect(470,400,150,50)]  
		self.textosAtributos=[]
		self.textShow=["45","50","0","91"]
		self.perguntas=["2+2","4+4","5*2","6/2","3+6"]
		self.respostas=["4","8","10","3","9"]
		self.perguntaAtiva=self.perguntas[0]
		self.resposta=''

		self.terminou=False
		self.acertou=True
		self.indexCarta=0
	def escolhePergunta(self):
		self.terminou=False
		self.textShow=[]
		self.textosAtributos=[]
		index=random.randint(0,len(self.perguntas)-1)
		self.perguntaAtiva=self.perguntas[index]
		self.resposta=self.respostas[index]
		self.textShow.append(self.respostas[index])

		while True:
			novo=random.randint(0,len(self.respostas)-1)

			if(self.respostas[novo] not in self.textShow):
				self.textShow.append(self.respostas[novo])
			if(len(self.textShow)==4):
				
				break

		for i in range(15):
			aux=random.randint(0,3)
			aux1=random.randint(0,3)

			aux2=self.textShow[aux]
			self.textShow[aux]=self.textShow[aux1]
			self.textShow[aux1]=aux2

	def verifica(self):
		return False

	def click(self,pos):
		for i in range(len(self.rect)):
			if(self.rect[i].collidepoint(pos)):
				if(self.resposta==self.textShow[i]):
					
					self.acertou=True
					
					logica.deck.usarCarta(self.indexCarta)
				else:
					self.acertou=False
					
				logica.hud.showPergunta=False

	def update(self):
		pass
	def render(self,screen,cam):
		if(logica.hud.showPergunta):
			s = pygame.Surface((500,400))  # the size of your rect
			s.set_alpha(200)                # alpha level
			s.fill((30,30,30))           # this fills the entire surface
			screen.blit(s, (150,100))
			
			
			pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect[0].left,self.rect[0].top,self.rect[0].width, self.rect[0].height))
			pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect[1].left,self.rect[1].top,self.rect[1].width, self.rect[1].height))
			pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect[2].left,self.rect[2].top,self.rect[2].width, self.rect[2].height))
			pygame.draw.rect(screen,(100,50,50), pygame.Rect(self.rect[3].left,self.rect[3].top,self.rect[3].width, self.rect[3].height))


			Texto(self.perguntaAtiva,370,150,(255,255,255),50,shadow=[True,(100,100,100),-2,3]).render(screen,cam)
			for i in range(len(self.rect)):
				self.textosAtributos.append(Texto(self.textShow[i],self.rect[i].left+10,self.rect[i].top,(255,255,255),50,shadow=[True,(100,100,100),-2,3]))
			for i in range(len(self.rect)):
				self.textosAtributos[i].render(screen,cam)
		
class Hud:
	def __init__(self):
		
		self.alt=70
		self.larg=70

		self.posiItem=[50,500]
		self.rectItem = pygame.Rect(self.posiItem[0],self.posiItem[1],self.larg,self.alt)

		self.posiPause=[400-50,300-50]
		self.rectPause = pygame.Rect(self.posiPause[0],self.posiPause[1],self.larg+50,self.alt+50)

		self.imgBomba = pygame.image.load('images/bomba.png')
		self.imgBomba=pygame.transform.scale(self.imgBomba, (self.larg, self.alt))

		self.imgFlecha = pygame.image.load('images/flecha.png')
		self.imgFlecha=pygame.transform.scale(self.imgFlecha, (self.larg, self.alt))

		self.moldura=pygame.image.load('images/moldura.png')
		self.moldura=pygame.transform.scale(self.moldura, (200, 400))

		self.rectSprite = pygame.Rect(50,100,300,200)
		self.contSpriteIdle=6
		self.spritesIdle=self.carregarSprite("images/Individual Sprite/idle/",self.contSpriteIdle,nome='Warrior_Idle_')
		self.contSprite=0
		self.contfp=0
		self.textosAtributos=[]
		self.textosAtributos.append(Texto("Vida: "+str(play.vida),535,50,(255,255,255),50,shadow=[True,(100,100,100),-2,3]))
		
		self.showPergunta=False
		self.pergunta=PerguntaHud(self)
	def perguntado(self,c):
		self.pergunta.escolhePergunta()
		self.pergunta.indexCarta=c
		self.showPergunta=True
		
		#self.pergunta.verifica()
	def carregarSprite(self,diretorio,num,nome=""):
		aux=[]
		for i in range(num):
			aux2=pygame.image.load(diretorio+nome+str(i+1)+'.png').convert_alpha()
			
			#aux2=self.changColor(aux2,(255- self.color[0],255- self.color[1],255-self.color[2]))
			aux.append(pygame.transform.scale(aux2, (self.rectSprite.width, self.rectSprite.height)))
		return aux
	def renderiza(self,spriteList,cont,condicao=[[0,0],[0,0]],dire=0):
		try:
			
			if(dire==0):
				screen.blit(spriteList[cont], (self.rectSprite.left+condicao[0][0],self.rectSprite.top+condicao[0][1]))
			if(dire==1):
				aux=pygame.transform.flip(spriteList[cont], True, False)
				screen.blit(aux, (self.rectSprite.left-10+condicao[1][0],self.rectSprite.top+condicao[1][1]))
		except:
			
			self.contSprite=0
			cont=0
			
			if(dire==0):
				screen.blit(spriteList[cont], (self.rectSprite.left+condicao[0][0],self.rectSprite.top+condicao[0][1]))
			if(dire==1):
				aux=pygame.transform.flip(spriteList[cont], True, False)
				screen.blit(aux, (self.rectSprite.left-10+condicao[1][0],self.rectSprite.top+condicao[1][1]))

	def update(self):
		if(~self.showPergunta):
			if(self.contfp>=5):
				self.frameRate()
				self.contfp=0
			self.contfp+=1
			self.textosAtributos=[]
			self.textosAtributos.append(Texto("Vida: "+str(int(play.vida)),535,50,(255,255,255),50,shadow=[True,(100,100,100),-2,3]))
			self.textosAtributos.append(Texto("Dano: "+str(play.dano),535,100,(255,255,255),50,shadow=[True,(100,100,100),-2,3]))

	def frameRate(self):
		self.contSprite+=1
		
				
		
		if(self.contSprite>=self.contSpriteIdle):
			self.contSprite=0
				
		
	def render(self,screen,cam):
		if(logica.showD):
			s = pygame.Surface((800,600))  # the size of your rect
			s.set_alpha(80)                # alpha level
			s.fill((30,30,30))           # this fills the entire surface
			screen.blit(s, (0,0))
			
			red = (0, 0, 0)
			size = (23, 187, 100, 20)
			surface = pygame.Surface((320, 240))
			surface.set_alpha(150) 
			surface.fill((255,255,255))
			surface.set_colorkey((255,255,255))
			ellipse = pygame.draw.ellipse(surface, red, size)
			
			screen.blit(self.moldura,pygame.Rect(500,25,30,23))
			screen.blit(surface, (100, 100))
			self.renderiza(self.spritesIdle,self.contSprite)
			for i in self.textosAtributos:
				i.render(screen,cam)
		if(play.itemEquipado==1):
			#pygame.draw.rect(screen,(100,150,150), self.rectItem)
			screen.blit(self.imgBomba,self.rectItem)
		elif(play.itemEquipado==2):
			#pygame.draw.rect(screen,(150,100,150), self.rectItem)
			screen.blit(self.imgFlecha,self.rectItem)
		#if(logica.pause):
		#	pygame.draw.rect(screen,(100,150,150), self.rectPause)
		self.pergunta.render(screen,cam)
class Angulo:
	def __init__(self,anguloInicial=0,total_angulo=50,multiplicador=[1,1]):
		self.angle=anguloInicial
		self.total_angulo=total_angulo
		self.angulos=(360/total_angulo)
		self.multiplica=multiplicador
	def step(self):
		self.angle += self.angulos;
		return math.cos(math.radians(self.angle))*self.multiplica[0],math.sin(math.radians(self.angle))*self.multiplica[1]
class Carta:
	def __init__(self,carta):
		self.posi=[100,480]
		self.posiOrigina=self.posi[1]
		self.maxSobe=self.posi[1]-100
		self.larg=130
		self.alt=200
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
		self.cor=[(170,80,70),(5,100,20),(150,100,20),(150,50,20),(50,80,150),]
		
		
		self.color=carta
		#self.color=3
		self.alpha=500
		self.s = pygame.Surface((self.larg,self.alt))  # the size of your rect
		self.s.set_alpha(self.alpha)                # alpha level
		self.s.fill(self.cor[self.color])           # this fills the entire surface
		

		
		self.sob=False
		self.pick=False
		self.time=30
	def setaNew(self):
		self.rect = pygame.Rect(self.posi[0],self.posi[1],self.larg,self.alt)
	def sobe(self):
		self.posi[1]-=15
		if(self.posi[1]<self.maxSobe):
			self.posi[1]=self.maxSobe
	def efeito(self):
		if(self.color==0):
			logica.addBomba(play.rect.left,play.rect.top,play.rect.left,play.rect.top,)
		if(self.color==1):
			play.curar(5)
		if(self.color==2):
			
			ang=Angulo(anguloInicial=-145,total_angulo=50,multiplicador=[150,150])
			for i in range(15):
				rai_x,rai_y=ang.step()
				rai_x += play.posi[0]+(random.random()*40)-20
				rai_y += play.posi[1]+(random.random()*40)-20
				logica.addFlecha(play.rect.left,play.rect.top,rai_x,rai_y)
		if(self.color==3):
			
			ang=Angulo(anguloInicial=-145,total_angulo=50,multiplicador=[190,190])
			for i in range(15):
				rai_x,rai_y=ang.step()
				rai_x += play.posi[0]+(random.random()*40)-20
				rai_y += play.posi[1]+(random.random()*40)-20
				logica.addBomba(play.rect.left,play.rect.top,rai_x,rai_y)
		if(self.color==4):
			play.dano+=5
		
	def dece(self):
		self.posi[1]+=5
		if(self.posi[1]>self.posiOrigina):
			self.posi[1]=self.posiOrigina
	def seleciona(self):
		if(not self.pick):
			self.pick=True
			self.efeito()
	def update(self):
		if(self.pick):
			self.time-=1
			self.posi[1]-=7
			self.alpha-=18
			self.s.set_alpha(self.alpha)
		elif(self.sob):
			self.sobe()
		else:
			self.dece()
	def render(self,screen,cam):
		#pygame.draw.rect(screen,self.cor[self.color], pygame.Rect(self.posi[0], self.posi[1], self.larg, self.alt))
		screen.blit(self.s, (self.posi[0],self.posi[1]))
class Deck:
	def __init__(self):
		self.baralho=[]
		
	def organiza(self):
		for i in range(len(self.baralho)):
			
			self.baralho[i].posi[0]=35+(i*150)
			self.baralho[i].setaNew()
	def addCarta(self,carta=666):
		if(carta==666):
			self.baralho.append(Carta(random.randint(0,4)))
		else:
			self.baralho.append(Carta(carta))
		self.organiza()
	def usarCarta(self,index):
		
		self.baralho[index].seleciona()
		
		
	def update(self):
		for i in self.baralho:
			i.update()
			if(i.time<0):
				self.baralho.remove(i)
	def render(self,screen,cam):
		for i in self.baralho:
			i.render(screen,cam)
class Logica:
	def __init__(self):
		self.pause=False
		self.particulas=[]
		self.hud=Hud()
		self.bombas=[]
		self.flechas=[]
		self.coleho=[]
		self.inimigos=[]
		self.deck=Deck()
		self.deck.addCarta()
		self.deck.addCarta()
		self.deck.addCarta()
		
		
		self.dropCard=[]
		self.dropCard.append(DropCarta(500,300,carta=666))
		self.dropCard.append(DropCarta(580,300,carta=666))
		self.dropCard.append(DropCarta(540,300,carta=666))
		self.dropCard.append(DropCarta(460,300,carta=666))
		self.dropCard.append(DropCarta(300,300,carta=4))		
		

		self.load=True
		self.contLoad=5
		self.showD=False
		self.hitPlay=[]
		global qtdChunk
		global tamChunk
		self.inimigos=[Inimigo(20,-20),InimigoCaveira(-2000,-2000),InimigoDemonio(400,400)]
		#for i in range(10):
		#	self.coleho.append(Coelho(random.randint(10,((qtdChunk*tamChunk*50)-5)),random.randint(10,(qtdChunk*tamChunk*50)-5)))
	def criaParticula(self,num,x,y,cor=[(200,150,100)],velocidade=1,taxaDiminui=0.3,radial=10,porcentagem=1):
		for i in range(num):
			if(random.random()<=porcentagem):
				self.particulas.append(ParticulaQueda(x,y,cor=cor,velocidade=velocidade,taxaDiminui=taxaDiminui,radial=radial))
	def showDeck(self):
		self.showD=not self.showD
		if(not self.pause and self.showD):
			self.pause=True
			self.deck.organiza()
		if( self.pause and not self.showD):
			self.pause=False
			self.hud.showPergunta=False
	def pegarItens(self):
		if(not self.showD):
			for i in self.dropCard:
				if (i.colidiu):
					self.deck.addCarta(carta=i.carta)
					i.pego=True
	def addBomba(self,x,y,x1,y1):
		dx=0
		dy=0
		dx,dy=self.seguir(x1,y1)
		
		self.bombas.append(Bomba(x,y,[(((x)-dx)/25)*-1,(((y)-dy)/20)*-1]))
	def addFlecha(self,x,y,x1,y1):
		dx=0
		dy=0
		dx,dy=self.seguir(x1,y1)
		
		self.flechas.append(Flecha(x,y,[(((x)-dx)/15)*-1,(((y)-dy)/10)*-1]))
	def render(self,screen,cam):
		for i in self.bombas:
			if(i.rect.left>cam.camera[0]-100 and i.rect.right<cam.camera[0]+800+100 and i.rect.bottom<cam.camera[1]+600+100 and i.rect.top>cam.camera[1]-100):
				i.render(screen,cam)
		for i in self.flechas:
			if(i.rect.left>cam.camera[0]-50 and i.rect.right<cam.camera[0]+800+50 and i.rect.bottom<cam.camera[1]+600+50 and i.rect.top>cam.camera[1]-50):
				i.render(screen,cam)
		for i in self.coleho:
			if(i.rect.left>cam.camera[0]-80 and i.rect.right<cam.camera[0]+800+80 and i.rect.bottom<cam.camera[1]+600+80 and i.rect.top>cam.camera[1]-80):
				i.render(screen,cam)
		
		for i in self.hitPlay:
			#if(i.rect.left>cam.camera[0]-80 and i.rect.right<cam.camera[0]+800+80 and i.rect.bottom<cam.camera[1]+600+80 and i.rect.top>cam.camera[1]-80):
			i.render(screen,cam)
		for i in self.inimigos:
			if(i.rect.left>cam.camera[0]-80 and i.rect.right<cam.camera[0]+800+80 and i.rect.bottom<cam.camera[1]+600+80 and i.rect.top>cam.camera[1]-80):
				i.render(screen,cam)
		for i in self.dropCard:
			if(i.rect.left>cam.camera[0]-80 and i.rect.right<cam.camera[0]+800+80 and i.rect.bottom<cam.camera[1]+600+80 and i.rect.top>cam.camera[1]-80):
				i.render(screen,cam)
		for i in self.particulas:
			
			i.render(screen,cam)
		
		self.hud.render(screen,cam)
		
	def update(self,cam,obj):



		self.contLoad-=1
		if(self.contLoad<0):
			self.load=False
		if(not self.pause):
			for i in self.particulas:
				i.update()
				if(i.radial<=0):
					self.particulas.remove(i)
			for i in self.coleho:
				if((i.rect.left>cam.camera[0]-200 and i.rect.right<cam.camera[0]+800+200 and i.rect.bottom<cam.camera[1]+600+200 and i.rect.top>cam.camera[1]-200)or self.load):
					i.update(cam,obj)
					if(i.vida<=0):
						self.coleho.remove(i)
			for i in self.bombas:
				i.update(cam,obj+self.inimigos)
				if(i.radial<0):
					self.bombas.remove(i)
			for i in self.inimigos:
				if((i.rect.left>cam.camera[0]-200 and i.rect.right<cam.camera[0]+800+200 and i.rect.bottom<cam.camera[1]+600+200 and i.rect.top>cam.camera[1]-200)or self.load):
					i.update(cam,obj)
					if(i.morto):
						self.inimigos.remove(i)
			for i in self.flechas:
				i.update(cam,obj)
				if(i.radial<0):
					self.flechas.remove(i)
			for i in self.hitPlay:

				i.update(cam,obj)
				
				if(i.tempo<=0):
					self.hitPlay.remove(i)
				if(i.podeUsar):
					if(i.tag=="inimigo"):
						if(play.rect.colliderect(i.rect)):
							play.vida-=i.dano

					for j in self.inimigos:
						if(i.podeUsar):
							if(i.tag=="play"):
								if(i.rect.colliderect(j.rect)):
								
									j.dano(play.dano)
									#i.podeUsar=False
							
								
			for i in self.dropCard:
				i.update()
				if(i.pego):
					self.dropCard.remove(i)
		
		self.hud.update()
		self.deck.update()
					
	def setMag(self,seg,mag):
		aux=[]
		aux1=[]
		#mag
		magentude=math.sqrt(seg[0]*seg[0] + seg[1]*seg[1]);
		#normalize
		if(magentude!=0 and magentude!=1):
			for i in seg:
				aux.append(i/magentude)
			
		else:
			aux=seg


		for i in aux:
				aux1.append(i*mag)
		return aux1
	def mult(self,seg,num):
		aux=[]
		for i in seg:
			aux.append(i*num)
		return aux
	def seguir(self, x,  y) :
		angulo=0
		dire = [x - play.posi[0]-cam.camera[0], y - play.posi[1]-cam.camera[1]];
		angulo = (math.atan2(dire[1],dire[0]));

		dire=self.setMag(dire,50)
		dire=self.mult(dire,-1)
		#print(dire)
		#print([x,y])
		a=[x+dire[0],y+dire[1]]
		return a[0],a[1]
		#print(self.a)
		#print(self.angulo);
pygame.init()	
screen = pygame.display.set_mode((800, 600), 0, 32)
font = pg.font.Font(None, 30)

clock = pygame.time.Clock()




tileMap=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1,1,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,9,9,9,9,5,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,9,9,9,9,5,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,9,9,9,9,5,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,7,7,7,7,6,13,0,16,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,10,11,11,11,12,0,0,0,0,0,0,0,0,0,14,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]]

tileMapInte=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]

tilePlat=[]
def criaMapa(mapa):
	aux=[]
	for i in range(len(mapa)):
		for j in range(len(mapa[0])):	
			if(mapa[i][j]!=0):
				aux.append(Plataforma(j*50,i*50,tipo=mapa[i][j]))
			
	return aux

def criarMapaInteligente(mapa,inix=0,iniy=0,finx=0,finy=0,borda=False):
	aux=[]
	
	for ii in range(finx):
		for jj in range(finy):
			i=ii+inix
			j=jj+iniy
			#print(i,j)
			if(borda):
				if(ii==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=11,destroi=False))
				if(ii==finx-1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=11,destroi=False))
				if(jj==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=14,destroi=False))
				if(jj==finy-1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=14,destroi=False))
			if(mapa[i][j]==1):
				
				
					
				if(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==1 and mapa[i+1][j-1]==1 and mapa[i+1][j+1]==1 and mapa[i-1][j+1]==0 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=20))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==0 and mapa[i+1][j-1]==1 and mapa[i+1][j+1]==1 and mapa[i-1][j+1]==1 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=19))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==1 and mapa[i+1][j-1]==0 and mapa[i+1][j+1]==1 and mapa[i-1][j+1]==1 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=18))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==1 and mapa[i+1][j-1]==1 and mapa[i+1][j+1]==0 and mapa[i-1][j+1]==1 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=17))

				elif(mapa[i-1][j]==0 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==1 and mapa[i+1][j-1]==1 and mapa[i+1][j+1]==0 and mapa[i-1][j+1]==0 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=22))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==0 and mapa[i+1][j-1]==0 and mapa[i+1][j+1]==1 and mapa[i-1][j+1]==1 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=21))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==0 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==1 and mapa[i+1][j-1]==1 and mapa[i+1][j+1]==0 and mapa[i-1][j+1]==0 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=23))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==0 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==0 and mapa[i+1][j-1]==0 and mapa[i+1][j+1]==1 and mapa[i-1][j+1]==1 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=24))

				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==0 and mapa[i+1][j-1]==1 and mapa[i+1][j+1]==1 and mapa[i-1][j+1]==0 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=25))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==1 and mapa[i+1][j-1]==0 and mapa[i+1][j+1]==0 and mapa[i-1][j+1]==1 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=26))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==1 and mapa[i+1][j-1]==1 and mapa[i+1][j+1]==0 and mapa[i-1][j+1]==0 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=28))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1 and mapa[i-1][j-1]==0 and mapa[i+1][j-1]==0 and mapa[i+1][j+1]==1 and mapa[i-1][j+1]==1 ):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=27))
				
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=9))
				
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==0 and mapa[i][j+1]==0 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=15))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==0 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=14))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==1 and mapa[i][j+1]==0 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=13))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==0 and mapa[i][j+1]==0 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=12))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==0 and mapa[i][j+1]==1 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=11))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==0 and mapa[i][j+1]==1 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=10))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=3))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==1 and mapa[i][j+1]==0 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=2))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==0 and mapa[i][j+1]==0 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=6))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==0 and mapa[i][j+1]==1 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=8))

				elif(mapa[i-1][j]==0 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=1))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==0 and mapa[i][j+1]==1 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=7))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==1 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=4))
				elif(mapa[i-1][j]==1 and mapa[i+1][j]==1 and mapa[i][j+1]==0 and mapa[i][j-1]==1):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=5))
				elif(mapa[i-1][j]==0 and mapa[i+1][j]==0 and mapa[i][j+1]==0 and mapa[i][j-1]==0):
					aux.append(Plataforma(j*50,i*50,cordenada=[i,j],tipo=16))
			if(mapa[i][j]==2):
				
				logica.coleho.append(Coelho(j*50,i*50))
				mapa[i][j]=0
			if(mapa[i][j]==3):
				
				logica.inimigos.append(Inimigo(j*50,i*50))
				mapa[i][j]=0
			if(mapa[i][j]==4):
				
				logica.inimigos.append(InimigoDemonio(j*50,i*50))
				mapa[i][j]=0
	return aux

plat=[]
tileset=[]
tamChunk=10
qtdChunk=5

cam=Camera(0,0)
play=Play(100,100)
logica=Logica()
tam=qtdChunk*tamChunk+2

chunk1=[[1,1,1,1,1,0,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,1,1,1,0,1],
        [1,0,3,0,0,0,0,0,1,1],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,0,0],
		[1,0,0,2,0,0,0,0,0,1],
		[1,0,0,0,0,0,0,2,0,1],
		[1,0,0,0,0,0,0,0,0,1],
		[1,1,1,1,0,0,1,1,1,1],]

chunk2=[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0],
		[0,1,0,4,0,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,0,0],
		[0,0,0,0,0,1,1,1,0,0],
		[0,0,0,0,0,1,1,1,0,0],
		[0,0,1,1,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],]

chunk3=[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0],
		[0,1,1,0,0,0,2,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,1,1,1,1,1,0],
		[0,0,0,0,1,1,1,1,1,0],
		[0,0,0,0,1,1,1,1,1,0],
		[0,0,0,0,0,0,0,0,0,0],]

chunk4=[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,0,0,0],
		[0,0,0,1,1,1,1,0,0,0],
		[0,0,0,1,1,1,1,1,1,1],
		[0,0,0,0,0,0,0,0,0,0],
		[1,1,0,0,0,0,0,0,0,0],
		[1,1,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,1,1,1,1],]
chunk7=[[0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,1,0,0,1,1],
        [0,0,0,0,0,1,1,0,1,1],
		[0,0,0,1,1,1,1,1,1,1],
		[0,0,0,1,1,1,1,1,1,1],
		[0,0,0,0,0,0,0,0,0,0],
		[1,1,0,0,0,0,0,0,0,0],
		[1,1,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,1,1,1,1],]

chunk8=[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,1],
		[1,1,1,0,0,0,0,0,0,0],
		[0,0,1,0,0,0,0,1,1,1],
		[1,1,1,0,0,0,0,0,0,0],
		[1,0,0,0,0,0,0,0,0,0],
		[1,0,0,0,1,1,0,0,1,1],
		[1,0,0,0,0,0,0,0,0,0],]

chunk9=[[1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,1,1],
		[0,0,1,0,0,0,0,0,0,0],
		[0,0,1,0,0,0,0,1,0,0],
		[1,0,1,0,0,0,0,0,1,1],
		[1,0,0,0,0,0,4,0,0,1],
		[1,0,0,0,0,0,0,0,0,1],
		[1,1,1,1,0,0,1,1,1,1],]
chunk11=[[1,1,1,1,0,0,1,1,1,1],
        [1,1,1,1,0,0,1,1,1,1],
        [1,1,0,0,0,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,1,1],
		[0,0,1,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,0,0],
		[1,1,0,0,0,0,0,0,1,1],
		[1,1,0,0,0,0,0,0,0,1],
		[1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1],]
chunk12=[[0,1,1,1,0,0,1,1,1,1],
        [1,1,1,1,0,0,1,1,1,1],
        [1,1,0,0,0,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,1,1],
		[0,0,0,0,1,1,0,0,0,0],
		[0,0,0,0,1,1,0,0,0,0],
		[1,1,0,0,0,0,0,0,0,1],
		[1,1,0,0,0,0,0,0,0,1],
		[1,0,1,0,0,0,0,1,1,1],
		[0,1,1,1,0,0,1,1,1,1],]


chunk5=[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,0,0],
		[0,0,0,0,0,0,0,1,1,0],
		[0,0,0,1,1,0,1,1,1,0],
		[1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,0,1,1,1],]
chunk10=[[0,0,0,0,1,0,0,0,1,0],
        [0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,1,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,1,1,1,1,1,1,1,0,0],
		[1,1,1,1,1,1,1,1,1,1],
		[1,1,1,0,1,1,1,1,1,1],
		[1,1,1,1,1,1,0,0,1,1],
		[1,1,1,1,1,0,0,1,1,1],]
chunk6=[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1,1,1],]
chunk50=[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],]
def addChunk(mat,chunk,x,y):
	for i in range(tamChunk):
		for j in range(tamChunk):
			#print(mat[i+x][j+y])
			if(chunk[i][j]==1):
				mat[i+x][j+y]=chunk[i][j]
			if(chunk[i][j]==2):
				mat[i+x][j+y]=chunk[i][j]
			if(chunk[i][j]==3):
				mat[i+x][j+y]=chunk[i][j]
			if(chunk[i][j]==4):
				mat[i+x][j+y]=chunk[i][j]
	return mat
def gera(tileset):
	
	for i in range(int((tam-2)/tamChunk)):
		for j in range(int((tam-2)/tamChunk)):
			#print(j)
			

			
			if(i>=0):
				a=random.randint(0,1)
				if(a==0):
					tileset=addChunk(tileset,chunk1,1+i*tamChunk,1+j*tamChunk)
				if(a==1):
					tileset=addChunk(tileset,chunk2,1+i*tamChunk,1+j*tamChunk)
			if(i==1):
				a=random.randint(0,2)
				if(a==0):
					tileset=addChunk(tileset,chunk1,1+i*tamChunk,1+j*tamChunk)
				if(a==1):
					tileset=addChunk(tileset,chunk2,1+i*tamChunk,1+j*tamChunk)
				if(a==2):
					tileset=addChunk(tileset,chunk3,1+i*tamChunk,1+j*tamChunk)
			if(i==2):
				a=random.randint(0,2)
				if(a==0):
					tileset=addChunk(tileset,chunk2,1+i*tamChunk,1+j*tamChunk)
				if(a==1):
					tileset=addChunk(tileset,chunk3,1+i*tamChunk,1+j*tamChunk)
				if(a==2):
					tileset=addChunk(tileset,chunk4,1+i*tamChunk,1+j*tamChunk)
				
			if(i>=3):
				a=random.randint(0,3)
				if(a==0):
					tileset=addChunk(tileset,chunk3,1+i*tamChunk,1+j*tamChunk)
				if(a==1):
					tileset=addChunk(tileset,chunk4,1+i*tamChunk,1+j*tamChunk)
				if(a==2):
					tileset=addChunk(tileset,chunk7,1+i*tamChunk,1+j*tamChunk)
				if(a==3):
					tileset=addChunk(tileset,chunk9,1+i*tamChunk,1+j*tamChunk)
			if(i>=4):
				a=random.randint(0,3)
				
				if(a==0):
					tileset=addChunk(tileset,chunk8,1+i*tamChunk,1+j*tamChunk)
				if(a==1):
					
					tileset=addChunk(tileset,chunk9,1+i*tamChunk,1+j*tamChunk)
				if(a==2):
				
					tileset=addChunk(tileset,chunk11,1+i*tamChunk,1+j*tamChunk)
				if(a==3):
					
					tileset=addChunk(tileset,chunk12,1+i*tamChunk,1+j*tamChunk)
			
				
				
			'''
			if(a==6):
				tileset=addChunk(tileset,chunk9,1+i*tamChunk,1+j*tamChunk)
			if(a==7):
				tileset=addChunk(tileset,chunk10,1+i*tamChunk,1+j*tamChunk)
			if(a==8):
				tileset=addChunk(tileset,chunk11,1+i*tamChunk,1+j*tamChunk)
				'''
			if((1+i*tamChunk)==tam-tamChunk-1):
				a=random.randint(0,2)
				if(a==0):
					tileset=addChunk(tileset,chunk5,1+i*tamChunk,1+j*tamChunk)
				if(a==1):
					tileset=addChunk(tileset,chunk6,1+i*tamChunk,1+j*tamChunk)
				if(a==2):
					tileset=addChunk(tileset,chunk10,1+i*tamChunk,1+j*tamChunk)
	return tileset


def cria():
	global plat
	global tileMapInte
	plat=[]
	tileMapInte=[]
	for i in range(tam):
		aux=[]
		for j in range(tam):
			aux.append(0)

		tileMapInte.append(aux)

	tileMapInte=gera(tileMapInte)
	plat=criarMapaInteligente(tileMapInte,finx=tam,finy=tam,borda=True)

def remove_repetidos(lista):
	l = []
	for i in range(len(lista)-1,-1,-1):
		cont=True
		for j in l:
			if lista[i].cordenada  == j.cordenada:
				cont=False
		if(cont):
			
			l.append(lista[i])
	
	return l
cria()
'''
plat=[Plataforma(200,400,tipo=1),Plataforma(150,500,tipo=1),Plataforma(400,540,tipo=1),Plataforma(410,530,tipo=1),Plataforma(420,520,tipo=1),Plataforma(430,510,tipo=1),Plataforma(440,500,tipo=1)]
for i in range(40):
	plat.append(Plataforma(i*50+10,550,tipo=1))
for i in range(40):
	plat.append(Plataforma(i*50+10,600,tipo=2))
for i in range(40):
	plat.append(Plataforma(i*50+10,650,tipo=2))
for i in range(40):
	plat.append(Plataforma(i*50+10,700,tipo=2))
for i in range(40):
	plat.append(Plataforma(i*50+10,750,tipo=2))
for i in range(6):
	plat.append(Plataforma(i*50+330,200,tipo=1))
	'''
paralax=[Plataforma(100,350,alt=500,larg=400,cores=(52,53,95),paralax=2,tipo=0),Plataforma(500,300,alt=500,larg=300,cores=(52,53,95),paralax=2,tipo=0),Plataforma(1000,400,alt=500,larg=300,cores=(52,53,95),paralax=2,tipo=0),
Plataforma(-800,550,alt=500,larg=2400,cores=(52,53,95),paralax=2,tipo=0)]
paralax2=[Plataforma(-100,100,alt=500,larg=800,cores=(46,90,137),paralax=3,tipo=0),Plataforma(400,200,alt=500,larg=800,cores=(46,90,137),paralax=3,tipo=0),
Plataforma(-800,450,alt=500,larg=2400,cores=(46,90,137),paralax=3,tipo=0)]
redesenhaPlat=[]
def render(screen):
		global plat
		global tileMapInte
		global redesenhaPlat
		for i in paralax2:
			i.render(screen,cam)
		for i in paralax:
			i.render(screen,cam)
		
		play.render(screen,cam)
		
		redesenhaPlat=[]
		for i in plat:
			if(i.rect.left>cam.camera[0]-50 and i.rect.right<cam.camera[0]+800+50 and i.rect.bottom<cam.camera[1]+600+50 and i.rect.top>cam.camera[1]-50):
				i.render(screen,cam)
			if(i.vida<=0):
				logica.criaParticula(10,i.posi[0]+i.larg/2,i.posi[1]+i.alt/2,cor=[(120,60,50)])
				#tileMapInte[i.cordenada[0]][i.cordenada[1]]=0
				#print(tileMapInte[i.cordenada[0]][i.cordenada[1]])
				plat.remove(i)
				chunky=int(i.cordenada[0]/tamChunk)
				chunkx=int(i.cordenada[1]/tamChunk)
				redesenhaPlat.append([chunkx,chunky])
				#print((chunky)*tamChunk,(chunkx)*tamChunk)
		logica.render(screen,cam)
		for i in range(len(redesenhaPlat)):
			#print(i)
			aux=criarMapaInteligente(tileMapInte,inix=(redesenhaPlat[i][1]*tamChunk),iniy=(redesenhaPlat[i][0]*tamChunk),finx=tamChunk,finy=tamChunk)
			#print('f')
			#aux=[]
			for j in aux:
				plat.append(j)
			if(i==len(redesenhaPlat)-1):
				#print('rr')
				plat=remove_repetidos(plat)
			
		
		if(logica.showD):
			logica.deck.render(screen,cam)
		logica.hud.render(screen,cam)
def update():
	if(not logica.pause):

		play.update(cam,plat)

	cam.update(play.posi[0],play.posi[1])
	logica.update(cam,plat)
dx=0
dy=0
angulo=0
async def main():
    
	done = False
	while not done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				if (event.type == pygame.MOUSEBUTTONDOWN):
					if event.button == 4:
						play.RolarItem('cima')
					elif event.button == 5:
						
						play.RolarItem('baixo')
				
				if(logica.showD):

					pos = pygame.mouse.get_pos()
					
					for c,i in enumerate(logica.deck.baralho):
						if(i.rect.collidepoint(pos)):
							i.sob=True
							if(pygame.mouse.get_pressed()[0]):
								logica.hud.perguntado(c)
								
						else:
							i.sob=False
				if ( pygame.mouse.get_pressed()[0]):
					pos = pygame.mouse.get_pos()
					if(logica.hud.showPergunta):
						logica.hud.pergunta.click(pos)
					#play.ativarItem(pos)
					if(not logica.showD):
						play.attacar()
					
				if event.type == pygame.KEYDOWN:
					#print(event)
					#Q-abrir baralho
					if event.scancode == 20:
						logica.showDeck()
						#logica.addBomba(play.posi[0],play.posi[1],[(((play.posi[0]-cam.camera[0])-dx)/20)*-1,(((play.posi[1]-cam.camera[1])-dy)/20)*-1])
					if event.scancode == 44:
						play.dash()
						#logica.pause=not logica.pause
						#print(logica.pause)
					if event.scancode == 7:
						#play.move=2
						play.right = True
					if event.scancode == 4:
						#play.move=1
						play.left = True
					if event.scancode == 26:
						
						play.jump()
					#E - pegar itens
					if event.scancode == 8:
						logica.pegarItens()
					#i - iventario
					if event.scancode == 12:
						pass
				if event.type == pygame.KEYUP:
					if event.scancode == 7:
						play.right = False
						play.contSprite=0
					if event.scancode == 4:
						play.left = False
						play.contSprite=0

			#pygame.draw.rect(screen,(100,150,50), pygame.Rect(dx, dy, 25, 25))
			pygame.display.flip()
			clock.tick(60)
			screen.fill((150,190,190))

			render(screen)
			update()
			fps = font.render("fps: "+str(int(clock.get_fps())), True, pg.Color('white'))
			screen.blit(fps, (50, 50))
			await asyncio.sleep(0)
asyncio.run(main())

			  
				