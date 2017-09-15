#! /usr/bin/python

from dataget import data # <== dataget
import tensorflow as tf
import cytoolz as cz
from phi.api import *
from model import get_templates
import numpy as np
import random
from tfinterface.supervised import GeneralSupervisedInputs
import click

@click.command()
@click.option('--device', '-d', default="/gpu:0", help='Device, default = gpu:0')
def main(device):

    n_classes = data("visual-words").n_classes

    graph = tf.Graph()
    sess = tf.Session(graph=graph)

    # inputs
    inputs_t, model_t = get_templates(n_classes)

    # model
    with tf.device(device):
        inputs = inputs_t()
        model = model_t(inputs)

    with graph.as_default():
        print("")
        print("##########################################################")
        print("Number of Weights = {:,}".format(model.count_weights()))
        print("##########################################################")

if __name__ == '__main__':
    main()
