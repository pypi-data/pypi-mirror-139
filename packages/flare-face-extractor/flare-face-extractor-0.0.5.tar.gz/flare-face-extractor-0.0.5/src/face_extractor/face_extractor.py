import numpy as np
import cv2 as cv
from typing import List
import base64


class Face:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __getitem__(self, index):
        return (self.x, self.y, self.width, self.height)[index]


def __load_image(encoded_image: bytes) -> np.ndarray:
    """
    Loads an image from a file.

    :param encoded_image: A base64 encoded image.
    :return: A numpy array of RGB values.
    """
    image = base64.b64decode(encoded_image)
    image_np = np.frombuffer(image, dtype=np.uint8)

    return cv.imdecode(image_np, flags=1)


def __draw_rectangles(image: np.ndarray, faces: List[Face]) -> None:
    if image is None:
        return

    for (x, y, w, h) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def __detect(image: np.ndarray) -> List[Face]:
    """
    Identifies the location of faces in a given numpy array of RGB values.

    :param image: A numpy array of RGB values.
    :return: A list of faces. Each face consists of its x and y coordinates as well as its width and height.
    """
    if image is None:
        return []

    cascade_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(gray_image, 1.3, 10)

    return [Face(x, y, w, h) for (x, y, w, h) in faces]


def locate_faces(encoded_image: bytes) -> List[Face]:
    """
    Calculates the location of all the faces in a given image.

    :param encoded_image: A base64 encoded image.
    :return: A list of faces. Each face consists of its x and y coordinates as well as its width and height.
    """
    image = __load_image(encoded_image)
    return __detect(image)


def outline_faces(encoded_image: bytes) -> None:
    """
    Opens a window displaying the image provided and outlines the faces present in the photo.
    Should be used purely for interactive purposes.

    :param encoded_image: A base64 encoded image.
    :return: None
    """
    image = __load_image(encoded_image)
    faces = __detect(image)

    __draw_rectangles(image, faces)

    cv.imshow("image", image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def count(encoded_image: bytes) -> int:
    """
    Returns the number of faces present in the given image.

    :param encoded_image: A base64 encoded image.
    :return: An integer representing the number of `Faces` present.
    """
    image = __load_image(encoded_image)
    return len(__detect(image))


# For local testing:
# image_path = '../../data/test.jpeg'
#
# with open(image_path, "rb") as image:
#     f = image.read()
#     image = bytearray(f)
#     encoded_image = base64.b64encode(image)
#     print(count(encoded_image))
#     print(locate_faces(encoded_image))
#     print(outline_faces(encoded_image))
