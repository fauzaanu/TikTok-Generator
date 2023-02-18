import praw, os
import requests, random
from moviepy.editor import * 
from datetime import date
 



#           Get reddit photos
def get_photo(client_id,client_secret, user_agent, username,password,subreddit, filename):
    folder = os.getcwd()
    reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = user_agent, username = username, password = password)

    subred = reddit.subreddit(subreddit)
    bg_photo_post = subred.hot(limit = 1)


    #               Download The Photo
    for i in bg_photo_post:
        print(i.title,"\n" ,i.url, "\n")
        req = requests.get(i.url)
        format = i.url.split(".")

        if format[-1] == "jpg":
            with open(filename, "wb") as file:
                file.write(req.content)
                file.close()

#               Get the quote
def get_quote():
    # today = date.today() 
    # day_of_year = today.strftime('%j')
    
    # print("\nDay of year: ", day_of_year, "\n")
    
    # with open(quotesfile, "r", encoding="utf-8") as file:
    #     allquotes = file.read()
    #     quotes = allquotes.split("_***_\n")
    #     quote = quotes[int(day_of_year)]
    
    # quote = quote.replace("-----", " ")
    
    quote = input("Enter Quote: ")
    
    
    
    return quote

        #   Splits the quote in 2
def split_quote(quote):
    sp_quote = quote.split(" ")
    charcount = 0
    charcount2 = 0
    tcharcount = 0
    
    quote1 = ""
    quote2 = ""
    for i in sp_quote:

        tcharcount = tcharcount + len(i)
        if tcharcount < len(quote)/2:
            charcount = charcount + len(i)
            if charcount > 25:
                i = i + "\n\n"
                charcount = 0
            quote1 = quote1 + " " + i
        else:
            charcount2 = charcount2 + len(i)
            if charcount2 > 25:
                i = i + "\n\n"
                charcount2 = 0
            quote2 = quote2 + " " + i
    
    return quote1,quote2



#               Merge Video

def merge_video(fps, duration,image, quote1,quote2):
    # make sure the image is in 1080x1920 resolution
    clip = ImageClip(image).set_duration(duration).set_fps(fps).set_pos("center")
    
    
    rez_clip = CompositeVideoClip([clip], size=(1080,1920), )
    rez_clip = rez_clip.resize(lambda t: 1 + 0.04 * t)  # Zoom-in effect


# timing the effect
    rez_clip1 = rez_clip.subclip(0,duration/2)
    rez_clip2 = rez_clip.subclip(duration/2,duration)


# the text clips
# Text 1
    text1 = TextClip(quote1,fontsize=64, font="Arial Bold", color="White").set_duration(duration/2)
    text1 = text1.set_position("center")
# Text 2   
    text2 = TextClip(quote2,fontsize=64, font="Arial Bold", color="White").set_duration(duration/2)
    text2 = text2.set_position("center")


# the background for the texts
# Text 1 Background
    color1 = ColorClip(size=(int(text1.w*1.1), int(text1.h*1.5)), color=(0, 0, 0)).set_duration(duration/2)
    color1 = color1.set_opacity(1)
    color1 = color1.set_position("center")
    color1 = color1.margin(left=10, right=10, top=10, bottom=10, color=(255, 255, 0))

# Text 2 Background   
    color2 = ColorClip(size=(int(text2.w*1.1), int(text2.h*1.5)), color=(0, 0, 0)).set_duration(duration/2)
    color2 = color2.set_opacity(1)
    color2 = color2.set_position("center")
    color2 = color2.margin(left=10, right=10, top=10, bottom=10, color=(255, 255, 0))
    

# Subtitle = Background + Text
# Sub 1
    subtitle1 = CompositeVideoClip([color1,text1])
    subtitle1 = subtitle1.set_position("center")
# Sub 2
    subtitle2 = CompositeVideoClip([color2,text2])
    subtitle2 = subtitle2.set_position("center")

# Subtitle + Image
#1
    subtitle_clip1 = CompositeVideoClip([rez_clip1,subtitle1], size=(1080,1920)).set_duration(duration/2)
#2
    subtitle_clip2 = CompositeVideoClip([rez_clip2,subtitle2], size=(1080,1920)).set_duration(duration/2)
    
# Final Video
    video_clip = concatenate_videoclips([subtitle_clip1,subtitle_clip2]).set_duration(duration)
    video_clip = video_clip.set_duration(duration)

# Export the video
    video_clip.write_videofile("visual/output.mp4", fps=fps, codec='h264_nvenc', threads=12, preset="fast", )





if __name__ == "__main__":

    photoname = "visual/bgImg.jpg"
    
    content = get_quote()
    

    duration = len(content.split(" "))/180 * 60
    if duration < 10:
        duration = 10
    print(duration)

    # get_photo(client_id, client_secret, user_agent, username, password, "EarthPorn", photoname)
    quote1, quote2 = split_quote(content)
    # audio = get_music(music)

    merge_video(75, duration, photoname, quote1, quote2)
    
 
