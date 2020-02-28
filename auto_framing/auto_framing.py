import cv2
import numpy as np
import os
from PyQt5 import QtCore
from PyQt5 import QtGui

def enquadramento(thresh):
    mold_area = thresh.shape[0]*thresh.shape[1]
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if mold_area*0.9>area>mold_area*0.1:
            x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(mold,(x,y),(x+w,y+h),(0,0,255),2)
    if w == 0 or h == 0:
        print('ERRO: Problema ao detectar enquadramento da moldura')
        return -1
    return x,y,w,h

def put_frame(img, mold):
    mold_h, mold_w, _ = mold.shape
    thresh = (255-mold[:,:,3])
    png = cv2.merge((thresh, thresh, thresh, thresh))
    x,y,w,h = enquadramento(thresh)
    # adiciona um canal a img
    img = np.dstack([img, np.ones((img.shape[0], img.shape[1]), dtype="uint8") * 255])
    img = cv2.resize(img,(w,h))
    ovr = np.zeros((mold_h,mold_w,4), dtype="uint8")
    ovr[y:y+h,x:x+w,:] = img

    dst = cv2.bitwise_and(mold, (255-png))
    dst2 = cv2.bitwise_and(ovr, png)
    dst3 = cv2.bitwise_or(dst, dst2)

    return dst3

def emoldurar(imgs_path):
    # mold_path = input('Digite o path da moldura:')
    # mold_path = "/home/samuel/workspace/moldura_automatica/molds/mold_1.png"
    if os.path.isfile(mold_path) and mold_path.split('.')[-1] == "png":
        mold = cv2.imread(mold_path, cv2.IMREAD_UNCHANGED)
    else:
        print("ERRO: verifique se o nome do arquivo está correto e tente novamente.\n")
        return -1

    # imgs_path = input('Digite o path da pasta de imagens:')
    # imgs_path = "testes"
    result_path = imgs_path+'/result'
    if not os.path.isdir(imgs_path):
        print("ERRO: Imagens não encontradas")
        return -1
    
    if not os.path.isdir(result_path):
        os.mkdir(result_path)

    imgs_list = os.listdir(imgs_path)
    for img_name in imgs_list:
        if img_name.split('.')[-1] == "JPG":
            img = cv2.imread(imgs_path+'/'+img_name)
            result = put_frame(img, mold)
            cv2.imwrite(result_path+'/'+img_name,result)
            # cv2.namedWindow("result",0)
            # cv2.imshow("result",result)
            # cv2.waitKey(1)

if __name__=="__main__":
    main()


