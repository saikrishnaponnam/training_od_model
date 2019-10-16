import os
import shutil

partition_file = "training_demo/Eval/list_eval_partition.txt"

fp = open(partition_file, 'r')
lines = int(fp.readline())
image_path, evaluation_status = fp.readline().split()

for i in range(lines):
    image_path, evaluation_status = fp.readline().split()

    src = os.path.join("training_demo/", image_path)
    img = image_path.split("/")

    if os.path.exists(src):
        des_dir = os.path.join("training_demo/images", evaluation_status, img[-2])
        if not  os.path.exists(des_dir):
            os.makedirs(des_dir)
        print(str(i) + ". moving " + image_path)
        shutil.move(src, os.path.join(des_dir, img[-1]))
    else:
        print(image_path + " deoesn't exists")
