import os
import pandas as pd
import tensorflow as tf
import sys
from PIL import Image
import io


sys.path.append("models/research")
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

def get_catgeory_map(file="training_demo/annotations/list_category_cloth.txt"):
    _categories = []
    with open(file, 'r') as fp:
        _categories = fp.readlines()[1:]
    _categories = [cat.split()[0] for cat in _categories]

    categories = dict()
    for i, ctg in enumerate(_categories):
        categories[ctg] = i + 1
    return categories

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def create_tf_example(group, path):
    with tf.gfile.GFile(path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(ctg[row['class']])

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    mode = "test"

    csv_input = "training_demo/data/{}.csv".format(mode)
    output_path = "training_demo/data/{}.record".format(mode)
    img_dir = "training_demo/images/{}".format(mode)

    writer = tf.python_io.TFRecordWriter(output_path)
    # path = os.path.join(img_path)
    examples = pd.read_csv(csv_input)
    grouped = split(examples, 'filename')
    idx = 1
    for group in grouped:
        print(idx)
        idx += 1
        img_path = os.path.join(img_dir, group.filename)
        tf_example = create_tf_example(group, img_path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    # output_path = os.path.join(os.getcwd(), output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    ctg = get_catgeory_map()
    tf.app.run()
    # print(ctg)