from pywebio import start_server
from pywebio import output

from pywebio import input
from pywebio.output import put_scope, put_scrollable




import threading
import time
from collections import deque

import numpy as np
import cv2

class Cideo(object):
    def __init__(self,output_video_path,weight,height):
        self.shape=(weight,height)

        self.output_fps = 30
        self.output_video_path=output_video_path
        self.video_writer = cv2.VideoWriter(
            self.output_video_path,
            # cv2.VideoWriter_fourcc(*'MP4V'),
            # cv2.VideoWriter_fourcc(*'XVID'),
            cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
            # cv2.VideoWriter_fourcc('I', '4', '2', '0'),
            # cv2.VideoWriter_fourcc('M','J','P','G'), # https://docs.opencv.org/master/dd/d43/tutorial_py_video_display.html
            self.output_fps,  # fps 每秒的帧数
            self.shape,  # resolution
            True
        )


def receive_video(cap,q,lock1):

    while cap.isOpened():



        lock1.acquire()
        ok, image = cap.read()
        if ok:
            if len(q) >= 8:
                q.popleft()
            else:
                q.append(image)
        else:
            break
        lock1.release()
        time.sleep(0.01)
    cap.release()

def detect_frame(cap,q,lock1,ideo,countlist):
    count=0
    while cap.isOpened():
        if len(q) == 0:
            time.sleep(0.01)

        else:

            lock1.acquire()
            image = q.pop()
            lock1.release()
            count=count+1
            if count%10==0:
                ideo.video_writer.write(image)

            print(count)
            countlist.append(count)
        if count==474:
            ideo.video_writer.release()
            cv2.destroyAllWindows()
            break




        time.sleep(0.01)




def main1():
    q = deque([], 3)
    source = '/home/galieo/Videos/Screencasts/demo1.mp4'
    cap = cv2.VideoCapture(source)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    lock1 = threading.Lock()
    result=''
    output_video_path = "/home/galieo/Videos/Screencasts/demo3.mp4"

    ideo=Cideo(output_video_path,width,height)
    countlist=[]

    # start_server(user_output_component, debug=True, port=8800)




    p1 = threading.Thread(target=receive_video,args=(cap,q,lock1))
    p2 = threading.Thread(target=detect_frame,args=(cap,q,lock1,ideo,countlist))
    p1.daemon = True
    p2.daemon = True
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    return countlist


# if __name__=="__main__":
#     main()


def user_output_component():
    # tmpfile='import os, time \nfrom pywebio.input import NUMBER, TEXT'
    with open("/home/galieo/Downloads/visualize.py",'r') as ff:
        # tmpfile = ff.readlines()
        tmpfile=ff.read()


    output.put_column([

    output.put_code(tmpfile, language='python', rows=10)])

    # output.put_button(label='put button demo', onclick=lambda: main1(countlist), color='dark', outline=True, disabled=False)
    # print("hahah------------")
    select_res = input.select("please select your city:", ['代码1', '代码2', '代码3'])
    if select_res=="代码1":
        countlist=main1()

        output.put_scrollable(put_scope('scrollable'), height=200, keep_bottom=True)
        for i in countlist:

            output.put_text(str(i), scope='scrollable')
    elif select_res=="代码2":
        countlist = main1()

        output.put_scrollable(put_scope('scrollable'), height=200, keep_bottom=True)
        for i in countlist:
            output.put_text(str(i), scope='scrollable')
    else:
        countlist = main1()

        output.put_scrollable(put_scope('scrollable'), height=200, keep_bottom=True)
        for i in countlist:
            output.put_text(str(i), scope='scrollable')


    print('your city is:', select_res)
    # output.put_text(str(88))
    # text_res = input.textarea("please input what you want to say:", rows=3, placeholder='...')
    # print('what you said is:', text_res)

if __name__ == '__main__':
    start_server(user_output_component, debug=True, port=8800)



