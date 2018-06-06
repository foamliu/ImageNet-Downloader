import cv2 as cv
import os

if __name__ == '__main__':
    image_folder = '/mnt/code/ImageNet-Downloader/image/resized'
    names = [n for n in os.listdir(image_folder) if n.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tiff'))]

    for name in names:
        try:
            filename = os.path.join(image_folder, name + '.jpg')
            # b: 0 <=b<=255, g: 0 <=g<=255, r: 0 <=r<=255.
            bgr = cv.imread(filename)
            # bgr = cv.resize(bgr, (img_rows, img_cols), cv.INTER_CUBIC)
            gray = cv.imread(filename, 0)
            # gray = cv.resize(gray, (img_rows, img_cols), cv.INTER_CUBIC)
            lab = cv.cvtColor(bgr, cv.COLOR_BGR2LAB)
        except:
            print('Error: {}'.format(name))
