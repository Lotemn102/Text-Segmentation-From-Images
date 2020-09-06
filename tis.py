from process_functions import *
import os

'''
Class tis:

Parameters:
    - img_path (string): A path to text-based image to work on.
        
Returns:
    A new text_segmentation object.
'''
class tis:

    def __init__(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path)

    '''
    Function crop_text:
    
    Parameters:
        - output_dir (string): A path to save the image to. If None is given as
            a parameter, images will be saved in a directory called 
            "text_segmentation" inside the original image's parent directory.
        - iterations (int): Number of dilation iterations that will be done on
        the image. Default value is set to 5.
        - dilate (bool): Whether to dilate the text in the image or not.
            Default is set to 'True'. It is recommended to dilate the image for
            better segmentation. 

            
    Returns:
        None.
        Saves images of all words from the text in the output path.
    '''
    def crop_text(self, output_dir, iterations=5, dilate=True):
        sharp_img = self.__sharpen_text(self.img)
        conts = self.__contours(sharp_img, iterations, dilate)

        if not output_dir:
            print("Please insert output directory.")
            return

        self.__crop_words(sharp_img, conts, output_dir)

    '''
    Function draw_rectangles:

    Parameters:
        - output_path (string): A path to save the image to. If None is given as
            a parameter, image will be saved in the original image parent
            directory.
        - iterations (int): Number of dilation iterations that will be done on
        the image. Default value is set to 5.
        - dilate (bool): Whether to dilate the text in the image or not.
            Default is set to 'True'. It is recommended to dilate the image for
            better segmentation. 

    Returns:
        None.
        Saves the image in the output path.
    '''
    def draw_rectangles(self, output_path=None, iterations=5, dilate=True):
        sharp_img = self.__sharpen_text(self.img)
        conts = self.__contours(sharp_img, iterations, dilate)

        if not output_path:
            parent_path = os.path.dirname(self.img_path)
            output_path = parent_path + 'draw_rectangles_result.png'

        for i in conts:
            self.__draw_rects(sharp_img, i, str(output_path))
            
    # Clean image background and sharpen text.
    def __sharpen_text(img):
        thresh = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
        return thresh

    # Find contours of words in the text.
    def __contours(img, iterations=3):
        # Dilate image for better segmentation
        im = self.__dilate_img(img, iterations)
        contours, hierarchy = cv2.findContours(im, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        return contours

    # Dilate image for better segmentation in contours detection.
    def __dilate_img(img, iterations):
        # Clean all noises.
        denoised = cv2.fastNlMeansDenoising(img, dst=None, h=10)

        # Negative the image.
        imagem = cv2.bitwise_not(denoised)
        kernel = np.ones((3, 3), np.uint8)
        dilate = cv2.dilate(imagem, kernel, iterations=iterations)

        # Negative it again to original color
        final = cv2.bitwise_not(dilate)

        return final

    # Crop the words the contours function found.
    def __crop_words(img, conts, output_dir):
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
    def __draw_rects(img, contour, path_save):
        (x, y, w, h) = cv2.boundingRect(contour)

        # Clean all small contours out.
        if (h*w) < 25:
            return

        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.imwrite(path_save, img)

