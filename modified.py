# error_type = 0, no t1c
# error_type = 1, no t2
# error_type = 2, have t1c with no overlap
# error_type = 3, have t2 with no overlap
# error_type = 4, t1c irregular
# error_type = 5, t2 irregular
# type = 6, regular
import os
import cv2
# open_csv_file
record_array = [[] for i in range(6)]

def calculate2(image_path):
    left, top, right, bottom = 0,0,0,0
    mat_img2 = cv2.imread(image_path,cv2.CV_8UC1)
    ret,thresh = cv2.threshold(mat_img2,47,255,cv2.THRESH_BINARY)
    # cv2.imshow("thresh", thresh)
    # cv2.waitKey(0)
    height,width = thresh.shape
    for i in range(height):
        for j in range(width):
            if thresh[i][j]==0:continue
            # if i<left and j<top:
            #     left = i
            #     top = j
            # if i>right and j>bottom:
            #     right = i
            #     bottom = j
            if i<left:left = i
            if j<top:top = j
            if i>right:right = i
            if j>bottom:bottom = j
    return (right-left)*(bottom-top)


def calculate(image_path):
    #读取文件
    mat_img = cv2.imread(image_path)
    mat_img2 = cv2.imread(image_path,cv2.CV_8UC1)

    #自适应分割
    # dst = cv2.adaptiveThreshold(mat_img2,20,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,3,10)
    ret,thresh1 = cv2.threshold(mat_img2,47,255,cv2.THRESH_BINARY)
    #提取轮廓
    # contours,heridency = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours,heridency = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #标记轮廓
    cv2.drawContours(mat_img,contours,-1,(255,0,255),3)

    #计算轮廓面积
    area = 0
    for i in contours:
        area += cv2.contourArea(i)
    return area

def output_pix_matrix(image_path):
    mat_img2 = cv2.imread(image_path,cv2.CV_8UC1)
    # file = open("simple.txt",'w')
    # file.write(str(mat_img2))
    # file.close()
    height,width=mat_img2.shape
    file=open('simple.txt','w')
    for i in range(height):
        for j in range(width):
            file.write(str(mat_img2[i,j]))
            file.write(" ")
        file.write('\n')
    file.close()

def show_contour(image_path):
    # img=cv2.imread(image_path)
    # GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.imread(image_path,cv2.CV_8UC1)
    ret,thresh1 = cv2.threshold(img,47,255,cv2.THRESH_BINARY)
    contours,heridency = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,125,3)  
    cv2.imshow("img", img)  
    cv2.waitKey(0)

def show_image_pixel(image_path):
    pixel_dict = {}
    img = cv2.imread(image_path,cv2.CV_8UC1)
    height,width=img.shape
    for i in range(height):
        for j in range(width):
            pixel = img[i][j]
            if pixel not in pixel_dict:
                pixel_dict[pixel] = 0
            pixel_dict[pixel] = pixel_dict[pixel]+1
    pixel_dict = sorted(pixel_dict.items(), key=lambda x: x[1])
    print(pixel_dict)


def scan():
    abspath = "C:/Users/viole/Desktop/meningioma"
    dirs = os.listdir(abspath)
    for dir in dirs[1:]:
        if not dir.isdigit():continue
        t1c_path = ''.join([abspath,"/",dir,"/t1c"])
        t2_path = ''.join([abspath,"/",dir,"/t2"])
        t1c_overlap_path = ''.join([abspath,"/",dir,"/t1c/overlap"])
        t2_overlap_path = ''.join([abspath,"/",dir,"/t2/overlap"])
        if not os.path.isdir(t1c_path):
            record_array[0].append([dir,"error_type = 0, no t1c"])
        if os.path.isdir(t1c_path) and not os.path.isdir(t1c_overlap_path):
            record_array[2].append([dir,"error_type = 2, have t1c with no overlap"])
        for p, dirs, fns in os.walk(t1c_overlap_path):
            first_image_path = ''.join([p,"/",fns[0]])
            last_image_path = ''.join([p,"/",fns[len(fns)-1]])
            first_image_area = calculate2(first_image_path)
            last_image_area = calculate2(last_image_path)
            if first_image_area-last_image_area>10000:
                print("t1c_overlap_path:dir:",dir)
                print("t1c_overlap_path:first_image_area:",first_image_area)
                print("t1c_overlap_path:last_image_area:",last_image_area,"\n")
                record_array[4].append([dir,"error_type = 4, t1c irregular"])
        if not os.path.isdir(t2_path):
            record_array[1].append([dir,"error_type = 1, no t2"])
        if os.path.isdir(t2_path) and not os.path.isdir(t2_overlap_path):
            record_array[3].append([dir,"error_type = 3, have t2 with no overlap"])
        for p, dirs, fns in os.walk(t2_overlap_path):
            first_image_path = ''.join([p,"/",fns[0]])
            last_image_path = ''.join([p,"/",fns[len(fns)-1]])
            first_image_area = calculate2(first_image_path)
            last_image_area = calculate2(last_image_path)
            if first_image_area-last_image_area>10000:
                print("t2_overlap_path:dir:",dir)
                print("t2_overlap_path:first_image_area:",first_image_area)
                print("t2_overlap_path:last_image_area:",last_image_area,"\n")
                record_array[5].append([dir,"error_type = 5, t2 irregular"])
if __name__ == "__main__":
    # show_image_pixel("C:/Users/viole/Desktop/meningioma/10320470/T1C/overlap/10320470_0001.png")
    # show_image_pixel("C:/Users/viole/Desktop/meningioma/10320470/T1C/overlap/10320470_0020.png")
    # show_contour("C:/Users/viole/Desktop/meningioma/10320470/T1C/overlap/10320470_0001.png")
    # show_contour("C:/Users/viole/Desktop/meningioma/10320470/T1C/overlap/10320470_0020.png")
    # print(calculate2("C:/Users/viole/Desktop/meningioma/10320470/T1C/overlap/10320470_0001.png"))
    # print(calculate2("C:/Users/viole/Desktop/meningioma/10320470/T1C/overlap/10320470_0020.png"))
    scan()
    file=open('data.txt','w')
    for i in range(6):
        for j in range(len(record_array[i])):
            file.write(str(record_array[i][j]))
            file.write("\n")
        file.write("\n")
    file.close()