import cv2
import numpy as np

# Read the input image
img = cv2.imread('input_image.jpg')

# Define the dimensions of the A4 paper
width, height = 210, 297  # mm

# Define the destination points for the homography function
dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

# Define the callback function for mouse events
def mouse_callback(event, x, y, flags, params):
    global corners, index, img_copy

    # Make a copy of the original image to draw the selected points
    img_copy = img.copy()

    # If the left mouse button is clicked, add a point to the list of corners
    if event == cv2.EVENT_LBUTTONDOWN:
        corners[index] = [x, y]
        index += 1

        # Draw a circle at the clicked point
        cv2.circle(img_copy, (x, y), 5, (0, 0, 255), -1)

        # If all four corners have been selected, apply the homography function
        if index == 4:
            h, _ = cv2.findHomography(corners, dst)
            corrected_img = cv2.warpPerspective(img, h, (width, height))

            # Display the original and corrected images
            cv2.imshow("Original", img)
            cv2.imshow("Corrected", corrected_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # Display the image with the selected points
    cv2.imshow("Image", img_copy)

# Create a named window for the image and set the mouse callback function
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

# Initialize the list of corners and the index of the next corner to be selected
corners = np.zeros((4, 2), dtype=np.int32)
index = 0

# Calculate the size of the input image and adjust the window size accordingly
img_height, img_width, _ = img.shape
window_height = min(img_height, 800)
window_width = min(img_width, 1200)

# Display the original image
cv2.imshow("Image", img)
cv2.resizeWindow("Image", window_width, window_height)

# Wait for a key press
cv2.waitKey(0)
cv2.destroyAllWindows()
