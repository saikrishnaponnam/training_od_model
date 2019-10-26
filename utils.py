import pandas as pd
from PIL import Image
import shutil
import sys


class Utils:
    def __init__(self):
        self.ctg_file = "training_demo/annotations/list_category_cloth.txt"
        self.img_ctg_file = "training_demo/annotations/list_category_img.txt"
        self.eval_part_file = "training_demo/annotations/list_eval_partition.txt"
        self.bbox_file = "training_demo/annotations/list_bbox.txt"

    def get_catgeory_map(self, ctg_file=None):
        ctg_file = ctg_file if ctg_file else self.ctg_file
        try:
            with open(ctg_file, 'r') as fp:
                data = [line.split()[0] for line in fp.readlines()[2:]]
        except FileNotFoundError:
            print("couldn't find {}".format(ctg_file))
            sys.exit(1)
        categories = dict()
        for i in range(len(data)):
            categories[i + 1] = data[i]
        return categories

    def get_ctg_img_map(self, img_ctg_file=None):
        img_ctg_file = img_ctg_file if img_ctg_file else self.img_ctg_file
        try:
            with open(img_ctg_file, 'r') as fp:
                data = fp.readlines()[2:]
        except FileNotFoundError:
            print("couldn't find {}".format(img_ctg_file))
            sys.exit(1)
        ctg_img = dict()
        for i in range(len(data)):
            img, cat = data[i].split()
            cat = int(cat)
            if cat in ctg_img:
                ctg_img[cat].append(img)
            else:
                ctg_img[cat] = [img]
        return ctg_img

    def get_img_ctg_map(self, img_ctg_file=None):
        img_ctg_file = img_ctg_file if img_ctg_file else self.img_ctg_file
        try:
            with open(img_ctg_file, 'r') as fp:
                data = fp.readlines()[2:]
        except FileNotFoundError:
            print("couldn't find {}".format(img_ctg_file))
            sys.exit(1)
        img_ctg = dict()
        for i in range(len(data)):
            img, cat = data[i].split()
            img_ctg[img] = cat
        return img_ctg

    def get_img_status_map(self, eval_part_file=None):
        eval_part_file = eval_part_file if eval_part_file else self.eval_part_file
        try:
            with open(eval_part_file, 'r') as fp:
                data = fp.readlines()[2:]
        except FileNotFoundError:
            print("couldn't find {}".format(eval_part_file))
            sys.exit(1)
        img_status = dict()
        for line in data:
            img, eval_staus = line.split()
            img_status[img] = eval_staus
        return img_status

    def get_train_test_list(self, eval_part_file=None):
        img_evalstatus_dict = self.get_img_status_map(eval_part_file)
        split = {'train': [], 'test': [], 'val': []}
        for img, eval_status in img_evalstatus_dict.items():
            split[eval_status].append(img)
        return split

    def get_img_bboxs(self, bbox_file=None):
        bbox_file = bbox_file if bbox_file else self.bbox_file
        try:
            with open(bbox_file, 'r') as fp:
                data = [line.split() for line in fp.readlines()[2:]]
        except FileNotFoundError:
            print("couldn't find {}".format(bbox_file))
            sys.exit(1)
        img_bbox = dict()
        for d in data:
            img_bbox[d[0]] = d[1:]
        return img_bbox

    def get_annot_csv(self, bbox_file=None):
        img_bbox = self.get_img_bboxs(bbox_file)
        # print(img_bbox)
        ctg_cls_map = self.get_catgeory_map()
        # print(ctg_cls_map)
        ctg_img_map = self.get_ctg_img_map()
        # print(ctg_img_map)
        img_status_map = self.get_img_status_map()
        # print(img_status_map)
        # return

        data = []
        for key, imgs in sorted(ctg_img_map.items()):
            ctg = ctg_cls_map[key]
            # print(ctg)
            idx = 1
            for img in imgs:
                print("{} --> {}. {} ".format(ctg, idx, img))
                im = Image.open("training_demo/" + img)
                width, height = im.size
                img_data = [ctg + "_{:05d}.jpg".format(idx), width, height, ctg] + img_bbox[img] + [img,
                                                                                                    img_status_map[img]]
                data.append(img_data)
                idx += 1
        # print(data[:10])
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'original_filename',
                       'eval_status']
        xml_df = pd.DataFrame(data, columns=column_name)
        return xml_df


if __name__ == '__main__':
    # df = get_annot_csv()
    # print(df)
    # df.to_csv('training_demo/annotations/annotation.csv', index=None)

    # df = pd.read_csv("training_demo/annotations/annotation.csv")
    # print(len(df))
    # for idx, row in df.iterrows():
    #     # print(row['original_filename'], row['eval_status'], row['filename'])
    #     print(idx)
    #     shutil.copy("training_demo/" + row['original_filename'],
    #                 "training_demo/images/" + row['eval_status'] + "/" + row['filename'])

    # df = pd.read_csv("training_demo/annotation.csv")
    # train_df = pd.DataFrame()
    # test_df = pd.DataFrame()
    # val_df = pd.DataFrame()
    # for idx, row in df.iterrows():
    #     print(idx)
    #     if row['eval_status'] == 'train':
    #         train_df = train_df.append(row)
    #     elif row['eval_status'] == 'test':
    #         test_df = test_df.append(row)
    #     else:
    #         val_df = val_df.append(row)
    #
    # print(len(train_df))
    # print(len(test_df))
    # print(len(val_df))
    #
    # train_df.to_csv('training_demo/data/{}.csv'.format("train"), index=None)
    # test_df.to_csv('training_demo/data/{}.csv'.format("test"), index=None)
    # val_df.to_csv('training_demo/data/{}.csv'.format("val"), index=None)

    # print(CreateTFRecord().get_train_test_list())
    # Utils().get_annot_csv()

    utils = Utils()
    data = utils.get_ctg_img_map()
    ctg_map = utils.get_catgeory_map()
    for ctg, imgs in data.items():
        print(ctg_map[ctg], len(imgs))
