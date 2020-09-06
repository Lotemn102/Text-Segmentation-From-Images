import cv2
import numpy as np

# Clean image background and sharpen text.
def sharpen_text(img):
    # Check if image is already in gray scale.
    try:
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        imgray = img

    # Blurring the image before and after threshold seems to have better
    # results.
    imgBlur = cv2.medianBlur(imgray, 3, 0)
    _, imgBin = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_OTSU)
    img = cv2.blur(imgBin, (1, 1))

    return img

# Find contours of words in the text.
def contours(img, iterations=3, dilate=True):
    if dilate is False:
        im = img
    else:
        # Dilate image for better segmentation
        im = dilate_img(img, iterations)

    # Check if image is already gray.
    try:
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    except:
        imgray = im

    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    return contours

# Dilate image for better segmentation in contours detection.
def dilate_img(img, iterations):
    # Convert image to gray.
    # Check if image is already in gray scale.
    try:
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        imgray = img

    # Clean all noises.
    denoised = cv2.fastNlMeansDenoising(imgray, dst=None, h=10)

    # Negative the image.
    imagem = cv2.bitwise_not(denoised)

    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(imagem, kernel, iterations=iterations)

    # Negative it again to original color
    final = cv2.bitwise_not(dilate)

    return final

# Crop the words the contours function found.
def crop_words(img, conts, output_dir):
    counter = 0

    for i in conts:
        x, y, w, h = cv2.boundingRect(i)
        cropped = img[y:y + h, x:x + w]
        width, height = cropped.shape[:2]

        # Avoid cropping very small contours e.g dots, commas.
        if width * height > 300:
            cv2.imwrite(str(output_dir) + str(counter) + ".png", cropped)

        counter = counter + 1

    return

# Draw rectangles around the contours function found.
def draw_rects(img, contour, path_save):
    (x, y, w, h) = cv2.boundingRect(contour)

    # Clean all small contours out.
    if (h*w) < 25:
        return

    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
    cv2.imwrite(path_save, img)
