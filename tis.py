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
        - path_save (string): A path to save the image to. If None is given as
            a parameter, images will be saved in a directory called 
            "text_segmentation" inside the original image's parent directory.
        - iterations (int): Number of dilation iterations that will be done on
        the image. Default value is set to 5.
        - remove_lines (bool): Whether to remove lines from the text
            (i.e for notebook pages) or not. Default value is set to False.
        - dilate (boolean): Whether to dilate the text in the image or not.
            Default is set to 'True'. Highly recommended to dilate the image for
            better segmentation. 
            
    Returns:
        None.
        Saves images of all words from the text in the saving path.
    '''
    def crop_text(self, output_dir=None, remove_lines=False, iterations=5):

        if remove_lines:
            no_lines_img = remove_horizontal_lines(self.img)
        else:
            no_lines_img = self.img

        sharp_img = sharpen_text(no_lines_img)
        conts = contours(sharp_img, iterations)

        if not output_dir:
            parent_dir = os.path.dirname(self.img_path)
            output_dir = os.path.join(
                parent_dir, 'text_segmentation')

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_dir = output_dir + '\\'

        elif not os.path.exists(output_dir):
            os.makedirs(output_dir)
            output_dir = output_dir + '\\'

        elif os.path.exists(output_dir):
            output_dir = output_dir + '\\'

        crop_words(sharp_img, conts, output_dir)

    '''
    Function draw_rectangles:

    Parameters:
        - output_dir (string): A path to save the image to. If None is given as
            a parameter, image will be saved in the original image parent
            directory.
        - iterations (int): Number of dilation iterations that will be done on
        the image. Default value is set to 5.
        - remove_lines (bool): Whether to remove lines from the text
            (i.e for notebook pages) or not. Default value is set to False.
        - dilate (boolean): Whether to dilate the text in the image or not.
            Default is set to 'True'. Highly recommended to dilate the image for
            better segmentation. 

    Returns:
        The edited image (numpy array).
        Saves the image in the saving path.
    '''
    def draw_rectangles(self, output_path=None, remove_lines=False, iterations=5, dilate=True):

        if remove_lines:
            no_lines_img = remove_horizontal_lines(self.img)
        else:
            no_lines_img = self.img

        sharp_img = sharpen_text(no_lines_img)
        conts = contours(sharp_img, iterations, dilate)

        if not output_path:
            parent_path = os.path.dirname(self.img_path)
            output_path = parent_path + 'draw_rectangles_result.png'

        for i in conts:
            draw_rects(sharp_img, i, str(output_path))

    '''
    Function remove_lines:
    
    Parameters:
        output_dir (string): A path to save the image to. If None is given as
        a parameter, image will be saved in the original image parent directory.

    Returns:
        The edited image (numpy array).
        Saves the image in the saving path.
    '''
    def remove_lines(self, output_path=None):

        no_lines_img = remove_horizontal_lines(self.img)

        if not output_path:
            parent_path = os.path.dirname(self.img_path)
            output_path = parent_path + 'remove_lines_result.png'

        cv2.imwrite(str(output_path), no_lines_img)

        return no_lines_img




