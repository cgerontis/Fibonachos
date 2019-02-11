On line 14 and 25, you need to change the file path to where you saved the training set

Things that can be manipulated:
Line 32: The part that says "(11,11)". The higher the numbers the more it blurs the image.
They must be odd numbers. This is helpful because the more the image is blurred, the less likely
it will pick individual squares for the checkered pattern. The downside, however, if it's too blurred
it will not pick up anything useful

Lines 33 and 34: These are the two thresholds. The "60" and "100" determine the level. I'm not sure the
range for these (probably 0 to 255?). 

Lines 57 and 78: The higher the number in "> 1" means you accept contours who are further away from the 
the saved contour. The lower the number, the closer the contour is to the checkered pattern