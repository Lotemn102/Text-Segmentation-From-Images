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

# Removes horizontal lines (e.g from notebook scans).
def remove_horizontal_lines(img):
     # Check if image is already in gray scale.
    try:
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        imgray = img

    # Inverse the image.
    img_inverse = cv2.bitwise_not(imgray)

    # Change image to binary color.
    bw = cv2.adaptiveThreshold(img_inverse, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 15, -2)

    # Copy binary image.
    horizontal = bw.copy()

    # Find structuring element size. 30 is ok for most images i've tested in
    # various size from ~50*100 (a single word) to ~1500*2300 (full page).
    horiz_size = int(bw.shape[1] / (bw.shape[1]/30))

    # Create a line structuring element.
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                     (horiz_size, 1))

    # Preform erode function with structuring element in order to find the
    # image lines.
    horizontal = cv2.erode(src=horizontal, kernel=horizontal_structure,
                           anchor=(-1, -1))

    # Preform dilate function in order to connect some gaps in found lines.
    horizontal = cv2.dilate(src=horizontal, kernel=horizontal_structure,
                            anchor=(-1, -1))

    # Inverse the image, so that lines are black for masking.
    horizontal_inv = cv2.bitwise_not(horizontal)

    # Mask the inverted img with the inverted mask lines.
    masked_img = cv2.bitwise_and(img_inverse, img_inverse, mask=horizontal_inv)

    # Reverse the image back to normal.
    masked_img_inv = cv2.bitwise_not(masked_img)

    # Blur image and threshold it for better result.
    imgBlur = cv2.medianBlur(masked_img_inv, 3, 0)
    _, final = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_OTSU)

    return final















