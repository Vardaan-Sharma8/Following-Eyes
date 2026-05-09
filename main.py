import pygame as pg
import cv2
import math

#Class for eyes and pupils
class ball:
    def __init__(self, x, y, radius, color) :
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.max_dist = 0
        self.start_pos = 0
        self.dist = []
        self.base_radius = radius

    def display(self) :
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

#Initializing and definining constants
pg.init()
running = True
screen = pg.display.set_mode((800, 600), pg.RESIZABLE)
WIDTH = pg.display.get_window_size()[0]
HEIGHT = pg.display.get_window_size()[1]

#Detecting the faces
haarCas = cv2.CascadeClassifier("FaceDet.xml")

#Accessing the camera
idx = 0
if idx is None:
    raise SystemExit("No camera found.")

cap = cv2.VideoCapture(idx)

cam_W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cam_H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
camHalf_W = cam_W // 2
camHalf_H = cam_H // 2

#Making the eyeballs
eyeL = ball(((WIDTH / 2) - 150), (HEIGHT / 2), 100, (255,255,255))
eyeR = ball(((WIDTH / 2) + 150), (HEIGHT / 2), 100, (255,255,255))

#Making the pupils
pupilL = ball((WIDTH / 2) - 150, (HEIGHT / 2), 10, (0,0,0))
pupilR = ball((WIDTH / 2) + 150, (HEIGHT / 2), 10, (0,0,0))

#Setting starting postions of the pupils
pupilL.start_pos = [((WIDTH / 2) - 150), (HEIGHT / 2)]
pupilR.start_pos = [((WIDTH / 2) + 150), (HEIGHT / 2)]

#Limiting the pupils in the eyeballs
pupilL.max_dist = eyeL.radius - pupilL.radius
pupilR.max_dist = eyeR.radius - pupilR.radius

#Function to give one point (likely the nose) on the face detected from the camera.
def camera():
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(1)
    if not ret:
        return None

    cv2.imshow("Camera", frame)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haarCas.detectMultiScale(frame, 1.3, 3) 
    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]  # take first face
    middle = [x + w // 2, y + h // 2]
    middle[0] = middle[0] - camHalf_W
    middle[1] = middle[1] - camHalf_H

#    for (x, y, w, h) in faces:
#        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#        middle = [x + w // 2, y + h // 2]
#        cv2.circle(frame, middle, 2, (255, 0, 0), 2)
 
    if len(middle) == 2 :
        return middle
    else :
        return None

def meth(pupil) :
    mid = camera()
    if mid is None :
        distX = pupil.x - pupil.start_pos[0]
        distY = pupil.y - pupil.start_pos[1]
        D = math.sqrt((distX**2)+(distY**2))
        if D >= 100 :
            ratio = 100 / D
            distX = distX * ratio
            distY = distY * ratio
        shrink_amount = (D / pupil.max_dist) * 2 
        pupil.radius = int(pupil.base_radius - shrink_amount)
        pupil.dist = [distX, distY]
    else :
        distX = (mid[0] * 100) / cam_W
        distY = (mid[1] * 100) / cam_H

        D = math.sqrt((distX ** 2) + (distY ** 2))
        if D > 100 :
            ratio = 100 / D
            distX = distX * ratio
            distY = distY * ratio
        shrink_amount = (D / pupil.max_dist) * 2
        pupil.radius = int(pupil.base_radius - shrink_amount)
        pupil.dist = [distX, distY]


#The "game" loop
while running :
    screen.fill((0,0,0))

    meth(pupilL)
    
    pupilL.x = pupilL.start_pos[0] - pupilL.dist[0]
    pupilL.y = pupilL.start_pos[1] + pupilL.dist[1]
    
    pupilR.x = pupilL.x + 300
    pupilR.y = pupilL.y
    
    pupilR.radius = pupilL.radius

    #Displaying the eyes and the pupils
    eyeL.display()
    eyeR.display()
    pupilL.display()
    pupilR.display()

    #Updating the screen
    pg.display.flip()
    #For quiting the window. (press q or the cross button)
    for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False

