import sys
import urllib.request
import hashlib
import os


veggies_classes = ['tomato', 'cucumber', 'carrot', 'eggplant', 'potato',
                   'beat', 'pumpkin', 'broccoli', 'cabbage', 'pepper',
                   'onion', 'zucchini', 'celery', 'cauliflower', 'garlic']


def download_link(url, file_path):
    try:
        img = urllib.request.urlopen(url).read()
    except Exception as e:
        print('Unable to download link: %s.\n%s' % (url, e))
        return
    md5 = hashlib.md5()
    md5.update(img)
    file_name = os.path.join(file_path,
                             '%s.%s' % (md5.hexdigest(), url.split('.')[-1]))
    try:
        with open(file_name, 'wb') as f_out:
            f_out.write(img)
    except Exception as e:
        print('Unable to save image: %s.\n%s' % (url, e))
        return


if __name__ == '__main__':
    print('To be implemented')
    url = 'https://farm3.staticflickr.com/2810/8757757198_067b156ca3.jpg'
    download_link(url, '')
