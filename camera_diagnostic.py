

import cv2

backends = [
    ("Default", cv2.CAP_ANY),
    ("DirectShow", cv2.CAP_DSHOW),
    ("Media Foundation", cv2.CAP_MSMF),
]

for index in range(5):
    for name, backend in backends:
        camera = cv2.VideoCapture(index, backend)

        opened = camera.isOpened()
        received_frame = False

        if opened:
            received_frame, frame = camera.read()

        print(
            f"Index {index} | {name} | "
            f"Opened: {opened} | Frame: {received_frame}"
        )

        camera.release()

cv2.destroyAllWindows()
