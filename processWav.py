from features import mfcc
import cv2
import numpy as np

def writeMFCC(data, samp, fpath=None):


    mfcc_feat = mfcc(data,samp)
    mMin = mfcc_feat.min()
    mMax = mfcc_feat.max()
    mfcc_feat -= mMin
    mfcc_feat *= 255/mfcc_feat.max()

    outImg = np.array(mfcc_feat, np.uint8)

    if fpath != None:
        cv2.imwrite(fpath, outImg)
    
    return outImg

