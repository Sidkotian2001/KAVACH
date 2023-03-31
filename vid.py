import cv2
import os
# Open the video file
cap = cv2.VideoCapture('RoadAccidents/RoadAccidents002_x264.mp4')

# Get the video frame width and height
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, 30, (frame_width, frame_height))

# Loop through the video frames
while cap.isOpened():
    ret, frame = cap.read()

    # If the frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Add a rectangle to the frame
    cv2.rectangle(frame, (50, 50), (frame_width - 50, frame_height - 50), (0, 255, 0), 3)

    # Write the modified frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Frame', frame)
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the video capture and writer objects, and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()

#now run "ffmpeg -i output_video.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart output_video2.mp4" on terminal
os.system("ffmpeg -i output_video.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart output_video2.mp4")

