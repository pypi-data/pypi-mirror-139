import io
from typing import Union
from PIL import Image as img
import base64
from PIL.Image import Image
import imagehash
from imagehash import ImageHash, hex_to_hash


def __load_image(encoded_image: bytes) -> Union[Image, None]:
    """
    Opens and identifies the given image file.

    :param image_path: A string specifying where the image in located
    :return: PIL.Image on success.
    """
    image = base64.b64decode(encoded_image)
    return img.open(io.BytesIO(image))


def hash_image(encoded_image: bytes) -> Union[ImageHash, None]:
    """
    Average Hash computation of the given image.

    :param encoded_image: A base64 encoded image.
    :return: An imagehash `ImageHash` object on success. None otherwise.
    """
    image = __load_image(encoded_image)

    if not image:
        return None

    return imagehash.average_hash(image)


def are_similar(reference_hash: str, other_hash: str) -> bool:
    """
    Returns True if two images are relatively similar.

    :param reference_hash: An hex string returned from str(ImageHash)
    :param other_hash: An hex string returned from str(ImageHash)
    :return: True if similar. False otherwise.
    """

    return abs(hex_to_hash(reference_hash) - hex_to_hash(other_hash)) <= 15


def similarity(reference_hash: str, other_hash: str) -> int:
    """
    Returns how similar the hashes of two images are. Lower is more similar and 0 is equal.

    :param reference_hash: An hex string returned from str(ImageHash)
    :param other_hash: An hex string returned from str(ImageHash)
    :return: The bit difference between two hashes
    """

    return abs(hex_to_hash(reference_hash) - hex_to_hash(other_hash))


# For testing:
# pairs = [
#     ['test.jpeg', 'test_cropped_in.jpeg'],
#     ['IMG_5643.jpg', 'IMG_5644.jpg'],
# ]
#
# for pair in pairs:
#     hashes = []
#
#     for path in pair:
#         with open(f"../../images/{path}", "rb") as image:
#             f = image.read()
#             image = bytearray(f)
#             encoded_image = base64.b64encode(image)
#             calculated_hash = hash_image(encoded_image)
#             print(f"{path}: {calculated_hash}")
#             hashes.append(str(calculated_hash))
#
#     print(are_similar(hashes[0], hashes[1]), similarity(hashes[0], hashes[1]))
