# -*- encoding:utf-8 -*-
# Copyright (c) Alibaba, Inc. and its affiliates.

import logging
import os

import tensorflow as tf
from tensorflow.python.lib.io import file_io

from easy_rec.python.main import predict

if tf.__version__ >= '2.0':
  tf = tf.compat.v1

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d : %(message)s',
    level=logging.INFO)

tf.app.flags.DEFINE_string('pipeline_config_path', None,
                           'Path to pipeline config '
                           'file.')
tf.app.flags.DEFINE_string(
    'checkpoint_path', None, 'checkpoint to be evaled '
    ' if not specified, use the latest checkpoint in '
    'train_config.model_dir')
tf.app.flags.DEFINE_string(
    'input_path', None, 'predict data path, if specified will '
    'override pipeline_config.eval_input_path')
tf.app.flags.DEFINE_string('output_path', None, 'path to save predict result')
tf.app.flags.DEFINE_string('model_dir', None, help='will update the model_dir')
FLAGS = tf.app.flags.FLAGS


def main(argv):
  assert FLAGS.model_dir or FLAGS.pipeline_config_path, 'At least one of model_dir and pipeline_config_path exists.'
  if FLAGS.model_dir:
    pipeline_config_path = os.path.join(FLAGS.model_dir, 'pipeline.config')
    if file_io.file_exists(pipeline_config_path):
      logging.info('update pipeline_config_path to %s' % pipeline_config_path)
    else:
      pipeline_config_path = FLAGS.pipeline_config_path
  else:
    pipeline_config_path = FLAGS.pipeline_config_path

  pred_result = predict(pipeline_config_path, FLAGS.checkpoint_path,
                        FLAGS.input_path)
  if FLAGS.output_path is not None:
    logging.info('will save predict result to %s' % FLAGS.output_path)
    with tf.gfile.GFile(FLAGS.output_path, 'wb') as fout:
      for k in pred_result:
        fout.write(str(k).replace("u'", '"').replace("'", '"') + '\n')


if __name__ == '__main__':
  tf.app.run()