
video = 'GarethDavies.mp4'
text = '#rugby'


from instapy_cli import client
import cv2



username = 'therugbyvault'
password = 'Warner2001!'
cookie_file = 'therugbyvault.json' # default: `USERNAME_ig.json`

with client(username, password, cookie_file=cookie_file, write_cookie_file=True) as cli:
    # get string cookies
    cookies = cli.get_cookie()
    print(type(cookies)) # == str
    print(cookies)
    # do stuffs with cli
    # import pdb
    # pdb.set_trace()
    ig = cli.api()
    #me = ig.current_user()
    # print(me)



    file_path = "GarethDavies.mp4"  # change to your own video path
    vid = cv2.VideoCapture(file_path)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps = vid.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    

    ig.post_video("GarethDavies.mp4", (720, 720), duration, "GarethDavies.mp4")