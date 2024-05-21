import argparse
from pathlib import Path

from label_image import load_graph, load_labels, get_prediction

import cv2
import numpy as np


MODEL_FILE = 'retrained_graph.pb'
LABEL_FILE = 'retrained_labels.txt'
graph = None
labels = None


def predict_class(image_file):
    pred = get_prediction(graph, labels, image_file)
    return '%s: %0.1f%%' % (pred[0][0], 100 * pred[0][1])


def show_image(win_name, image):
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_name, 500, 500)
    cv2.imshow(win_name, image)
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key in [27, 81, 83, 255]:
            return key


def add_text_to_image(image, text):
    image = cv2.resize(image, (0, 0), fx=500 / image.shape[0], fy=500 / image.shape[0])
    bottom_padding = 255 * np.ones(shape=(50, image.shape[1], 3),
                                   dtype=np.uint8)
    bottom_padding = np.pad(bottom_padding, ((3,3), (3,3), (0, 0)),
                            'constant', constant_values=((0,0), (0,0), (0,0)))
    image = np.pad(image, ((3,0), (3,3), (0, 0)),
                   'constant', constant_values=((0,0), (0,0), (0,0)))
    font = cv2.FONT_HERSHEY_DUPLEX
    font_size = np.min([0.5*bottom_padding.shape[1] / cv2.getTextSize(text, font, 1, 1)[0][0],
                        0.5*bottom_padding.shape[0] / cv2.getTextSize(text, font, 1, 1)[0][1]])
    new_size = cv2.getTextSize(text, font, font_size, 1)
    cv2.putText(bottom_padding,
                text,
                org=(
                    np.round(0.5*(bottom_padding.shape[1] - new_size[0][0])).astype(np.int32),
                    np.round(bottom_padding.shape[0] - 0.5*(bottom_padding.shape[0] - new_size[0][1])).astype(np.int32)
                ),
                fontFace=font,
                fontScale=font_size,
                color=(0, 0, 0),
                thickness=1,
                lineType=cv2.LINE_AA)
    return np.vstack((image, bottom_padding))


def _main_(args):
    path = args.img_folder

    global graph, labels
    graph = load_graph(MODEL_FILE)
    labels = load_labels(LABEL_FILE)
    from datetime import datetime

    img_list = [str(file) for file in sorted(Path(path).iterdir())]
    idx = 0
    while True:
        if idx < 0:
            idx = len(img_list) - 1
        elif idx == len(img_list):
            idx = 0
        print('Prediction started: %s' % datetime.now().strftime('%H:%M:%S'))
        # TODO prediction in separate thread
        text = predict_class(img_list[idx])
        print('Prediction finished: %s' % datetime.now().strftime('%H:%M:%S'))

        image = add_text_to_image(cv2.imread(img_list[idx]), text)
        response = show_image(img_list[idx], image)
        if response == 27 or response == 255:
            cv2.destroyAllWindows()
            return
        elif response == 83:
            idx += 1
        elif response == 81:
            idx -= 1
        cv2.destroyAllWindows()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Predict veggie class')
    argparser.add_argument(
        '-img_folder',
        dest='img_folder',
        required=True,
        help='path to folder with images')
    args = argparser.parse_args()
    _main_(args)
