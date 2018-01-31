import sys
import os
import numpy as np
import cv2

def main(basepic, picdir):
    MIN_MATCH_COUNT = 10
    files = os.listdir(picdir)
    files = list((sorted(filter(lambda a: a.lower().endswith('jpg') or a.lower().endswith('jpeg') or a.lower().endswith('png'), files))))
    img2 = cv2.imread(basepic, 0)
    sz = img2.shape
    savedir = picdir+'alignedImages/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    #endif

    for picpath in files:
        if(basepic == picdir+picpath):
            cv2.imwrite(savedir+picpath, cv2.imread(picdir+picpath))
            pass
        #endif

        # Load the image in gray scale
        img1 = cv2.imread(picdir+picpath,0)

        # Detect the SIFT key points and compute the descriptors for the two images
        sift = cv2.xfeatures2d.SIFT_create()
        keyPoints1, descriptors1 = sift.detectAndCompute(img1, None)
        keyPoints2, descriptors2 = sift.detectAndCompute(img2, None)

        # Create brute-force matcher object
        bf = cv2.BFMatcher()

        # Match the descriptors
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)

        # Select the good matches using the ratio test
        goodMatches = []

        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                goodMatches.append(m)

        # Apply the homography transformation if we have enough good matches
        if len(goodMatches) > MIN_MATCH_COUNT:
            # Get the good key points positions
            sourcePoints = np.float32([ keyPoints1[m.queryIdx].pt for m in goodMatches ]).reshape(-1, 1, 2)
            destinationPoints = np.float32([ keyPoints2[m.trainIdx].pt for m in goodMatches ]).reshape(-1, 1, 2)

            # Obtain the homography matrix
            M, mask = cv2.findHomography(sourcePoints, destinationPoints, method=cv2.RANSAC, ransacReprojThreshold=5.0)
            matchesMask = mask.ravel().tolist()
            # print(M)

            # Apply the perspective transformation to the source image corners
            h, w = img1.shape
            corners = np.float32([ [0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0] ]).reshape(-1, 1, 2)
            transformedCorners = cv2.perspectiveTransform(corners, M)

            # Draw a polygon on the second image joining the transformed corners
            img2 = cv2.polylines(img2, [np.int32(transformedCorners)], True, (255, 255, 255), 2, cv2.LINE_AA)

            # im_aligned = cv2.warpPerspective (cv2.imread('sequences/test/IMG_6150.jpeg'), M, (sz[1],sz[0]), flags=cv2.INTER_LINEAR)
            im_aligned = cv2.warpPerspective (cv2.imread(picdir+picpath), M, (sz[1],sz[0]), flags=cv2.INTER_LINEAR)
            # flags=cv2.INTER_NEAREST + cv2.WARP_INVERSE_MAP
            # M is the Homography Matrix
            # cv2.imshow('TransformationMaybe', im_aligned)
            cv2.imwrite(savedir+picpath, im_aligned)
        else:
            print("Not enough matches are found - %d/%d" % (len(goodMatches), MIN_MATCH_COUNT))
            matchesMask = None
        # endif
        
        # # Draw the matches
        # drawParameters = dict(matchColor=(0, 255, 0), singlePointColor=None, matchesMask=matchesMask, flags=2)
        # result = cv2.drawMatches(img1, keyPoints1, img2, keyPoints2, goodMatches, None, **drawParameters)

        # # Display the results
        # cv2.imshow('Homography', result)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    #endfor
#enddef main



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if sys.argv[2].endswith('/') else sys.argv[2]+'/')
#endif
