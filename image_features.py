import tensorflow as tf
from tensornets.references import rcnns

inputs = tf.placeholder(tf.float32, [None, 620, 426, 3])
model = rcnns.faster_rcnn_vgg16_voc(inputs, classes=4000)

# fout = open('data/features.tsv', 'w')
# download roi-pooling from https://github.com/deepsense-ai/roi-pooling


