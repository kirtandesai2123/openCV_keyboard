import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

keys = [["Q","w","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

finalText = ""

keyboard = Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x,y = button.pos
        w,h = button.size
        cv2.rectangle(img, button.pos, (x+w,y+h), (255,0,255), cv2.FILLED)
        cv2.putText(img, button.text, (x+20, y+65), 
                    cv2.FONT_HERSHEY_PLAIN,
                    4,(255,255,255),4)
    return img
class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []
for i in range (len(keys)):
            for j, key in enumerate(keys[i]):
                buttonList.append(Button([100*j+50, 100*i+50],key))

try:
    while cap.isOpened():
        success, img = cap.read()
        

        if not success or img is None:
            print("Frame is nor being captured!")
            continue
        img = cv2.flip(img,1)
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            lmlist = hand["lmList"] #list of 21 landMarks
            bbox = hand["bbox"] #BOUNDING BOX
            center = hand["center"] #center coordinates
            handType = hand["type"] 

            img = drawAll(img, buttonList)
        
            if lmlist:
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size
                    if x< lmlist[8][0] <x+w and y<lmlist[8][1]<y+h:
                        cv2.rectangle(img, button.pos, (x+w,y+h), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x+20, y+65), 
                        cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                        l, _, _ = detector.findDistance(lmlist[8][:2], lmlist[12][:2], img)
                        print(l)

                        if l<50:
                            keyboard.press(button.text)
                            cv2.rectangle(img, button.pos, (x+w,y+h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x+20, y+65), 
                            cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                            finalText += button.text
                            sleep(0.2)

        cv2.rectangle(img, (50,350), (700,450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 430), 
        cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)                   
                       

            


        '''handType = "Right" if handType == "Left" else "Left"
            cv2.putText(img, handType, (bbox[0], bbox[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)'''
        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  
finally:
    cap.release() 
    cv2.destroyAllWindows()