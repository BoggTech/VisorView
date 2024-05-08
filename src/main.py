import globals
from panda3d.core import loadPrcFile
loadPrcFile(globals.CONFIG_DIR)

import os
from datetime import datetime
from panda3d.core import AntialiasAttrib, Loader
from panda3d.core import TextNode, Mat4
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from camera import Camera

resources = globals.RESOURCES_DIR
if not os.path.exists(resources):
            os.makedirs(resources)
            print("Please input Toontown Rewritten extracted phase files!")

class VisorView(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = base
        self.render = render

        self.camera_controller = Camera()

        # initialize shadow
        self.shadow = loader.loadModel(globals.SHADOW_MODEL)
        self.shadow.setScale(globals.SHADOW_SCALE)
        self.shadow.setColor(globals.SHADOW_COLOR)

        # initialize the gui
        self.animationScrollList = DirectScrolledList(
            incButton_pos=(-1, 0, -.1), 
            incButton_text="DN",
            incButton_text_scale=0.1,
            incButton_borderWidth=(0.05, 0.05),
            
            decButton_pos=(-1, 0, .1), 
            decButton_text="UP", 
            decButton_text_scale=0.1,
            decButton_borderWidth=(0.05, 0.05),

            itemFrame_pos=(-.8, 0, 0.8),
            forceHeight=.11,
            
            numItemsVisible=15)
        self.animationScrollList.hide()
        self.is_animation_scroll = False
        
        # initialize our actor
        self.actor = None
        self.available_animations = []
        self.is_shadow = True
        self.is_head = True
        self.is_body = True
        self.is_posed = False
        self.is_blend = True
        self.current_animation = "zero"
        self.last_pose_frame = 0
        self.cog_list = list(globals.COG_DATA)
        self.current_cog_index = 0
        self.current_cog = self.cog_list[self.current_cog_index]
        self.build_cog()

        self.reset_actor_pos()
        self.reset_camera_pos()

        # we're initialized, time to accept input
        self.accept("space", self.cycle)
        self.accept("s", self.toggle_shadow)
        self.accept("control-b", self.toggle_body)
        self.accept("control-h", self.toggle_head)
        self.accept("a", self.toggle_animation_scroll)
        self.accept("p", self.toggle_pose)
        self.accept("b", self.toggle_blend)
        self.accept("r", self.reset_camera_roll)
        self.accept("f9", self.take_screenshot)
        self.accept("control-z", self.reset_camera_pos)
        self.accept("wheel_up", self.scroll_up)
        self.accept("wheel_down", self.scroll_down)
    
    def take_screenshot(self):
        path = globals.SCREENSHOT_DIR
        if not os.path.exists(path):
            os.makedirs(path)
        
        now = datetime.now()
        date_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        screenshot_name = os.path.join(path, "ss-{}-{}.png".format(self.current_cog, date_string))
        self.base.screenshot(screenshot_name, False)

    def enable_mouse_cam(self):
        self.camera_controller.enable()
        
    def disable_mouse_cam(self):
        self.camera_controller.disable()

    def reset_camera_roll(self):
        camera.setR(0)

    def reset_actor_pos(self):
        self.actor.setPosHpr(*globals.DEFAULT_POS, *globals.DEFAULT_HPR)

    def reset_camera_pos(self):
        base.camera.setPosHpr(*globals.DEFAULT_CAMERA_POS,0,0,0)
        
    def toggle_animation_scroll(self, state=None):
        if not state == None:
            self.is_animation_scroll = state
        else:
            self.is_animation_scroll = not self.is_animation_scroll

        if self.is_animation_scroll:
            self.animationScrollList.show()
            self.disable_mouse_cam()
        else:
            self.animationScrollList.hide()
            self.enable_mouse_cam()

    def scroll_up(self):
        if ( self.is_animation_scroll ):
            self.animationScrollList.scrollBy(-1)
        elif ( self.is_posed and self.last_pose_frame != None ):
            self.last_pose_frame += 1
            if self.last_pose_frame > self.actor.getNumFrames(self.current_animation):
                self.last_pose_frame = 0
            self.actor.pose(self.current_animation, self.last_pose_frame)

    def scroll_down(self):
        if ( self.is_animation_scroll ):
            self.animationScrollList.scrollBy(1)
        elif ( self.is_posed and self.last_pose_frame != None ):
            self.last_pose_frame -= 1
            if self.last_pose_frame < 0:
                self.last_pose_frame = self.actor.getNumFrames(self.current_animation)
            self.actor.pose(self.current_animation, self.last_pose_frame)
    
    def toggle_pose(self):
        self.is_posed = not self.is_posed
        if self.is_posed:
            # if the scroll is open, toggle it
            self.toggle_animation_scroll(False)
            self.last_pose_frame = self.actor.getCurrentFrame()
            self.actor.pose(self.current_animation, self.last_pose_frame)
        else:
            self.actor.loop(self.current_animation)

    def set_animation(self, animation):
        self.current_animation = animation
        self.actor.loop(animation)

        # no more posing
        self.is_posed = False

    def toggle_blend(self):
        self.is_blend = not self.is_blend
        self.actor.setBlend(frameBlend=self.is_blend)

    def build_cog(self):
        # make sure the new actor is in the same place _ previous actor is removed
        pos = 0
        hpr = 0
        if not self.actor == None:
            pos = self.actor.getPos()
            hpr = self.actor.getHpr()
            self.actor.cleanup()
            self.actor.removeNode()
        
        body_path = ""
        body_animations = {}
        if ( globals.COG_DATA[self.current_cog]["suit"] == "a" ):
            body_path = globals.SUIT_A_MODEL
            body_animations = globals.SUIT_A_ANIMATION_DICT
            self.available_animations = globals.SUIT_A_ANIMATIONS
        elif ( globals.COG_DATA[self.current_cog]["suit"] == "b" ):
            body_path = globals.SUIT_B_MODEL
            body_animations = globals.SUIT_B_ANIMATION_DICT
            self.available_animations = globals.SUIT_B_ANIMATIONS
        else:
            body_path = globals.SUIT_C_MODEL
            body_animations = globals.SUIT_C_ANIMATION_DICT
            self.available_animations = globals.SUIT_C_ANIMATIONS

        self.animationScrollList.removeAndDestroyAllItems()
        for i in self.available_animations:
            if not i == "lose" and not i == "lose_zero":
                # lose animations have their own body type and viewing them on the wrong model = unpleasant
                new_button = DirectButton(text=i, 
                                            text_scale=0.1, 
                                            text_align = TextNode.ALeft, 
                                            relief = None,
                                            suppressMouse=False,
                                            command=self.set_animation,
                                            extraArgs=[i])
                self.animationScrollList.addItem(new_button)

        self.actor = Actor(body_path, body_animations)

        self.shadow.reparentTo(self.actor.find('**/def_shadow'))

        tx_blazer = loader.loadTexture(globals.COG_DATA[self.current_cog]["blazer"])
        self.actor.find('**/torso').setTexture(tx_blazer, 1)

        tx_leg = loader.loadTexture(globals.COG_DATA[self.current_cog]["leg"])
        self.actor.find('**/legs').setTexture(tx_leg, 1)

        tx_sleeve = loader.loadTexture(globals.COG_DATA[self.current_cog]["sleeve"])
        self.actor.find('**/arms').setTexture(tx_sleeve, 1)
        
        self.actor.find('**/hands').setColor(globals.COG_DATA[self.current_cog]["hands"])

        medallion = globals.COG_DATA[self.current_cog]["emblem"]
        chest_null = self.actor.find("**/def_joint_attachMeter")
        icons = loader.loadModel(globals.COG_ICONS)
        corp_medallion = icons.find('**/' + medallion).copyTo(chest_null)
        corp_medallion.setPosHprScale(*globals.COG_ICON_POS_HPR_SCALE)

        head = loader.loadModel(globals.COG_DATA[self.current_cog]["head"])
        head.reparentTo(self.actor.find('**/def_head'))

        self.actor.setScale(globals.COG_DATA[self.current_cog]["scale"])

        self.actor.setPos(pos)
        self.actor.setHpr(hpr)

        # match settings
        self.toggle_head(False)
        self.toggle_shadow(False)
        self.toggle_body(False)

        self.actor.reparentTo(render)
        self.actor.setBlend(frameBlend=self.is_blend)
    
    # Function that switches to the next cog in the index
    def cycle(self):
        self.current_cog_index += 1
        if ( self.current_cog_index >= len(self.cog_list) ):
            self.current_cog_index = 0
        self.current_cog = self.cog_list[self.current_cog_index]
        self.build_cog()

    # Function to toggle shadow hidden/unhidden, update_state exists if we want to make sure it's in the right state (i.e
    # hidden when false rather than shown) instead of toggling it.
    def toggle_shadow(self, update_state=True):
        if update_state:
            self.is_shadow = not self.is_shadow

        if self.is_shadow:
            self.shadow.show_through()
        else:
            self.shadow.hide()

    # Hide/show head, update_state exists if we want to make sure it's in the right state (i.e
    # hidden when false rather than shown) instead of toggling it.
    def toggle_head(self, update_state=True):
        if update_state:
            self.is_head = not self.is_head

        if self.is_head:
            self.actor.find('**/def_head').show_through()
        else:
            self.actor.find('**/def_head').hide()

    # Hide/show head, update_state exists if we want to make sure it's in the right state (i.e
    # hidden when false rather than shown) instead of toggling it.
    def toggle_body(self, update_state=True):
        if update_state:
            self.is_body = not self.is_body

        if self.is_body:
            self.actor.show_through()
        else:
            self.actor.hide()

        # make sure the children are shown/hidden if they need to be
        self.toggle_head(False)
        self.toggle_shadow(False)

    
app = VisorView()
app.render.setAntialias(AntialiasAttrib.MMultisample)
app.run()