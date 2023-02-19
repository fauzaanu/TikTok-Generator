import praw, os
import requests, random
from moviepy.editor import * 
from datetime import date
import math
import PIL.ImageColor as ImageColor
 


#   Splits the quote in a dynamic way that is always 25 characters long in each part
def split_to_words(content):
    maincontent = []
    
    # split the content into words
    
    words = content.split(" ")
    # print(words)

    # add the words to the list
    for i in range(len(words)):
        maincontent.append(words[i])

    return maincontent



#               Merge Video

def merge_video(fps, duration,image, kontent):
    # make sure the image is in 1080x1920 resolution
    clip = ImageClip(image).set_duration(duration).set_fps(fps).set_pos("center")
    
    rez_clip = CompositeVideoClip([clip], size=(1080,1920), )
    rez_clip = rez_clip.resize(lambda t: 1 + 0.04 * t)  
    # Zoom-in effect
    
    
    
    rez_clips = []
    for i in range(len(kontent)):
        
        # the subclips will be split into as many parts as the number of splits in kontent and the duration for each part will be the duration of the video divided by the number of splits and the start and end position needs to be synced with the text clips
        
        subclip = rez_clip.subclip(i*(duration/len(kontent)), (i+1)*(duration/len(kontent)))
        rez_clips.append(subclip)
       


    
# the text clips will also be split into as many parts as the number of splits in kontent and the duration for each part will be the duration of the video divided by the number of splits
# Texts
    text_clips = []
    for i in range(len(kontent)):
        
        colorlist = ["white", "red", "green", "yellow", "pink"]
        
        # imagemagick fonts file does not contain all system fonts.
        # lets get a list of all the fonts installed on the system
        # and lets edit the type-ghostscript.xml file to include all the fonts
        
        # get a list of all the fonts installed on the windows system
        

        #fonts =TextClip.list('font')
        # print(fonts)
        
        
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
            
        
            
            #"Montserrat-Black"
            #MV-Boli


        text = TextClip(kontent[i], fontsize=fs, color=textcol, font="C:\\Users\\Fauzaanu\\Desktop\\fonts.fauzaanu\\Dhivehi Fonts Collection 0bcbbbfe0fc24b6a855c3761f5744ea5\\Dhivehi Fonts Main database dd2471ac389346f187a24fd3a89f172c\\Mvlhohi bold 6cd29f5185524784a35d2d34f4e6fc55\\Mvlhohi_bold.ttf", stroke_color=strokecol, stroke_width=7).set_duration(duration/len(kontent))
        text = text.set_position("center")

        
        text_clips.append(text)
        
        
    

# the background for the texts will be a black rectangle with a yellow border and they will also be split into as many parts as the number of splits in kontent and the duration for each part will be the duration of the video divided by the number of splits
    color_clips = []
    for i in range(len(kontent)):
        # there maybe more than 2 splits
        # so we will split the video into as many parts as the number of splits in kontent
        # the width of the rectangle will be the width of the text times 1.5
        # the height of the rectangle will be the height of the text times 1.5
        
        color = ColorClip(size=(int(text_clips[i].w*1.5), int(text_clips[i].h*1.5)), color=(0,0,0), duration=duration/len(kontent))
        color = color.set_position("center")
        color = color.set_duration(duration/len(kontent))
        
        # lets add a yellow border to the rectangle
        color = color.margin(10, color=(255,255,0))
       
        
        
        
        # we will add the clips to the set
        color_clips.append(color)
        


# Subtitle clips will be a combination of the text clips and the background clips and they need to be in the same order as the text clips
    subtitle_clips = []
    for i in range(len(kontent)):
        # subtitle_clips.append(CompositeVideoClip([color_clips[i], text_clips[i]]))
        # subtitle_clips[i] = subtitle_clips[i].set_position("center")
        # subtitle_clips[i] = subtitle_clips[i].set_duration(duration/len(kontent))
        
        subtitle_clips.append(CompositeVideoClip([text_clips[i]]))
        subtitle_clips[i] = subtitle_clips[i].set_position("center")
        subtitle_clips[i] = subtitle_clips[i].set_duration(duration/len(kontent))
        
           

    main_clips = []
   
    for i in range(len(kontent)):
        # we need to concat the subtitle clips to the main clips along with the rez clips

        main_clips.append(CompositeVideoClip([rez_clips[i], subtitle_clips[i]], size=(1080,1920)))
        
        main_clips[i] = main_clips[i].set_duration(duration/len(kontent))
        

    print(len(main_clips))

# Final Video should be a combination of all the clips in main_clips
    video_clip = concatenate_videoclips(main_clips)
    
    
    # there are some words being skipped to find out lets log the len of all the lists and see if they are the same
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
    
    # AV1 is the fasted codec but it is not supported by most devices
    # what file format should we use for AV1?
    # video_clip.write_videofile("visual/output.mp4", fps=fps, threads=thread_count, preset="fast", codec="libaom-av1")
    
    video_clip.write_videofile("visual/output.mp4", fps=fps, threads=thread_count, audio=False, codec="h264_nvenc")
    # good night friends measureing
    # 69.35123443603516 with h264_nvenc 75.53507041931152 86.18613743782043
    # no codec given 74.1991195678711
    # hevc_nvenc 71.86556506156921
    # mpeg4 72.23147368431091
    
    
    
    
    
    end = time.time()
    print(end - start)

    


if __name__ == "__main__":

   

    photoname = "visual/bgImg.jpg"
    content = input("Enter Content: ")
    
    # lets capitalize all the ketters in the content
    content = content.upper()
    

    

    duration = len(content) * 0.2/5
    if duration < 10:
        duration = 10
    print(duration)

    # get_photo(client_id, client_secret, user_agent, username, password, "EarthPorn", photoname)
    kontent = split_to_words(content)
    print(kontent)
    # audio = get_music(music)

    merge_video(75, duration, photoname, kontent)
    
 
