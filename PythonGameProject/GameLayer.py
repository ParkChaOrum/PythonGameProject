# -*- coding: cp949 -*-
from typing import Callable
from OrumMiniEngine import *
import pygame

class Player:
    def __init__(self):
        self.gameObject = GameObject(mainScene, tag="Player")
        self.transform = Transform(self.gameObject, centerPos)
        self.gameObject.AddComponent(self.transform)
        self.renderer = Renderer(self.transform)
        self.gameObject.AddComponent(self.renderer)
        self.animController = AnimationController(self.renderer)
        self.gameObject.AddComponent(self.animController)
        leftIdleAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_idle_anim.gif', 10, Image.FLIP_LEFT_RIGHT)
        rightIdleAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_idle_anim.gif', 10)
        leftRunAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_run_anim.gif', 5, Image.FLIP_LEFT_RIGHT)
        rightRunAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_run_anim.gif', 5)
        leftJumpAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_jump_1up_anim.gif', 10, Image.FLIP_LEFT_RIGHT)
        rightJumpAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_jump_1up_anim.gif', 10)
        leftFallAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_jump_3down_anim.gif', 5, Image.FLIP_LEFT_RIGHT)
        rightFallAnim = Animation(self.animController, 'Sprites\\spr_m_traveler_jump_3down_anim.gif', 5)
        self.animController.AddAnim('leftIdle', leftIdleAnim)
        self.animController.AddAnim('rightIdle', rightIdleAnim)
        self.animController.AddAnim('leftRun', leftRunAnim)
        self.animController.AddAnim('rightRun', rightRunAnim)
        self.animController.AddAnim('leftJump', leftJumpAnim)
        self.animController.AddAnim('rightJump', rightJumpAnim)
        self.animController.AddAnim('leftFall', leftFallAnim)
        self.animController.AddAnim('rightFall', rightFallAnim)
        self.collider = Collider(self.transform, 15, 15, 28, 32, showRect=False, collisionStayFunc=PlayerCollision)
        self.gameObject.AddComponent(self.collider)
        self.physics = Physics(self.collider, 1, 20, horizontalFriction=1 ,jumpCount=2)
        self.gameObject.AddComponent(self.physics)
        mainScene.AddGameObject(self.gameObject)

class FlyingCreature:
    def __init__(self, position:Vector2D, cycle: int = 150):
        self.gameObject = GameObject(mainScene, tag="Creature")
        self.transform = Transform(self.gameObject, position)
        self.gameObject.AddComponent(self.transform)
        self.renderer = Renderer(self.transform)
        self.gameObject.AddComponent(self.renderer)
        self.animController = AnimationController(self.renderer)
        self.gameObject.AddComponent(self.animController)
        leftAnim = Animation(self.animController, 'Sprites\\spr_toucan_fly_anim.gif', 10, Image.FLIP_LEFT_RIGHT)
        rightAnim = Animation(self.animController, 'Sprites\\spr_toucan_fly_anim.gif', 10)
        self.animController.AddAnim('left', leftAnim)
        self.animController.AddAnim('right', rightAnim)
        self.damageToPlayerCollider = Collider(self.transform, 25, 20, 15, 15, showRect=False, onlyForTrigger=True, colliderTag="DamageToPlayer")
        self.killCollider = Collider(self.transform, 25, 20, 20, -15, showRect=False, onlyForTrigger=True, collisionStayFunc=Kill)
        self.gameObject.AddComponent(self.damageToPlayerCollider)
        self.gameObject.AddComponent(self.killCollider)
        self.flipTick = Tick(cycle)
        self.left = True
        mainScene.AddGameObject(self.gameObject)
    def Move(self):
        if self.flipTick.Trigger():
            if self.left:
                self.left = False
                self.animController.Play("right")
            else:
                self.left = True
                self.animController.Play("left")
        if self.left:
            self.transform.Move(Vector2D(-1,0))
        else:
            self.transform.Move(Vector2D(1,0))

class WalkingCreature:
    def __init__(self, position:Vector2D, cycle: int = 200):
        self.gameObject = GameObject(mainScene, tag="Creature")
        self.transform = Transform(self.gameObject, position)
        self.gameObject.AddComponent(self.transform)
        self.renderer = Renderer(self.transform)
        self.gameObject.AddComponent(self.renderer)
        self.animController = AnimationController(self.renderer)
        self.gameObject.AddComponent(self.animController)
        leftAnim = Animation(self.animController, 'Sprites\\spr_skeleton_walk_anim.gif', 10, Image.FLIP_LEFT_RIGHT)
        rightAnim = Animation(self.animController, 'Sprites\\spr_skeleton_walk_anim.gif', 10)
        self.animController.AddAnim('left', leftAnim)
        self.animController.AddAnim('right', rightAnim)
        self.damageToPlayerCollider = Collider(self.transform, 30, 25, 20, 35, showRect=False, onlyForTrigger=True, colliderTag="DamageToPlayer", rectColor="green")
        self.physicsCollider = Collider(self.transform, 25, 20, 20, 35, showRect=False, onlyForTrigger=False, rectColor="red")
        self.killCollider = Collider(self.transform, 25, 20, 25, -20, showRect=False, onlyForTrigger=True, collisionStayFunc=Kill)
        self.gameObject.AddComponent(self.damageToPlayerCollider)
        self.gameObject.AddComponent(self.killCollider)
        self.gameObject.AddComponent(self.physicsCollider)
        self.physics = Physics(self.physicsCollider, 1, 20, horizontalFriction=1 ,jumpCount=2)
        self.gameObject.AddComponent(self.physics)
        self.flipTick = Tick(cycle)
        self.left = True
        mainScene.AddGameObject(self.gameObject)
    def Move(self):
        if self.flipTick.Trigger():
            if self.left:
                self.left = False
                self.animController.Play("right")
            else:
                self.left = True
                self.animController.Play("left")
        if self.left:
            self.transform.Move(Vector2D(-1,0))
        else:
            self.transform.Move(Vector2D(1,0))
        
def Kill(me: Collider, other: Collider):
    if other.GetGameObject().GetTag() == "Player":
        creatureSoundChannel.play(creatureDeathSound)
        me.GetGameObject().Destroy()

def PlayerCollision(me: Collider, other: Collider):
    if other.GetColliderTag() == "DamageToPlayer":
        print("Damaged")

class Block:
    def __init__(self, position:Vector2D, size: Vector2D, source:str = "Sprites\\ground0.png"):
        self.gameObject = GameObject(mainScene)
        self.transform = Transform(self.gameObject, position)
        self.gameObject.AddComponent(self.transform)
        img = Image.open(source)
        self.renderer = Renderer(self.transform, img.resize((size.x, size.y)))
        self.gameObject.AddComponent(self.renderer)
        self.collider = Collider(self.transform, size.x/2, size.x/2, size.y/2, size.y/2, showRect=False)
        self.gameObject.AddComponent(self.collider)
        mainScene.AddGameObject(self.gameObject)

class Background:
    def __init__(self,img:Image.Image, position:Vector2D, size: Vector2D):
        self.gameObject = GameObject(mainScene)
        self.transform = Transform(self.gameObject, position)
        self.gameObject.AddComponent(self.transform)
        self.renderer = Renderer(self.transform, img.resize((size.x, size.y)))
        self.gameObject.AddComponent(self.renderer)
        mainScene.AddGameObject(self.gameObject)

class ColliderBlock:
    def __init__(self, position:Vector2D, size: Vector2D, collisionStayFunc: Callable[[Collider, Collider],None] ,onlyForTrigger:bool=True,showRect:bool=False):
        self.gameObject = GameObject(mainScene)
        self.transform = Transform(self.gameObject, position)
        self.gameObject.AddComponent(self.transform)
        self.collider = Collider(self.transform, size.x/2, size.x/2, size.y/2, size.y/2,collisionStayFunc=collisionStayFunc,onlyForTrigger=onlyForTrigger, showRect=showRect)
        self.gameObject.AddComponent(self.collider)
        mainScene.AddGameObject(self.gameObject)

windowSize = Vector2D(960,540)
centerPos = Vector2D(windowSize.x/2,windowSize.y/2 + 170)
window = Window("Platformer", windowSize)
mainScene = Scene(window)
menuScene = Scene(window)
gameEngine = OrumGame(window, {"menu": menuScene,"main": mainScene}, "menu")
background = Background(Image.open("Sprites\\background1.jpg"),Vector2D(windowSize.x/2,windowSize.y/2), Vector2D(960,540))
playerGameObject = Player()
blocks:list[Block] = [Block(Vector2D(350,700), Vector2D(500, 80)), 
                      Block(Vector2D(900,600), Vector2D(500, 80)), 
                      Block(Vector2D(1500,550), Vector2D(500, 80))]
def TouchPlayer(collider0: Collider, collider1: Collider)->None:
    if collider1 == playerGameObject.collider:
        print("Touched")
bottomCollider = ColliderBlock(Vector2D(windowSize.x/2,1500),Vector2D(1000,500),collisionStayFunc=TouchPlayer,onlyForTrigger=True, showRect=False)
left = True
pygame.init()
pygame.mixer.music.load("Sounds\\backgroundMusic0.mp3")
pygame.mixer.music.play(-1)
playerSoundChannel = pygame.mixer.Channel(0)
creatureSoundChannel = pygame.mixer.Channel(1)
jumpSound = pygame.mixer.Sound("Sounds\\jump.mp3")
creatureDeathSound = pygame.mixer.Sound("Sounds\\punch.mp3")
flyingCreatures = [FlyingCreature(Vector2D(1000, 400))]
walkingCreatures = [WalkingCreature(Vector2D(900, 400))]

def MainUpdate()->None:
    global left
    if gameEngine.GetKey(39):
        left = False
        playerGameObject.physics.SetVelocityX(5)
    if gameEngine.GetKey(37):
        left = True
        playerGameObject.physics.SetVelocityX(-5)
    if gameEngine.GetKeyDown(38):
        playerGameObject.physics.Jump(15)
        playerSoundChannel.play(jumpSound)
    deltaPos = playerGameObject.transform.GetPosition() - centerPos
    if deltaPos.y > 0:
        if left:
            playerGameObject.animController.Play("leftFall")
        else:
            playerGameObject.animController.Play("rightFall")
    elif deltaPos.y < 0:
        if left:
            playerGameObject.animController.Play("leftJump")
        else:
            playerGameObject.animController.Play("rightJump")
    else:
        if deltaPos.x > 0:
            playerGameObject.animController.Play("rightRun")
        elif deltaPos.x < 0:
            playerGameObject.animController.Play("leftRun")
        else:
            if left:
                playerGameObject.animController.Play("leftIdle")
            else:
                playerGameObject.animController.Play("rightIdle")
    for flyingCreature in flyingCreatures:
        flyingCreature.Move()
    for walkingCreature in walkingCreatures:
        walkingCreature.Move()
    backGroundMoveVector = Vector2D(-deltaPos.x,-deltaPos.y)
    bottomCollider.transform.Move(Vector2D(0,-deltaPos.y))
    for block in blocks:
        block.transform.Move(backGroundMoveVector)
    playerGameObject.transform.Move(backGroundMoveVector)
    for flyingCreature in flyingCreatures:
        flyingCreature.transform.Move(backGroundMoveVector)
    for walkingCreature in walkingCreatures:
        walkingCreature.transform.Move(backGroundMoveVector)

menuScene.GetCanvas().create_text(centerPos.x,centerPos.y - 250,font="Times 20 bold",text="Platformer")
menuScene.GetCanvas().create_text(centerPos.x,centerPos.y - 180,font="Times 15 italic bold",text="Start")
menuScene.GetCanvas().create_text(centerPos.x,centerPos.y - 130,font="Times 15 italic bold",text="Exit")
arrowGameObject = GameObject(menuScene)
arrowTransform = Transform(arrowGameObject, Vector2D(centerPos.x-80,centerPos.y - 180))
arrowGameObject.AddComponent(arrowTransform)
arrowRenderer = Renderer(arrowTransform, Image.open("Sprites\\arrow.png").resize((25, 20)))
arrowGameObject.AddComponent(arrowRenderer)
menuScene.AddGameObject(arrowGameObject)

menuIndex = 0
def MenuUpdate()->None:
    global menuIndex
    if gameEngine.GetKeyDown(32):
        if menuIndex == 0:
            gameEngine.SetCurrentScene("main")
        elif menuIndex == 1:
            window.Destroy()
    if gameEngine.GetKeyDown(38):
        menuIndex = (menuIndex + 1) % 2
    if gameEngine.GetKeyDown(40):
        menuIndex = (menuIndex - 1) % 2
    if menuIndex == 0:
        arrowTransform.SetPosition(Vector2D(centerPos.x-80,centerPos.y - 180))
    elif menuIndex == 1:
        arrowTransform.SetPosition(Vector2D(centerPos.x-80,centerPos.y - 130))

mainScene.SetUpdateFunc(MainUpdate)
menuScene.SetUpdateFunc(MenuUpdate)

gameEngine.GameUpdate()
