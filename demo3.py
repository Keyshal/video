from  moviepy.editor import *
clipVideo =(VideoFileClip(r"/home/galieo/Videos/Screencasts/demo1.mp4").subclip(0,16).resize(0.6))
clipVideo.write_gif(r"/home/galieo/Videos/Screencasts/3.gif", fps=2)
