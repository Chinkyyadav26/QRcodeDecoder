import cv2
import numpy as np
from pyzbar.pyzbar import decode

class QRCodeScanner:
    def __init__(self):
        self.cap = None

    def scan_from_webcam(self):
        """Scan QR codes using the webcam."""
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Unable to access the webcam.")
            return

        print("Press 'q' to exit.")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            self._process_frame(frame)

            cv2.imshow("QR Code Scanner - Webcam", frame)

            # Break the loop if the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def scan_from_image(self, image_path):
        """Scan QR codes from an image file."""
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Error: Unable to load image at {image_path}")
            return

        self._process_frame(frame)

        cv2.imshow("QR Code Scanner - Image", frame)
        print("Press any key to close the image.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def _process_frame(self, frame):
        """Process a frame to detect and decode QR codes."""
        qr_codes = decode(frame)

        for qr in qr_codes:
            points = qr.polygon

            if len(points) == 4:
                cv2.polylines(frame, [np.array(points, dtype=np.int32)], True, (0, 255, 0), 2)

            qr_data = qr.data.decode('utf-8')
            print(f"QR Code Detected: {qr_data}")

            cv2.putText(frame, qr_data, (qr.rect.left, qr.rect.top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

if __name__ == "__main__":
    scanner = QRCodeScanner()

    print("Choose an option:")
    print("1. Scan from Webcam")
    print("2. Scan from Image")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        scanner.scan_from_webcam()
    elif choice == '2':
        image_path = input("Enter the path to the image file: ")
        scanner.scan_from_image(image_path)
    else:
        print("Invalid choice. Exiting.")
