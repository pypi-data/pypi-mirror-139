# Copyright 2022 XXIV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import http.client
import json


class DogAPIException(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_request(endpoint):
    conn = http.client.HTTPSConnection('dog.ceo')
    conn.request('GET', f'/api/{endpoint}')
    data = conn.getresponse().read().decode('UTF-8')
    conn.close()
    return data


def random_image():
    """
    DISPLAY SINGLE RANDOM IMAGE FROM ALL DOGS COLLECTION

    :return: a random dog image
    :raises DogAPIException:
    """
    try:
        response = get_request("breeds/image/random")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def multiple_random_images(images_number: int):
    """
    DISPLAY MULTIPLE RANDOM IMAGES FROM ALL DOGS COLLECTION

    :param images_number: number of images
    :return: multiple random dog image, NOTE ~ Max number returned is 50
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breeds/image/random/{images_number}")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def random_image_by_breed(breed: str):
    """
    RANDOM IMAGE FROM A BREED COLLECTION

    :param breed: breed name
    :return: a random dog image from a breed, e.g. hound
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breed/{breed.strip()}/images/random")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def multiple_random_images_by_breed(breed: str, images_number: int):
    """
    MULTIPLE IMAGES FROM A BREED COLLECTION

    :param breed: breed name
    :param images_number: number of images
    :return: multiple random dog image from a breed, e.g. hound
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breed/{breed.strip()}/images/random/{images_number}")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def images_by_breed(breed: str):
    """
    ALL IMAGES FROM A BREED COLLECTION

    :param breed: breed name
    :return: an array of all the images from a breed, e.g. hound
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breed/{breed.strip()}/images")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def random_image_by_sub_breed(breed: str, sub_breed: str):
    """
    SINGLE RANDOM IMAGE FROM A SUB BREED COLLECTION

    :param breed: breed name
    :param sub_breed: sub_breed name
    :return: a random dog image from a sub-breed, e.g. Afghan Hound
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breed/{breed.strip()}/{sub_breed.strip()}/images/random")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def multiple_random_images_by_sub_breed(breed: str, sub_breed: str, images_number: int):
    """
    MULTIPLE IMAGES FROM A SUB-BREED COLLECTION

    :param breed: breed name
    :param sub_breed: sub_breed name
    :param images_number: number of images
    :return: multiple random dog images from a sub-breed, e.g. Afghan Hound
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breed/{breed.strip()}/{sub_breed.strip()}/images/random/{images_number}")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def images_by_sub_breed(breed: str, sub_breed: str):
    """
    LIST ALL SUB-BREED IMAGES

    :param breed: breed name
    :param sub_breed: sub_breed name
    :return: an array of all the images from the sub-breed
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breed/{breed.strip()}/{sub_breed.strip()}/images")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def breeds_list():
    """
    LIST ALL BREEDS

    :return: object of all the breeds as keys and sub-breeds as values if it has
    :raises DogAPIException:
    """
    try:
        response = get_request("breeds/list/all")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)


def sub_breeds_list(breed: str):
    """
    LIST ALL SUB-BREEDS

    :param breed: breed name
    :return: an array of all the sub-breeds from a breed if it has sub-breeds
    :raises DogAPIException:
    """
    try:
        response = get_request(f"breed/{breed.strip()}/list")
        data = json.loads(response)
        if data['status'] != "success":
            raise Exception(data['message'])
        if len(data["message"]) == 0:
            raise Exception("the breed does not have sub-breeds")
        return data['message']
    except Exception as ex:
        raise DogAPIException(ex)