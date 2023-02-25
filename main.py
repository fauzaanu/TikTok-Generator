import praw, os
import requests, random
from moviepy.editor import * 
from datetime import date
import math

def create_video(duration,input, amount):

    clip_amount = amount
    clip_duration = duration
    video = input
    
    
    start_time = video.duration / clip_amount
    start_times = [start_time * i for i in range(clip_amount)]
    end_times = [start_time * i + clip_duration for i in range(clip_amount)]
    
    
    clips = [video.subclip(start_time, end_time) for start_time, end_time in zip(start_times, end_times)]
    color_clip = ColorClip(size=(1080, 1920), color=(112, 128, 144), duration=clip_duration)
    
    # the clips should not have audio
    #clips = [clip.set_audio(None) for clip in clips]

    
    clips = [clip.fx(vfx.blackwhite) for clip in clips]
    scaled_clips = [clip.resize(width=1080) for clip in clips]
    clips_with_color = [CompositeVideoClip([color_clip, clip.set_pos('center')]) for clip in scaled_clips]
    
   
    for clip in clips_with_color:
        clip.duration = clip_duration
    
    
    for i, clip in enumerate(clips_with_color):
        if i == 1 or i == 2 or i == 5 or i == 7:
            clip.write_videofile(f"output{i}.mp4")

if __name__ == "__main__":
    inputvideo = VideoFileClip("Pulp.Fiction.1994.1080p.BrRip.x264.YIFY.mp4")
    create_video(10, inputvideo, 10)

   
    
 
