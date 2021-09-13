import PySimpleGUI as sg
sg.theme('Light Blue 2')

layout = [[sg.Text('Folder for blob detection ')],
         [sg.Text('Path for folder ', size=(8, 1)), sg.Input(key='-USERFOLDER-'), sg.FolderBrowse(target='-USERFOLDER-')],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('folder ', layout)

event, values = window.read()
window.close()
#print(f'You clicked {event}')
#print(f'You chose filenames {values[0]}')

folder = values['-USERFOLDER-']
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
train_path=next(os.walk(folder))[2]
train_ids=sorted(train_path)
#print(train_ids)
for filename in train_ids:
    mId=filename.split('.')[0]
    print(filename)
    image = cv2.imread(folder+'/'+mId+'.jpg') 
    low=np.array([0,0,0])
    high=np.array([200,200,200])
    imm=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(imm,low,high)
    ime=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("hjgjh",mask)
    #imgplot = plt.imshow(mask)
    #plt.show()
    img2_fg = cv2.bitwise_and(mask,ime)
    #imgplot = plt.imshow(img2_fg)
    #plt.show()
    img_contours, hierarchy = cv2.findContours(img2_fg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(ime, img_contours, -1, (0, 255, 0))
    #cv2.imshow('Image Contours', image)
    BLACK_THRESHOLD = 200
    THIN_THRESHOLD = 100
    idx = 0
    root_ext = os.path.splitext(filename) 
    path = os.path.join(folder+'/', root_ext[0]) 
    try:  
        os.mkdir(path)  
    except OSError as error:  
        print(error)   
    for cnt in img_contours:
        area = cv2.contourArea(cnt)
        if area > 9000:
            idx += 1
            # Find length of contours
            param = cv2.arcLength(cnt, True)
            # Approximate what type of shape this is
            approx = cv2.approxPolyDP(cnt, 0.01 * param, True)
            cv2.drawContours(ime, cnt, -1, (255, 255, 0), 10)
            x, y, w, h = cv2.boundingRect(cnt)
            #shape, x, y, w, h = find_shape(approx)
            roi = image[y:y + h, x:x + w]
            #x, y, w, h = cv2.boundingRect(cnt)
            #epsilon = 0.1*cv2.arcLength(cnt,True)
            #approx = cv2.approxPolyDP(cnt,epsilon,True)
            #roi = ime[y:y + h, x:x + w]
            if h < THIN_THRESHOLD or w < THIN_THRESHOLD:
                continue
            #path = 'Documents/AWS_IMG/'
            #cv2.imwrite(os.path.join(path , filename+str(idx) + '.jpg'), roi)
            cv2.imwrite(os.path.join(path , filename+"%d.jpg" % idx), image)
            #cv2.imwrite(filename+str(idx) + '.jpg', roi)
            cv2.rectangle(ime, (x, y), (x + w, y + h), (200, 0, 0), 2)
    #imgplot = plt.imshow(image)
    #plt.show()
    #cv2.imshow('img', ime)
    import PySimpleGUI as sg
    import PySimpleGUI as sg
    import io
    from PIL import Image
    sg.theme('Light Blue 2')
    layout = [
        [sg.Output(key='-OUT-', size=(50, 10))],
            [sg.Image(key="-IMAGE-")],
    ]
    window = sg.Window("Image Viewer", layout,finalize=True,auto_close=True)
    #window = sg.Window('Image shape Analysis', layout, element_justification='center').finalize()
    window['-OUT-'].TKOut.output.config(wrap='word') # set Output element word wrapping

    cv2.imwrite("ime.jpg", ime)
    image = Image.open("ime.jpg")
    image.thumbnail((800, 800))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())
    while True:
        win, ev, val = sg.read_all_windows()
        if ev == sg.WIN_CLOSED:
            win.close()
            break
    window.close()
#cv2.waitKey(0)
cv2.waitKey(0)