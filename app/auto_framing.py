import cv2
import numpy as np
import os

def detectar_enquadramento(thresh):
    mold_area = thresh.shape[0]*thresh.shape[1]
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if mold_area*0.9>area>mold_area*0.1:
            x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(mold,(x,y),(x+w,y+h),(0,0,255),2)
    if w == 0 or h == 0:
        raise Exception('ERRO: Problema ao detectar enquadramento da moldura')
    return x,y,w,h

def correcao_tamanho(img, w,h):
    new_img_w = int(h*(img.shape[1]/img.shape[0]))
    if new_img_w<w:
        # iguala a largura e ajusta a altura
        new_img_w = w
        new_img_h = int(w*(img.shape[0]/img.shape[1]))
        img = cv2.resize(img,(new_img_w,new_img_h))
        dif_h = int((new_img_h-h)/2)
        # recorta o excedente da altura
        img = img[dif_h:-dif_h,:,:]

    else:
        # iguala a altura e ajusta a largura
        new_img_h = h
        img = cv2.resize(img,(new_img_w,new_img_h))
        dif_w = int((new_img_w-w)/2)
        # recorta o excedente da largura
        img = img[:,dif_w:-dif_w,:]
    
    img = cv2.resize(img,(w,h))
    return img

def put_frame(img, mold):
    mold_h, mold_w, _ = mold.shape
    thresh = (255-mold[:,:,3])
    png = cv2.merge((thresh, thresh, thresh, thresh))
    x,y,w,h = detectar_enquadramento(thresh)
    # adiciona um canal a img
    img = np.dstack([img, np.ones((img.shape[0], img.shape[1]), dtype="uint8") * 255])
    img = correcao_tamanho(img,w,h)
    ovr = np.zeros((mold_h,mold_w,4), dtype="uint8")

    ovr[y:y+h,x:x+w,:] = img
    dst = cv2.bitwise_and(mold, (255-png))
    dst2 = cv2.bitwise_and(ovr, png)
    dst3 = cv2.bitwise_or(dst, dst2)

    return dst3

def emoldurar(imgs_path):
    if os.path.isfile(mold_path) and mold_path.split('.')[-1] == "png":
        mold = cv2.imread(mold_path, cv2.IMREAD_UNCHANGED)
    else:
        print("ERRO: verifique se o nome do arquivo está correto e tente novamente.\n")
        return -1
    result_path = imgs_path+'/result'
    if not os.path.isdir(imgs_path):
        print("ERRO: Imagens não encontradas")
    
    if not os.path.isdir(result_path):
        os.mkdir(result_path)

    imgs_list = os.listdir(imgs_path)
    for img_name in imgs_list:
        if img_name.split('.')[-1] == "JPG" or img_name.split('.')[-1] == "jpg" or img_name.split('.')[-1] == "png":
            print("Carregando: "+imgs_path+'/'+img_name+"\n")
            img = cv2.imread(imgs_path+'/'+img_name)
            if img is not None:
                result = put_frame(img, mold)
                cv2.imwrite(result_path+'/'+img_name,result)
            else:
                print("ERRO: ao carregar imagem"+imgs_path+'/'+img_name+"\n")

if __name__=="__main__":
    main()


