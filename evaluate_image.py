from keras import backend as K
import inception_v4
import numpy as np
import cv2
import os
import tensorflow as tf
from tfinterface.supervised import GeneralSupervisedInputs, GeneralSupervisedModel

class Model(GeneralSupervisedModel):
	"""docstring for Model."""

	def get_predictions(self, inputs):

		net = inputs.embedding

		self.preditions



def get_keras_objects():
	# Create model and load pre-trained weights
	model = inception_v4.create_model(weights='imagenet', include_top=True)

	sess = K.get_session()
	graph = sess.graph

	image = graph.get_tensor_by_name("input_1:0")
	embedding = graph.get_tensor_by_name("flatten_1/Reshape:0")

	return sess, graph, image, embedding
