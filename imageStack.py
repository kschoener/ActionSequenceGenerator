import sys
import os
from PIL import Image
from PIL import ImageChops


def main(pics):
    files = os.listdir(pics)
    files = list((sorted(filter(lambda a: a.lower().endswith('jpg') or a.lower().endswith('jpeg') or a.lower().endswith('png'), files))))
    # print(files)
    minValue = 75
    # minValue = 0
    finalPic = None
    finalMap = None
    for picIndex in range(1,len(files)):
        image1 = Image.open(pics+files[picIndex+1 if picIndex+1 != len(files) else 0])
        image2 = Image.open(pics+files[picIndex])
        if picIndex == 1:
            finalPic = Image.new(image1.mode, image1.size)
            finalMap = finalPic.load()
        #endif

        image = ImageChops.difference(image2, image1)

        mask1 = Image.eval(image, lambda pixelValue: 0 if pixelValue < minValue else 255) # should probably skip this step or return pixelValue
        differences = mask1.load()

        im1map = image1.load()
        im2map = image2.load()

        for i in range(image1.width):
            for j in range(image1.height):
                if sum(differences[i,j]) != 0:
                    finalMap[i,j] = im2map[i,j]
                elif picIndex == 1:
                    finalMap[i,j] = im1map[i,j]
                #endif
            #endfor
        #endfor
        # finalPic.show()
    #endfor
    if not os.path.exists('outputs/'):
        os.makedirs('outputs/')
    #endif
    finalPic.save('outputs/'+str(pics.split('/')[-2])+'.jpg', 'jpeg')
    finalPic.show()
#enddef main





if __name__ == '__main__':
    # print('Hello. This is my final project.')
    if len(sys.argv) > 1:
        main(sys.argv[1] if sys.argv[1].endswith('/') else sys.argv[1]+'/')
    else:
        main('.')
    # endif
# endif
