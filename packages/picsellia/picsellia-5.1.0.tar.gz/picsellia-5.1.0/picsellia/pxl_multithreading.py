import logging
from multiprocessing import Value
import requests
import os
import sys
from picsellia.decorators import retry
from picsellia.exceptions import ResourceNotFoundError
from picsellia.utils import print_line_return, print_next_bar

logger = logging.getLogger('picsellia')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Multiprocessed init
def pool_init(length, counter):
    global download_counter
    global total_length
    download_counter = counter
    total_length = length

def download_list_external_picture(png_dir : str, infos : list):
    global download_counter
    global total_length
    for info in infos:
        pic_name = os.path.join(png_dir, os.path.split(info['external_picture_url'])[-1])
        if not os.path.isfile(pic_name):
            download_external_picture(info=info, pic_name=pic_name)

        with download_counter.get_lock():
            download_counter.value += 1
            print_next_bar(download_counter.value, total_length)

def download_external_picture(info, pic_name):
    global download_counter
    global total_length
    try:
        response = requests.get(info["signed_url"], stream=True)
        if response.status_code == "404":
            raise ResourceNotFoundError('Picture does not exist on our server.')
        with open(pic_name, 'wb') as handler:
            for data in response.iter_content(chunk_size=1024):
                handler.write(data)
    except Exception:
        logger.error(f"Image {pic_name} can't be downloaded")


def init_pool_annotations(p, nb, req, ds_id, p_size):
    global page_done
    global nb_pages
    global connexion
    global annotation_list
    global dataset_id
    global page_size
    page_done = p
    nb_pages = nb - 1
    connexion = req
    dataset_id = ds_id
    annotation_list = []
    page_size = p_size


def dl_annotations(page_list):
    global page_done
    global nb_pages
    global connexion
    global annotation_list
    global dataset_id
    global page_size

    annotation_list = []
    for page in page_list:
        params = {
            'limit': page_size,
            'offset': page_size*page,
            'snapshot': False
        }
        r = connexion.get(
            'dataset/{}/annotations'.format(dataset_id), params=params)
        annotation_list += r.json()["annotations"]
        with page_done.get_lock():
            page_done.value += 1
        print_next_bar(page_done.value, nb_pages)
    return annotation_list
