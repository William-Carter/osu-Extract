from PIL import Image
import os 
dirPath = os.path.dirname(os.path.realpath(__file__))
def getAlbumArt(songObject):
    size = (512,512)
    im = Image.open(songObject.metadata["Background"])

    width, height = im.size

    left = (width-height)/2
    right = (width-height)/2+height
    top = 0
    bottom = height

    im1 = im.crop((left, top, right, bottom))
    im1.thumbnail(size)
    rgbIm = im1.convert("RGB")
    rgbIm.save(dirPath+"/temp/%s.jpg" % songObject.metadata["Title"], "JPEG" )