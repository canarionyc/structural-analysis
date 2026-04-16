from PIL import Image, ImageOps

img = Image.open(r"C:\dev\structural-analysis\Curved_beam\20260307_164104.jpg")
img = ImageOps.exif_transpose(img)  # applies the EXIF rotation and strips the tag
img.save(r"C:\dev\structural-analysis\Curved_beam\20260307_164104.jpg")