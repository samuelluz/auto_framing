import cv2
import numpy as np
import os

def detectar_enquadramento(mold):
    mold_thresh = (255-mold[:,:,3])
    mold_png = cv2.merge((mold_thresh, mold_thresh, mold_thresh, mold_thresh))
    mold_area = mold_thresh.shape[0]*mold_thresh.shape[1]
    contours, hierarchy = cv2.findContours(mold_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    molds_bboxs = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if mold_area*0.9>area>mold_area*0.1:
            x,y,w,h = cv2.boundingRect(cnt)
            if w == 0 or h == 0:
                raise Exception('ERRO: Problema ao detectar enquadramento da moldura')
            molds_bboxs.append([x,y,w,h])
            # cv2.rectangle(mold,(x,y),(x+w,y+h),(0,0,255),2)
    return molds_bboxs, mold_png

def correcao_tamanho(img, w, h):
    new_img_w = int(h*(img.shape[1]/img.shape[0]))
    if new_img_w<w:
        # iguala a largura e ajusta a altura
        new_img_w = w
        new_img_h = int(w*(img.shape[0]/img.shape[1]))
        img = cv2.resize(img,(new_img_w,new_img_h))
        dif_h = int((new_img_h-h)/2)
        # recorta o excedente da altura
        if dif_h>0:
            img = img[dif_h:-dif_h,:,:]

    else:
        # iguala a altura e ajusta a largura
        new_img_h = h
        img = cv2.resize(img,(new_img_w,new_img_h))
        dif_w = int((new_img_w-w)/2)
        # recorta o excedente da altura
        if dif_h>0:
            img = img[dif_h:-dif_h,:,:]
    
    img = cv2.resize(img,(w,h))
    return img

def put_frame(img, result, mold_bbox, mold_png):
    mold_h, mold_w, _ = mold_png.shape
    bbox_x, bbox_y, bbox_w, bbox_h = mold_bbox
    img = correcao_tamanho(img, bbox_w, bbox_h)
    zeros_mold = np.zeros((mold_h,mold_w, 4), dtype="uint8")
    zeros_mold[bbox_y:bbox_y+bbox_h, bbox_x:bbox_x+bbox_w,:] = img

    zeros_mold[:,:,3] = zeros_mold[:,:,3]*(mold_png[:,:,3]/255)
    zeros_mold[:,:,2] = zeros_mold[:,:,2]*(mold_png[:,:,3]/255)
    zeros_mold[:,:,1] = zeros_mold[:,:,1]*(mold_png[:,:,3]/255)
    zeros_mold[:,:,0] = zeros_mold[:,:,0]*(mold_png[:,:,3]/255)

    dst2 = cv2.bitwise_or(result, zeros_mold)
    return dst2

def emoldurar(imgs_path):
    if os.path.isfile(mold_path) and mold_path.split('.')[-1] == "png":
        mold = cv2.imread(mold_path, cv2.IMREAD_UNCHANGED)
        mold[:,:,2] = mold[:,:,2]*(mold[:,:,3]/255)
        mold[:,:,1] = mold[:,:,1]*(mold[:,:,3]/255)
        mold[:,:,0] = mold[:,:,0]*(mold[:,:,3]/255)
        mold_bboxs, mold_png = detectar_enquadramento(mold)
    else:
        print("ERRO: verifique se o nome do arquivo está correto e tente novamente.\n")
        return -1
    result_path = imgs_path+'/result'
    if not os.path.isdir(imgs_path):
        print("ERRO: Imagens não encontradas")
    
    if not os.path.isdir(result_path):
        os.mkdir(result_path)

    imgs_list = os.listdir(imgs_path)
    imgs_list.sort()
    complete = False
    result = mold
    num_frames_put = 0
    for i, img_name in enumerate(imgs_list):
        if img_name.split('.')[-1] == "JPG" or img_name.split('.')[-1] == "jpg" or img_name.split('.')[-1] == "jpeg" or img_name.split('.')[-1] == "png":
            print("Carregando: "+imgs_path+'/'+img_name+"\n")
            img = cv2.imread(imgs_path+'/'+img_name)
            # adiciona um canal a img
            img = np.dstack([img, np.ones((img.shape[0], img.shape[1]), dtype="uint8") * 255])

            if img is not None:
                mold_bbox = mold_bboxs.pop(0)
                mold_bboxs.append(mold_bbox)

                try:
                    result = put_frame(img, result, mold_bbox, mold_png)
                except Exception as err:
                    print(err)
                    print("ERRO: ao emoldurar imagem"+imgs_path+'/'+img_name+"\n")
                    break
                num_frames_put += 1
                if num_frames_put == len(mold_bboxs):
                    # cv2.imshow("result", result)
                    # cv2.waitKey(0)
                    cv2.imwrite(result_path+'/'+img_name, result)
                    num_frames_put = 0
                    result = mold

                elif i == len(imgs_list)-1:
                    # Se a ultima imagem não completar a moldura
                    mold_bbox = mold_bboxs.pop(0)
                    mold_bboxs.append(mold_bbox)
                    img = cv2.imread(imgs_path+'/'+imgs_list[0])
                    # adiciona um canal a img
                    img = np.dstack([img, np.ones((img.shape[0], img.shape[1]), dtype="uint8") * 255])
                    try:
                        result = put_frame(img, result, mold_bbox, mold_png)
                    except Exception as err:
                        print(err)
                        print("ERRO: ao emoldurar imagem"+imgs_path+'/'+img_name+"\n")
                        break
                    # cv2.imshow("result", result)
                    # cv2.waitKey(0)
                    cv2.imwrite(result_path+'/'+img_name, result)


            else:
                print("ERRO: ao carregar imagem"+imgs_path+'/'+img_name+"\n")

if __name__=="__main__":
    # mold_path = "/Users/samuelluzgomes/Pictures/Moldura-Foto.png"
    mold_path = "/Users/samuelluzgomes/Documents/workspace/auto_framing/molds/MoldPolaroide.png"
    emoldurar("/Users/samuelluzgomes/Pictures")