import sys
import time
import pygame
from . import window
from . import gameimage
from pygame.locals import *

pygame.init()

class Animation(gameimage.GameImage):

    def __init__(self, image_file, total_frames, loop=True):
        gameimage.GameImage.__init__(self, image_file)

        self.width = self.width/float(total_frames)  
        self.height = self.height

        self.playing = True
        self.drawable = True
        self.loop = loop

        self.total_frames = total_frames
        self.initial_frame = 0
        self.curr_frame = 0
        self.final_frame = total_frames

        self.frame_duration = []
        self.total_duration = 0

        # Tempo atual em ms
        self.last_time = int(round(time.time() * 1000))

        self.set_sequence(0, self.total_frames, self.loop)
        
    # ----------------------- SEQUENCE SETTERS -------------------- #

    def set_sequence(self, initial_frame, final_frame, loop=True):
        self.set_initial_frame(initial_frame)
        self.set_curr_frame(initial_frame)
        self.set_final_frame(final_frame)
        self.set_loop(loop)

    def set_sequence_time(self, initial_frame, final_frame,
                          total_duration, loop=True):
        self.set_sequence(initial_frame, final_frame, loop)
        time_ms = int(round(total_duration / float(final_frame - initial_frame + 1)))
        for x in range(initial_frame, final_frame):
            self.frame_duration.append(total_duration)

    def set_total_duration(self, time_ms):
        time_frame = float(time_ms) / self.total_frames
        self.total_duration = time_frame * self.total_frames
        for x in range(0, self.total_frames):
            self.frame_duration.append(time_frame)

    # ----------------------- DRAW & UPDATE METHODS -------------------- #

    def update(self):
        if(self.playing):
            time_ms = int(round(time.time() * 1000)) 
            if((time_ms - self.last_time > self.frame_duration[self.curr_frame])
               and (self.final_frame != 0)):
                self.curr_frame += 1
                self.last_time = time_ms
            if((self.curr_frame == self.final_frame) and (self.loop)):
                self.curr_frame = self.initial_frame
            else:
                if((not self.loop) and (self.curr_frame + 1 >= self.final_frame)):
                    self.curr_frame = self.final_frame - 1
                    self.playing = False
            
    def draw(self):
        if(self.drawable):
            clip_rect = pygame.Rect(self.curr_frame*self.width,
                                    0,
                                    self.width,
                                    self.height
                                    )

            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            window.Window.get_screen().blit(self.image, self.rect, area=clip_rect)
    
    # ---------------------- PLAYING CONTROL METHODS ---------------------- #

    def stop(self):
        self.curr_frame = self.initial_frame
        self.playing = False

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False
        
    def is_playing(self):
        return self.playing

    def is_looping(self):
        return self.loop

    def set_loop(self, loop):
        self.loop = loop

    def hide(self):
        self.drawable = False

    def unhide(self):
        self.drawable = True

    # ------------------------ GETTER & SETTER METHODS ------------------- # 

    def get_total_duration(self):
        return self.total_duration
    
    def set_initial_frame(self, frame):
        self.initial_frame = frame

    def get_initial_frame(self):
        return self.initial_frame

    def set_final_frame(self, frame):
        self.final_frame = frame

    def get_final_frame(self):
        return self.final_frame

    def set_curr_frame(self, frame):
        self.curr_frame = frame

    def get_curr_frame(self):
        return self.curr_frame