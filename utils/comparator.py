from PIL import Image
import imagehash
import requests
from io import BytesIO
from functools import lru_cache
import logging


@lru_cache
def load_image_from_url(url):
    """
    Load an image from a URL using Pillow.

    Parameters:
    - url (str): URL of the image.

    Returns:
    - Image.Image: Image object.
    """
    logging.debug(f'Loading image from web.Url:{url}')
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

@lru_cache
def are_images_same(image_path1, image_path2, hash_size=8, tolerance=5):
    """
    Check if two images are the same using perceptual hashing.

    Parameters:
    - image_path1 (str): Path to the first image file.
    - image_path2 (str): Path to the second image file.
    - hash_size (int): Size of the hash. Larger values provide more details but require more computation.
    - tolerance (int): Hamming distance tolerance. Images with a Hamming distance less than or equal to
                     this value are considered similar.

    Returns:
    - bool: True if the images are considered the same, False otherwise.
    """
    try:
        # Load images
        img1 = load_image_from_url(image_path1)
        img2 = load_image_from_url(image_path2)
        # Resize images for consistent hashing
        img1 = img1.resize((hash_size, hash_size))
        img2 = img2.resize((hash_size, hash_size))
        logging.debug('Resizing two images')

        # Compute perceptual hashes
        hash1 = imagehash.average_hash(img1)
        hash2 = imagehash.average_hash(img2)
        logging.debug('Computing average hash')

        # Compare hashes using Hamming distance
        hamming_distance = hash1 - hash2

        # Check if the images are similar based on the tolerance
        return hamming_distance <= tolerance

    except Exception as e:
        logging.exception(f"Error: {e}")
        return False

# import cv2

# def are_images_same(image_path1, image_path2):
#     """
#     Check if two images are the same using OpenCV.

#     Parameters:
#     - image_path1 (str): Path to the first image file.
#     - image_path2 (str): Path to the second image file.

#     Returns:
#     - bool: True if the images are considered the same, False otherwise.
#     """
#     try:
#         # Read images
#         img1 = cv2.imread(image_path1)
#         img2 = cv2.imread(image_path2)

#         # Check if the images have the same shape
#         if img1.shape != img2.shape:
#             return False

#         # Compute the absolute difference between the images
#         diff = cv2.absdiff(img1, img2)

#         # Convert the difference to grayscale
#         gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

#         # Set a threshold for the difference
#         _, threshold_diff = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

#         # Count the number of non-zero pixels in the thresholded difference
#         non_zero_pixels = cv2.countNonZero(threshold_diff)

#         # If the number of non-zero pixels is below a threshold, consider the images the same
#         return non_zero_pixels < 1000  # Adjust the threshold as needed

#     except Exception as e:
#         print(f"Error: {e}")
#         return False



def compare_dicts(previous_data:dict, new_data:dict):
    '''use to get difference between to dictionary'''
    # Find keys that are common to both dictionaries
    common_keys = set(previous_data.keys()) & set(new_data.keys())

    # Find keys that are unique to each dictionary
    unique_keys_dict1 = set(previous_data.keys()) - set(new_data.keys())
    unique_keys_dict2 = set(new_data.keys()) - set(previous_data.keys())

    # Find values that are different for common keys
    diff_val = [(key, previous_data[key], new_data[key]) for key in common_keys if previous_data[key] != new_data[key]]

    # Create a dictionary of the differences
    differences = {
        'common_keys': common_keys,
        'unique_keys_dict1': unique_keys_dict1,
        'unique_keys_dict2': unique_keys_dict2,
        'different_values': diff_val
    }

    return differences

def get_diff_val(previous_data:dict, new_data:dict) -> list[tuple]:
    '''same as compare_dicts '''
    
    # Find keys that are common to both dictionaries
    common_keys = set(previous_data.keys()) & set(new_data.keys())
    logging.debug(f'Getting different values from two dict')
    # Find values that are different for common keys
    diff_vals = []
    for key in common_keys:
        if previous_data[key] != new_data[key]:
            diff_vals.append((key, previous_data[key], new_data[key]))

    logging.debug(f'Different values :{diff_vals}')
    return diff_vals


def is_diff(dict1, dict2) -> bool:
    '''check if two dictionary are same or not'''

    logging.debug(f'Compering different values from two dict')
    # Check for changes in keys
    if set(dict1.keys()) != set(dict2.keys()):
        return True

    # Check for changes in values
    for key in dict1:
        if key.lower() == 'dp':
            if not are_images_same(dict1[key],dict2[key]):
                return True

        elif dict1[key] != dict2[key]:
            return True

    # No changes detected
    return False
