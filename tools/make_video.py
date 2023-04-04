import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from os.path import join
import PIL
from PIL import ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip

# get realpath of current directory
wd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(wd)
problem_id = 27


def create_image_by_plt():
    img = mpimg.imread(join(wd, 'image.png'))

    # set image size
    h, w, dpi = 1080, 1920, 100
    figure = plt.figure(figsize=(h/dpi, w/dpi), dpi=100)
    figure.patch.set_facecolor('black')
    # set background to black
    plot = plt.imshow(img, extent=[0, 1080, 0, 1024])
    plt.axis('off')
    # plt.title(r'$\alpha > \beta$')
    # plt.text(x=10/dpi, y=-100, s=r"$\frac{x^2 + 2x + 7}{2} > \beta$", color="white", fontsize=36)
    plt.text(x=10/dpi, y=-100, s="As Sarah was playing basketball with her friends,\nshe realized that the ball they were using had a unique shape.\nCan you help her identify the shape of a basketball?", color="white", fontsize=22)
    # plt.text(x=10/dpi, y=10/dpi, s="engmaths4kids", color="white", fontsize=100)

    plt.rcParams['axes.facecolor'] = 'black'
    plt.savefig(join(wd, 'image_final.png'))


class Colors:
    Black = (0, 0, 0)


class Fonts:
    font_path = join(pd, "assets", 'fonts', "Roboto", 'Roboto-Regular.ttf')
    Heading = ImageFont.truetype(font_path, 36)
    Text = ImageFont.truetype(font_path, 30)
    Options = ImageFont.truetype(font_path, 36)


def create_image_by_pil():
    W, H = 1080, 1920
    img = PIL.Image.new(mode="RGB", size=(W, H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    message = "engmath4kids"
    _, _, w, h = draw.textbbox((0, 0), message, font=Fonts.Heading)

    fontColor = (0, 0, 0)
    draw.text(((W-w)/2, 100), message, font=Fonts.Heading, fill=fontColor)

    draw.text((329, 1149),
              "Problem 6: Sharing is Caring",
              font=Fonts.Text,
              fill=Colors.Black)

    text = """\
Samantha and Jack are classmates who love to share their
snacks
during recess.
Samantha has 3 apples and her friend Jack gives her 2 more.
How many apples does Samantha have in total?\
"""
    draw.text((28, 1235), text, font=Fonts.Text, fill=Colors.Black)

    text = "A. 2    B. 3    C. 7    D. 5"
    draw.text((395, 1457), text, font=Fonts.Options, fill=Colors.Black)

    picture = PIL.Image.open(join(wd, 'image.png'))
    img.paste(picture, (28, 70))
    img.save(join(wd, "image_final.png"))


def create_video_frame_image():
    pass


def make_sound():
    global problem_id
    text = """\
Problem 27: Passing the Baton
Tom, Emily, John, and Sarah are on the school's relay race team.
Each runner will run a distance of 400 meters before passing the baton to the next runner.
Tom runs 1 kilometer in 7 minutes 30 seconds, Emily in 8 minutes 45 seconds, John in 10 minutes, and Sarah in 11 minutes 15 seconds.

How long (in seconds) will it take the team to complete the entire 1600-meter relay race?
"""
    tts = gTTS(text=text, lang='en')

    tts.save(join(wd, f"{problem_id}.wav"))


def make_video():
    VIDEO_DURATION = 40
    global problem_id
    id = problem_id
    image_clip = ImageClip(join(wd, f"problem_{id}.png")).set_duration(VIDEO_DURATION)
    bg_files = [
        "cute_bg.mp3",
        "bg_cute_funny_cat_1pGgn9rfGZU.mp3",
        "bg_cute_furry_friends_79w0HiP0uA0.mp3",
        "bg_cute_cutest_bunny_UeKehu5DE0Y.mp3",
        "bg_cute_hide_and_seek_ktBjO98Zm6U.mp3",
        "bg_cute_happy_footstesp_RYsDvuSd-OA.mp3",
    ]
    bg_file = bg_files[5]
    bg_audio = AudioFileClip(join(wd, bg_file)).set_duration(VIDEO_DURATION).set_start(0).volumex(0.2).audio_fadein(0.5).audio_fadeout(2).audio_fadeout(2)
    transcript_audio = AudioFileClip(join(wd, f"{id}.wav")).set_start(0.5)
    audio = CompositeAudioClip([transcript_audio, bg_audio])

    video = image_clip.set_audio(audio)
    video.fps = 30
    video.write_videofile(join(wd, f"{id}.mp4"))


if __name__ == '__main__':
    # create_image_by_plt()
    # create_image_by_pil()
    # make_sound()
    make_video()
