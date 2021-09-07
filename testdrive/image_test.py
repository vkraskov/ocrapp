from PIL import Image, ImageOps
import io
import os

#img = Image.open('testimage_small_color.jpg')
img = Image.open('testimage_medium_color.jpg')
thresh = 128
fn = lambda x : 255 if x > thresh else 0
img_bw = img.convert('L').point(fn, mode='1')
im1 = img_bw.save('test_out.jpg', "JPEG", quality=80, optimize=True, progressive=True)

