import cv2
from PIL import Image
from util import get_limits

yellow = [0, 255, 255]  # yellow in BGR colorspace

def main():
    cap = cv2.VideoCapture(0)  # Use camera index 0

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        try:
            hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        except cv2.error as e:
            print(f"Error converting frame to HSV: {e}")
            break

        lowerLimit, upperLimit = get_limits(color=yellow)

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        mask_ = Image.fromarray(mask)

        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
