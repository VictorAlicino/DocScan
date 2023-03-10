import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from dataclasses import dataclass

@dataclass
class dst_size:
    factor: int = 5

    width: int = 210 * factor
    height: int = 297 * factor

filepath: str = ""

# Define the callback function for mouse events
def mouse_callback(event, x, y, flags, params):
    global corners, index, img_copy, scaling_factor

    # If the left mouse button is clicked, add a point to the list of corners
    if event == cv2.EVENT_LBUTTONDOWN:
        corners[index] = [int(x / scaling_factor), int(y / scaling_factor)]
        index += 1

        # Draw a circle at the clicked point
        cv2.circle(img_copy, (x, y), 10, (0, 255, 255), 2)

        # If all four corners have been selected, apply the homography function
        if index == 4:
            h, _ = cv2.findHomography(corners, dst)
            corrected_img = cv2.warpPerspective(img, h, (dst_size.width, dst_size.height))

            # Display the original and corrected images
            cv2.imshow("Corrected", corrected_img)

            # Ask for save the image
            response = messagebox.askyesno(title="Save Image", message="Do you want to save the image?")
            
            if response == 1:
                file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
                print(file_path)
                cv2.imwrite(file_path, corrected_img)
                cv2.destroyAllWindows()
                exit()
            else:
                cv2.destroyAllWindows()
                exit()
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # Display the image with the selected points
    cv2.imshow("Image", img_copy)

if __name__ == "__main__":
    # Create a root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Ask the user to select a file
    file_path = filedialog.askopenfilename()

    # Read the input image
    img = cv2.imread(file_path)

    # Define the destination points for the homography function
    dst = np.array(
        [[0, 0], 
        [dst_size.width - 1, 0], 
        [dst_size.width - 1, dst_size.height - 1], 
        [0, dst_size.height - 1]], 
        dtype=np.float32
        )

    # Create a named window for the image and set the mouse callback function
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)
    
    # Initialize the list of corners and the index of the next corner to be selected
    corners = np.zeros(
        (4, 2), 
        dtype=np.int32
        )
    index = 0
    
    # Get the size of the image
    h, w = img.shape[:2]
    
    # Calculate the scaling factor between the image and the display window
    scaling_factor = min(1.0, 800.0 / max(h, w))
    
    # Resize the image and create a copy to draw the selected points
    img_resized = cv2.resize(img, (0, 0), fx=scaling_factor, fy=scaling_factor)
    img_copy = img_resized.copy()
    
    # Display the original image
    cv2.imshow("Image", img_copy)
    
    # Wait for a key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()
