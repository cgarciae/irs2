from keras import backend as K
import inception_v4
import numpy as np
import cv2
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

		self.one_hot_labels = tf.one_hot(inputs.labels, self._n_classes)

		self.logits = tf.layers.dense(self._n_classes)
		self.prediction = tf.nn.softmax(self.logits)

		return dict(
			embedding = inputs.embedding,
			prediction = self.prediction
		)

	def get_loss(self, inputs):
		return tf.nn.softmax_cross_entropy_with_logits(
			logits=self.logits,
			labels=self.one_hot_labels
		)

	def get_score_tensor(self, inputs):
		return ti.metrics.softmax_score(self.predictions, self.one_hot_labels)



def get_keras_objects():
	# Create model and load pre-trained weights
	model = inception_v4.create_model(weights='imagenet', include_top=True)

	sess = K.get_session()
	graph = sess.graph

	image = graph.get_tensor_by_name("input_1:0")
	embedding = graph.get_tensor_by_name("flatten_1/Reshape:0")

	return sess, graph, image, embedding


def get_templates(n_classes, seed = 64):

	sess, graph, image, embedding = get_keras_objects()

	inputs_t = GeneralSupervisedInputs(
		name = "inputs",
		sess = sess,
		graph = graph,
		image = lambda: image,
		embedding = lambda: embedding,
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
