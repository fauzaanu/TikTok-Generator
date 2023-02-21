import praw, os
import requests, random
from moviepy.editor import * 
from datetime import date
import math
import PIL.ImageColor as ImageColor
 

#   Word by word splitting
def split_to_words(content):
    maincontent = []
    
    # split the content into words
    words = content.split(" ")

    # add the words to the list
    for i in range(len(words)):
        maincontent.append(words[i])

    return maincontent

# The creation of the video
def merge_video(fps, duration,image, kontent):
    
    clip = ImageClip(image).set_duration(duration).set_fps(fps).set_pos("center")
    
    
    
    rez_clip = CompositeVideoClip([clip], size=(1080,1920), )
    rez_clip = rez_clip.resize(lambda t: 1 + 0.04 * t)   # Zoom-in effect
    

    rez_clips = []
    for i in range(len(kontent)):      
        subclip = rez_clip.subclip(i*(duration/len(kontent)), (i+1)*(duration/len(kontent)))
        rez_clips.append(subclip)
       

# Texts
    text_clips = []
    for i in range(len(kontent)):
        
        colorlist = ["white", "red", "green", "yellow", "pink"]
 
        # take a random color from the list
        strokecol = "black"
        textcol = colorlist[random.randint(0, len(colorlist)-1)]
        
        # make sure the text color is not black
        while textcol == "black":
            textcol = colorlist[random.randint(0, len(colorlist)-1)]
            
        # if word has too much characters make the font smaller
        fs = 150
        
        if len(kontent[i]) > 25:
            fs = 100


        text = TextClip(kontent[i], fontsize=fs, color=textcol, font=f"{os.getcwd()}\\fonts\\lhohi.ttf", stroke_color=strokecol, stroke_width=7).set_duration(duration/len(kontent))
        text = text.set_position("center")

        text_clips.append(text)
        
        
    color_clips = []
    for i in range(len(kontent)):
        
        color = ColorClip(size=(int(text_clips[i].w*1.5), int(text_clips[i].h*1.5)), color=(0,0,0), duration=duration/len(kontent))
        color = color.set_position("center")
        color = color.set_duration(duration/len(kontent))
        
        color = color.margin(10, color=(255,255,0))
       
        color_clips.append(color)
        

    subtitle_clips = []
    for i in range(len(kontent)):
        
        subtitle_clips.append(CompositeVideoClip([text_clips[i]]))
        subtitle_clips[i] = subtitle_clips[i].set_position("center")
        subtitle_clips[i] = subtitle_clips[i].set_duration(duration/len(kontent))
        
    main_clips = []
    for i in range(len(kontent)):
        main_clips.append(CompositeVideoClip([rez_clips[i], subtitle_clips[i]], size=(1080,1920)))
        main_clips[i] = main_clips[i].set_duration(duration/len(kontent))
        
    print(len(main_clips))

    video_clip = concatenate_videoclips(main_clips)
    
    # some debug info
    print("rez_clips",len(rez_clips))
    print("text_clips",len(text_clips))
    print("color_clips",len(color_clips))
    print("subtitle_clips",len(subtitle_clips))
    print("main_clips",len(main_clips))

    # Export the video
    thread_count = os.cpu_count()
    import time
    # measure the time it took to run the program
    start = time.time()
    uname = str(date.today()) + str(random.randint(0, 1000000))
# make a unique file name
    video_clip.write_videofile(f"output/{uname}.mp4", fps=fps, threads=thread_count, audio=False, codec="h264_nvenc")
    end = time.time()
    print(end - start)
    
    
    
def phrases(filename:str, photofolder:str, fps:int,):
    """
    This function will take a text file and a folder of photos and will create a video with a random phrase from the text file and a random photo from the folder
    """
    
    # Photo will be choosen randomly from the specified
    photoname = f"visual//{photofolder}//" + random.choice(os.listdir(f"visual//{photofolder}//"))
    
    # The phrases will be choosen randomly from the specified file
    with open(f"{filename}.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        content = random.choice(lines)
    
    content = content.upper()
    duration = len(content) * 0.2/5
    if duration < 10:
        duration = 10
    print(duration)
    kontent = split_to_words(content)
    print(kontent)
    merge_video(fps, duration, photoname, kontent)
        
        
def longform(filename:str, photofolder:str, fps:int,):
    """
    This function will take a text file and a folder of photos and will create multiple videos for each line in the text file
    """
    
    # in this mode we are generating the full content. 1 video per line in the file
    with open(f"{filename}.txt", "r", encoding="utf-8") as f:
        # we need to know the number of lines in the file
        lines = f.readlines()
        
        for i in range(len(lines)):
            content = lines[i]
            content = content.upper()
            duration = len(content) * 0.2/5
            if duration < 10:
                duration = 10
            print(duration)
            kontent = split_to_words(content)
            print(kontent)
            photoname = f"visual//{photofolder}//" + random.choice(os.listdir(f"visual//{photofolder}//"))
            merge_video(fps, duration, photoname, kontent)
        


if __name__ == "__main__":
    longform("dhivehiphrases", "abstract", 60)

   
    
 
