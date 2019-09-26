from PIL import Image
import argparse
from imutils import paths
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
args = vars(ap.parse_args())

imagePaths = sorted(list(paths.list_images(args["dataset"])))
for imPath in imagePaths:
    if imPath[-4:] == '.png':
        # imName = imPath[imPath.rfind("\\")+1:-4]
        im = Image.open(imPath)
        rgb_im = im.convert('RGB')
        rgb_im.save(imPath[:-4] + '.jpg')
        os.remove(imPath)
