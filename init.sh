#git clone https://github.com/tensorflow/models.git

wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz -C training_demo/
rm ssd_mobilenet_v2_coco_2018_03_29.tar.gz

wget http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz
tar -xvf ssd_inception_v2_coco_2018_01_28.tar.gz -C training_demo/
rm ssd_inception_v2_coco_2018_01_28.tar.gz

#wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_oid_v4_2018_12_12.tar.gz
#tar -xvf ssd_mobilenet_v2_oid_v4_2018_12_12.tar.gz -C training_demo/
#rm ssd_mobilenet_v2_oid_v4_2018_12_12.tar.gz