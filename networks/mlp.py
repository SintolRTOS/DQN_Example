import tensorflow as tf

from .layers import *
from .network import Network

#多层网络感知机
#用于处理DQN的深度神经网络
class MLPSmall(Network):
  def __init__(self, sess,
               data_format,
               observation_dims,
               history_length,
               output_size,
               trainable=True,
               batch_size=None,
               weights_initializer=initializers.xavier_initializer(),
               biases_initializer=tf.zeros_initializer,
               hidden_activation_fn=tf.nn.relu,
               output_activation_fn=None,
               hidden_sizes=[50, 50, 50],
               value_hidden_sizes=[25],
               advantage_hidden_sizes=[25],
               network_output_type='dueling',
               name='MLPSmall'):
    super(MLPSmall, self).__init__(sess, name)

    with tf.variable_scope(name):
      if data_format == 'NHWC':
        layer = self.inputs = tf.placeholder(
          'float32', [batch_size] + observation_dims + [history_length], 'inputs')
      elif data_format == 'NCHW':
        layer = self.inputs = tf.placeholder(
          'float32', [batch_size, history_length] + observation_dims, 'inputs')
      else:
        raise ValueError("unknown data_format : %s" % data_format)

      if len(layer.get_shape().as_list()) == 3:
        assert layer.get_shape().as_list()[1] == 1
        layer = tf.reshape(layer, [-1] + layer.get_shape().as_list()[2:])

      for idx, hidden_size in enumerate(hidden_sizes):
        w_name, b_name = 'w_%d' % idx, 'b_%d' % idx

        layer, self.var[w_name], self.var[b_name] = \
            linear(layer, hidden_size, weights_initializer, 
              biases_initializer, hidden_activation_fn, trainable, name='lin_%d' % idx)

      self.build_output_ops(layer, network_output_type, 
          value_hidden_sizes, advantage_hidden_sizes, output_size, 
          weights_initializer, biases_initializer, hidden_activation_fn,
          output_activation_fn, trainable)
