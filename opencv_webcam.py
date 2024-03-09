import cv2

def main():
    # Open the default camera (usually the webcam)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly ret is True
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame
        cv2.imshow('Webcam', frame)

        # Check for 'q' key pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
