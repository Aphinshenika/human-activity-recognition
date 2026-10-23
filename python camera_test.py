
import cv2
import time

print("Starting camera test...")

for index in [0, 1, 2]:
    print(f"\nTrying camera index {index}...")

    camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(index, cv2.CAP_MSMF)

    if not camera.isOpened():
        print("Camera could not open.")
        camera.release()
        continue

    time.sleep(2)

    for attempt in range(10):
        success, frame = camera.read()

        if success and frame is not None:
            print(f"SUCCESS! Camera index {index} is working.")
            cv2.imshow("Camera Test - Press Q to quit", frame)

            while True:
                success, frame = camera.read()

                if success and frame is not None:
                    cv2.imshow("Camera Test - Press Q to quit", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            camera.release()
            cv2.destroyAllWindows()
            raise SystemExit

        time.sleep(0.5)

    print("Camera opened, but no frames received.")
    camera.release()

cv2.destroyAllWindows()
print("\nNo working camera found.")
