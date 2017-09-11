from keras import backend as K
import inception_v4
import numpy as np
import os
import tensorflow as tf
from tfinterface.supervised import GeneralSupervisedInputs, GeneralSupervisedModel
import tfinterface as ti

class Model(GeneralSupervisedModel):
	"""docstring for Model."""

	def __init__(self, n_classes, *args, **kwargs):

		self._n_classes = n_classes

		super(Model, self).__init__(*args, **kwargs)

	def get_predictions(self, inputs):

		print(inputs.embedding)


		self.one_hot_labels = tf.one_hot(inputs.labels, self._n_classes)

		net = inputs.embedding; print(net)

		net = ti.layers.dense_batch_norm(net, 256, activation = tf.nn.elu, batch_norm = dict(training = inputs.training)); print(net)

		net = self.logits = tf.layers.dense(net, self._n_classes); print(net)
		net = self.image_class = tf.nn.softmax(net); print(net)

		return dict(
			embedding = inputs.embedding,
			prediction = self.image_class
		)

	def get_loss(self, inputs):
		loss = tf.nn.softmax_cross_entropy_with_logits(
			logits=self.logits,
			labels=self.one_hot_labels
		)

		return tf.reduce_mean(loss)

	def get_score_tensor(self, inputs):
		return ti.metrics.softmax_score(self.image_class, self.one_hot_labels)


	def get_train_variables(self, **kwargs):
		return super(Model, self).get_train_variables(scope = self.name, **kwargs)



def get_keras_objects():
	# Create model and load pre-trained weights
	scope = "inception_v4"
	with tf.name_scope(scope):
		model = inception_v4.create_model(weights='imagenet', include_top=True)

		sess = K.get_session()
		graph = sess.graph

		image = graph.get_tensor_by_name(scope + "/input_1:0")
		dropout = graph.get_tensor_by_name(scope + "/dropout_1/cond/Merge:0")
		keras_training = graph.get_tensor_by_name(scope + "/batch_normalization_1/keras_learning_phase:0")
		embedding = tf.contrib.layers.flatten(dropout)


	# tf.summary.FileWriter(logdir = "logs", graph = graph).flush()

	return sess, graph, image, embedding, keras_training


def get_templates(n_classes, seed = 64):

	sess, graph, image, embedding, keras_training = get_keras_objects()

	inputs_t = GeneralSupervisedInputs(
		name = "inputs",
		sess = sess,
		graph = graph,
		image = lambda: image,
		embedding = lambda: embedding,
		keras_training = keras_training,
		labels = dict(shape = (None,), dtype = tf.uint8),
	)

	model_t = Model(
		n_classes = n_classes,
		name = "inception_v4_tunning",
		sess = sess,
		graph = graph,
		seed = seed,
		model_path = "models/inception_v4_tunning",
	)

	return inputs_t, model_t
