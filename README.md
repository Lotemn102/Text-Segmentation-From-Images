# TIS - Text-based Images Segmentation
A script for cropping words or characters from text-based images.

Can be used for both printed texts and handwritten texts. 

For example:

![1](https://user-images.githubusercontent.com/35609587/62475033-d65a2280-b7ac-11e9-8ddc-7977c59b79e3.png)

## Quick Start
```python
# Creates a new image object.
img = tis('example.png')

# Crops words from text and saves them to 'cropped_words' directory.
img.crop_text(output_dir='cropped_words', iterations=5, remove_lines=True)

# Draws rectangles around all words in the text, and saves the result to
# 'result_rec.png'.
img.draw_rectangles(output_path='result_rec.png', iterations=5, remove_lines=True)

```

## How This Works
This script uses cv2 package. 

The algorithm for finding the words in a text-based image is demonstrated in the following chart:

![2](https://user-images.githubusercontent.com/35609587/62476582-f8a16f80-b7af-11e9-8dd6-fa4c630fd207.png)


## Available Functions
**draw_rectangles**(output_path=None, iterations=5, dilate=True)

This function draws rectangles around the words in the text.
With this function, you can see how ‘iterations’ variables affect the scripts’ segmentation performance. Can be convenient for long texts.

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
    
For example:
```python
# Creates a new image object.
img = tis(‘example.png')

# Draws rectangles around all words in the text, and saves the result to
# 'result_rec.png'.
img.draw_rectangles(output_path='result_rec.png', iterations=5)
```
Result:

![3](https://user-images.githubusercontent.com/35609587/62475602-048c3200-b7ae-11e9-8f76-11eae1178e03.png)

Higher number of iteration is used for text segmentation, while lower number is used for characters segmentation.

For example:
```python
# Creates a new image object.
img = tis('example.png')

# Draws rectangles around all words in the text, and saves the result to
# 'result_rec.png'.
img.draw_rectangles(output_path='result_rec.png', iterations=1)
```
Result:

![4](https://user-images.githubusercontent.com/35609587/62475730-4cab5480-b7ae-11e9-8d35-b6ecae056a4c.png)


**crop_text**(output_dir=None, iterations=5, dilate=True):

This function crops the words from the text and saves them in separate png images.


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

For example:
```python
# Creates a new image object.
img = tis('example.png')

# Crops words from text and saves them to 'cropped_words' directory.
img.crop_text(output_dir='cropped_words', iterations=5)
```

Result:

![5](https://user-images.githubusercontent.com/35609587/62476196-3356d800-b7af-11e9-8152-cca5975f78a1.png)


## Requirements
-	NumPy
-	cv2
