from __future__ import annotations
from tkinter import *
from typing import Callable
from PIL import Image, ImageTk
from UtilityLibs import *

class Window:
    def __init__(self, title: str, size: Vector2D):
        self.__tk = Tk()
        self.__tk.title(title)
        self.__tk.geometry("%dx%d" %(size.x, size.y))
    def GetTK(self)->Tk:
        return self.__tk
    def Destroy(self):
        self.__tk.destroy()

class Scene:
    def __init__(self, window: Window, backgroundColor:str = "white"):
        self.__canvas = Canvas(window.GetTK(),background=backgroundColor)
        self.__gameObjects:list[GameObject] = []
        self.__colliders:list[Collider] = []
        self.__isPacked = False
        self.__updateFunc:Callable[[None],None] = None
    def GetCanvas(self)->Canvas:
        return self.__canvas
    def AddGameObject(self, gameObject:GameObject)->None:
        self.__gameObjects.append(gameObject)
    def Update(self)->None:
        for gameObject in self.__gameObjects:
            gameObject.Update()
        for colliderA in self.__colliders:
            self.CollisionCheck(colliderA)
        if self.__updateFunc is not None:
            self.__updateFunc()
    def SetUpdateFunc(self, updateFunc: Callable[[None],None])->None:
        self.__updateFunc = updateFunc
    def AddCollider(self, collider:Collider)->None:
        self.__colliders.append(collider)
    def CollisionCheck(self, colliderA: Collider)->None:
        for colliderB in self.__colliders:
            if colliderA != colliderB and Collider.IsCollided_AABB(colliderA, colliderB):
                colliderA.OnCollisionStay(colliderB)
    def GetColliders(self)->list[Collider]:
        return self.__colliders
    def DeleteCollider(self, collider:Collider):
        self.__colliders.remove(collider)
    def GetIsPacked(self):
        return self.__isPacked
    def Pack(self):
        self.__canvas.pack(expand=True, fill=BOTH)
        self.__isPacked = True
    def Unpack(self):
        self.__canvas.pack_forget()
        self.__isPacked = False

class OrumGame:
    def __init__(self, window: Window, nameToScene: dict[str, Scene]=None, currentSceneName: str=None):
        self.__window = window
        if nameToScene is None:
            self.__nameToScene = {}
        else:
            self.__nameToScene = nameToScene
        self.__currentSceneName: str = currentSceneName
        self.SetCurrentScene(currentSceneName)
        self.__window.GetTK().bind("<KeyPress>",self.OnPressKey)
        self.__window.GetTK().bind("<KeyRelease>",self.OnReleaseKey)
        self.__window.GetTK().protocol("WM_DELETE_WINDOW", self.OnClose)
        self.__pressedKeys = set()
        self.__pressedOnceKeys = set()
        self.__releasedOnceKeys = set()
        self.__window.GetTK().bind("<ButtonPress-1>",self.OnPressMouseLeftButton)
        self.__window.GetTK().bind("<ButtonRelease-1>",self.OnReleaseMouseLeftButton)
        self.__pressedMouseLeftButton = False
        self.__pressedOnceMouseLeftButton = False
        self.__releasedOnceMouseLeftButton = False
        self.__window.GetTK().bind("<ButtonPress-2>",self.OnPressMouseWheelButton)
        self.__window.GetTK().bind("<ButtonRelease-2>",self.OnReleaseMouseWheelButton)
        self.__pressedMouseWheelButton = False
        self.__pressedOnceMouseWheelButton = False
        self.__releasedOnceMouseWheelButton = False
        self.__window.GetTK().bind("<ButtonPress-3>",self.OnPressMouseRightButton)
        self.__window.GetTK().bind("<ButtonRelease-3>",self.OnReleaseMouseRightButton)
        self.__pressedMouseRightButton = False
        self.__pressedOnceMouseRightButton = False
        self.__releasedOnceMouseRightButton = False
        self.__window.GetTK().bind("<Motion>",self.OnMouseMove)
        self.__mousePosition = Vector2D(0,0)
    def SetCurrentScene(self, sceneName:str)->None:
        self.__currentSceneName = sceneName
    def AddScene(self, sceneName: str ,scene: Scene)->None:
        self.__nameToScene[sceneName] = scene
    def SetCurrentScene(self, sceneName: str)->None:
        self.__nameToScene[self.__currentSceneName].Unpack()
        self.__currentSceneName = sceneName
        self.__nameToScene[self.__currentSceneName].Pack()
    def GameUpdate(self)->None:
        while True:
            try:
                self.__nameToScene[self.__currentSceneName].Update()
                self.__pressedOnceKeys.clear()
                self.__releasedOnceKeys.clear()
                self.__pressedOnceMouseLeftButton = False
                self.__pressedOnceMouseWheelButton = False
                self.__pressedOnceMouseRightButton = False
                self.__releasedOnceMouseLeftButton = False
                self.__releasedOnceMouseWheelButton = False
                self.__releasedOnceMouseRightButton = False
            except TclError:
                return

            self.__window.GetTK().after(15)
            self.__window.GetTK().update()
    def GetKey(self, keyCode: int)->bool:
        if keyCode in self.__pressedKeys:
            return True
        return False
    def GetKeyDown(self, keyCode: int)->bool:
        if keyCode in self.__pressedOnceKeys:
            return True
        return False
    def GetKeyUp(self, keyCode: int)->bool:
        if keyCode in self.__releasedOnceKeys:
            return True
        return False
    def GetMouseButton(self, keyCode: int)->bool:
        if keyCode == 0:
            return self.__pressedMouseLeftButton
        if keyCode == 1:
            return self.__pressedMouseWheelButton
        if keyCode == 2:
            return self.__pressedMouseRightButton
        return False
    def GetMouseButtonDown(self, keyCode: int)->bool:
        if keyCode == 0:
            return self.__pressedOnceMouseLeftButton
        if keyCode == 1:
            return self.__pressedOnceMouseWheelButton
        if keyCode == 2:
            return self.__pressedOnceMouseRightButton
        return False
    def GetMouseButtonUp(self, keyCode: int)->bool:
        if keyCode == 0:
            return self.__releasedOnceMouseLeftButton
        if keyCode == 1:
            return self.__releasedOnceMouseLeftButton
        if keyCode == 2:
            return self.__releasedOnceMouseLeftButton
        return False
    def GetMousePosition(self)->Vector2D:
        return self.__mousePosition
    def OnPressKey(self,event)->None:
        self.__pressedKeys.add(event.keycode)
        self.__pressedOnceKeys.add(event.keycode)
        if event.keycode in self.__releasedOnceKeys:
            self.__releasedOnceKeys.remove(event.keycode)
    def OnReleaseKey(self, event)->None:
        self.__releasedOnceKeys.add(event.keycode)
        if event.keycode in self.__pressedKeys:
            self.__pressedKeys.remove(event.keycode)
        if event.keycode in self.__pressedOnceKeys:
            self.__pressedOnceKeys.remove(event.keycode)
    def OnPressMouseLeftButton(self, event)->None:
        self.__pressedMouseLeftButton = True
        self.__pressedOnceMouseLeftButton = True
        self.__releasedOnceMouseLeftButton = False
    def OnReleaseMouseLeftButton(self, event)->None:
        self.__pressedMouseLeftButton = False
        self.__pressedOnceMouseLeftButton = False
        self.__releasedOnceMouseLeftButton = True
    def OnPressMouseWheelButton(self, event)->None:
        self.__pressedMouseWheelButton = True
        self.__pressedOnceMouseWheelButton = True
        self.__releasedOnceMouseWheelButton = False
    def OnReleaseMouseWheelButton(self, event)->None:
        self.__pressedMouseWheelButton = False
        self.__pressedOnceMouseWheelButton = False
        self.__releasedOnceMouseWheelButton = True
    def OnPressMouseRightButton(self, event)->None:
        self.__pressedMouseRightButton = True
        self.__pressedOnceMouseRightButton = True
        self.__releasedOnceMouseRightButton = False
    def OnReleaseMouseRightButton(self, event)->None:
        self.__pressedMouseRightButton = False
        self.__pressedOnceMouseRightButton = False
        self.__releasedOnceMouseRightButton = True
    def OnMouseMove(self, event)->None:
        self.__mousePosition = Vector2D(event.x, event.y)
    def OnClose(self)->None:
        self.window.destroy()

class Component:
    def GetGameObject(self):
        pass

class UpdateComponent(Component):
    def Update(self):
        pass

class DestroyComponent:
    def Destroy(self):
        pass

class GameObject(UpdateComponent,DestroyComponent):
    def __init__(self, scene:Scene, tag:str="None" , components:list[Component]=None):
        if components is None:
            self.__components:list[Component] = []
        if components is not None:
            self.__components = components
        self.__scene = scene
        self.__tag = tag
    def Update(self):
        for component in self.__components:
            if isinstance(component ,UpdateComponent):
                component.Update()
    def AddComponent(self, component:Component)->None:
        self.__components.append(component)
    def GetScene(self)->Scene:
        return self.__scene
    def GetTag(self)->str:
        return self.__tag
    def GetGameObject(self)->GameObject:
        return self
    def GetComponent(self, componentType:Component)->Component:
        for component in self.__components:
            if isinstance(component, componentType):
                return component
        return None
    def GetComponents(self, componentType:Component)->list[Component]:
        components:list[Component] = []
        for component in self.__components:
            if isinstance(component, componentType):
                components.append(component)
        return components
    def Destroy(self):
        for component in self.__components:
            if isinstance(component, DestroyComponent):
                component.Destroy()
                del component

class Transform(UpdateComponent,DestroyComponent):
    def __init__(self, gameObject: GameObject, position: Vector2D):
        self.__gameObject = gameObject
        self.__targetTransform = gameObject.GetScene().GetCanvas().create_image(position.x, position.y)
        self.__position = position
    def Update(self)->None:
        self.__gameObject.GetScene().GetCanvas().coords(self.__targetTransform, self.__position.x, self.__position.y)
    def GetScene(self)->Scene:
        return self.__gameObject.GetScene()
    def GetTargetTransform(self)->Transform:
        return self.__targetTransform
    def SetPosition(self, position: Vector2D)->None:
        self.__position = position
    def GetPosition(self)->Vector2D:
        return self.__position
    def Move(self, deltaPosition : Vector2D)->None:
        self.__position += deltaPosition
    def GetGameObject(self)->GameObject:
        return self.__gameObject.GetGameObject()
    def Destroy(self):
        self.GetScene().GetCanvas().delete(self.__targetTransform)

class Renderer:
    def __init__(self, transform: Transform, source:str | Image.Image=None, transpose=None):
        if source is not None:
            if isinstance(source, str):
                source = Image.open(source)
            if isinstance(source, Image.Image):
                if transpose is None:
                    frame = source.copy()
                else:
                    frame = source.copy().transpose(transpose)
                self.__image = ImageTk.PhotoImage(frame)
            transform.GetScene().GetCanvas().itemconfigure(transform.GetTargetTransform(), image=self.__image)
        self.__transform = transform
    def GetScene(self)->Scene:
        return self.__transform.GetScene()
    def GetTargetTransform(self)->Transform:
        return self.__transform.GetTargetTransform()
    def GetGameObject(self)->GameObject:
        return self.__transform.GetGameObject()

class AnimationController(UpdateComponent):
    def __init__(self, renderer:Renderer ,nameToAnim:dict[str, Animation]=None):
        if nameToAnim is None:
            self.__nameToAnim:dict[str, Animation] = {}
        else:
            self.__nameToAnim = nameToAnim
        self.__renderer = renderer
        self.__currentAnim = None
    def AddAnim(self,name:str, anim:Animation)->None:
        self.__nameToAnim[name] = anim
        if self.__currentAnim is None:
            self.__currentAnim = anim
    def Play(self,name:str)->None:
        self.__currentAnim = self.__nameToAnim[name]
    def Update(self)->None:
        if self.__currentAnim != None:
            self.__currentAnim.Update()
    def GetScene(self)->Scene:
        return self.__renderer.GetScene()
    def GetTargetTransform(self)->Transform:
        return self.__renderer.GetTargetTransform()
    def GetGameObject(self)->GameObject:
        return self.__renderer.GetGameObject()

class Animation:
    def __init__(self, animController: AnimationController, source: str | Image.Image | list[Image.Image], waitFrame: int, transpose=None):
        if isinstance(source, str):
            source = Image.open(source)
        if isinstance(source, Image.Image):
            frames:list[Image.Image] = []
            try:
                while True:
                    if transpose is None:
                        frame = source.copy()
                    else:
                        frame = source.copy().transpose(transpose)
                    frames.append(ImageTk.PhotoImage(frame))
                    source.seek(source.tell() + 1)
            except EOFError:
                pass
            source = frames
        self.__currentIndex = 0
        self.__frames = frames
        self.__animTick = Tick(waitFrame)
        self.__animController = animController
    def PopFrame(self)->list[Image.Image]:
       currentFrame:list[Image.Image] = self.__frames[self.__currentIndex]
       self.__currentIndex = (self.__currentIndex + 1) % len(self.__frames)
       return currentFrame
    def Update(self)->None:
        if self.__animTick.Trigger():
            self.__animController.GetScene().GetCanvas().itemconfig(self.__animController.GetTargetTransform() , image=self.PopFrame())
    def Reset(self)->None:
        self.__currentIndex = 0
        self.__animTick.Reset()

class Collider(UpdateComponent,DestroyComponent):
    def __init__(self, transform: Transform, left: int, right: int, top: int, bottom: int, collisionStayFunc: Callable[[Collider, Collider],None] = None, onlyForTrigger:bool=False ,showRect: bool = True, rectColor: str = "skyblue", colliderTag:str="None"):
        transform.GetScene().AddCollider(self)
        self.__transform = transform
        self.__leftTop = Vector2D(left, top)
        self.__rightBottom = Vector2D(right, bottom)
        self.__colliderRect = transform.GetScene().GetCanvas().create_rectangle(self.__leftTop.x ,self.__leftTop.y,self.__rightBottom.x,self.__rightBottom.y, fill="", outline=rectColor)
        self.__collisionStayFunc = collisionStayFunc
        self.__onlyForTrigger = onlyForTrigger
        self.__colliderTag = colliderTag
        if showRect:
            self.ShowRect()
        else:
            self.HideRect()
    def GetColliderTag(self)->str:
        return self.__colliderTag
    def ShowRect(self)->None:
        self.__transform.GetScene().GetCanvas().itemconfigure(self.__colliderRect, state="normal")
    def HideRect(self)->None:
        self.__transform.GetScene().GetCanvas().itemconfigure(self.__colliderRect, state="hidden")
    def ChangeColor(self, rectColor: str)->None:
        self.__transform.GetScene().GetCanvas().itemconfigure(self.__colliderRect, outline=rectColor)
    def GetCurrentLeftTopAndRightBottom(self)->tuple[Vector2D,Vector2D]:
        leftTop = Vector2D(self.__transform.GetPosition().x - self.__leftTop.x,self.__transform.GetPosition().y - self.__leftTop.y)
        rightBottom = Vector2D(self.__transform.GetPosition().x + self.__rightBottom.x,self.__transform.GetPosition().y + self.__rightBottom.y)
        return (leftTop, rightBottom)
    def GetLeftRightTopBottom(leftTop:Vector2D, rightBottom:Vector2D)->tuple[int|float, int|float,int|float,int|float]:
        return (leftTop.x,rightBottom.x,leftTop.y, rightBottom.y)
    def Update(self)->None:
        leftTop, rightBottom = self.GetCurrentLeftTopAndRightBottom()
        self.__transform.GetScene().GetCanvas().coords(self.__colliderRect, leftTop.x, leftTop.y, rightBottom.x, rightBottom.y)
    def SetOnlyForTrigger(self, yes: bool = True)->None:
        self.__onlyForTrigger = yes
    def GetOnlyForTrigger(self)->bool:
        return self.__onlyForTrigger
    def MoveWithCollision(self, deltaPosition : Vector2D)->Vector2D:
        self.__transform.Move(deltaPosition)
        coliders = self.__transform.GetScene().GetColliders()
        netPenetrationVector = Vector2D(0,0)
        for colliderB in coliders:
            if self != colliderB and colliderB.GetOnlyForTrigger() == False and Collider.IsCollided_AABB(self, colliderB):
                leftTopA, rightBottomA = self.GetCurrentLeftTopAndRightBottom()
                aLeft,aRight,aTop,aBottom = Collider.GetLeftRightTopBottom(leftTopA, rightBottomA)
                leftTopB, rightBottomB = colliderB.GetCurrentLeftTopAndRightBottom()
                bLeft,bRight,bTop,bBottom = Collider.GetLeftRightTopBottom(leftTopB, rightBottomB)
                overlapX = min(aRight, bRight) - max(aLeft, bLeft)
                overlapY = min(aBottom, bBottom) - max(aTop, bTop)
                aCenter = Vector2D((aLeft+aRight)/2, (aTop+aBottom)/2)
                bCenter = Vector2D((bLeft+bRight)/2, (bTop+bBottom)/2)
                penetrationVector = Vector2D(0,0)
                if overlapX < overlapY:
                    if aCenter.x < bCenter.x:
                        penetrationVector.x = -overlapX
                    else:
                        penetrationVector.x = overlapX
                else:
                    if aCenter.y < bCenter.y:
                        penetrationVector.y = -overlapY
                    else:
                        penetrationVector.y = overlapY
                self.__transform.Move(penetrationVector)
                netPenetrationVector += penetrationVector
        return netPenetrationVector
    def GetScene(self)->Scene:
        return self.__transform.GetScene()
    def GetTargetTransform(self)->Transform:
        return self.__transform.GetTargetTransform()
    def GetGameObject(self)->GameObject:
        return self.__transform.GetGameObject()
    def AddCollisionStayFunc(self, collisionStayFunc: Callable[[Collider, Collider],None]):
        self.__collisionStayFunc = collisionStayFunc
    def OnCollisionStay(self, other: Collider)->None:
        if self.__collisionStayFunc is not None:
            self.__collisionStayFunc(self, other)
    def IsCollided_AABB(colliderA:Collider, colliderB:Collider)->bool:
        leftTopA, rightBottomA = colliderA.GetCurrentLeftTopAndRightBottom()
        aLeft,aRight,aTop,aBottom = Collider.GetLeftRightTopBottom(leftTopA, rightBottomA)
        leftTopB, rightBottomB = colliderB.GetCurrentLeftTopAndRightBottom()
        bLeft,bRight,bTop,bBottom = Collider.GetLeftRightTopBottom(leftTopB, rightBottomB)
        if (aLeft < bRight and aRight > bLeft) and (aTop < bBottom and aBottom > bTop):
            return True
        return False
    def Destroy(self):
        self.GetScene().GetCanvas().delete(self.__colliderRect)
        self.GetGameObject().GetScene().DeleteCollider(self)

class Physics(UpdateComponent):
    def __init__(self, collider:Collider, gravityAcceleration: int|float, terminalVelocity: int|float, horizontalFriction: int|float=1, jumpCount: int = 1):
        self.__collider = collider
        self.__velocity = Vector2D(0,0)
        self.__gravityAcceleration = gravityAcceleration
        self.__terminalVelocity = terminalVelocity
        self.__maxJumpCount = jumpCount
        self.__currentJumpCount = jumpCount
        self.__horizontalFriction = horizontalFriction
    def GetScene(self)->Scene:
        return self.__collider.GetScene()
    def GetTargetTransform(self)->Transform:
        return self.__collider.GetTargetTransform()
    def GetGameObject(self)->GameObject:
        return self.__collider.GetGameObject()
    def SetGravityAcceleration(self, gravityAcceleration: int|float)->None:
        self.__gravityAcceleration = gravityAcceleration
    def SetTerminalVelocity(self, terminalVelocity: int|float)->None:
        self.__terminalVelocity = terminalVelocity
    def SetJumpCount(self, jumpCount: int)->None:
        self.__jumpCount = jumpCount
    def SetVelocity(self, velocity: Vector2D)->None:
        self.__velocity = velocity
    def SetVelocityX(self, velocityX: int|float)->None:
        self.__velocity.x = velocityX
    def AccelerateX(self, accelerationX: int|float)->None:
        self.__velocity.x = self.__velocity.x + accelerationX
    def GetVelocity(self)->Vector2D:
        return self.__velocity
    def Update(self)->None:
        netPenetrationVector = self.__collider.MoveWithCollision(self.__velocity)
        if self.__velocity.x != 0:
            if abs(self.__velocity.x) < self.__horizontalFriction:
                self.__velocity.x = 0
            elif self.__velocity.x > 0:
                self.__velocity.x -= self.__horizontalFriction
            elif self.__velocity.x < 0:
                self.__velocity.x += self.__horizontalFriction
        if netPenetrationVector.y < 0:
            self.__velocity.y = 0
            self.__currentJumpCount = self.__maxJumpCount
        elif self.__velocity.y < self.__terminalVelocity:
            self.__velocity.y = self.__velocity.y + self.__gravityAcceleration
    def Jump(self, jumpPower: int|float)->None:
        if self.__maxJumpCount == -1 or self.__currentJumpCount > 0:
            self.__velocity.y = -jumpPower
            if self.__currentJumpCount > 0:
                self.__currentJumpCount -= 1