#! /usr/bin/python

from dataget import data # <== dataget
import tensorflow as tf
import cytoolz as cz
from phi.api import *
from model import get_model_t, get_inputs_t
import numpy as np
import random
from name import network_name, model_path
from tfinterface.supervised import GeneralSupervisedInputs
import click
import utils
from parameters import Parameters



@click.command()
@click.option('--device', '-d', default="/gpu:0", help='Device, default = gpu:0')
@click.option('--epochs', '-e', default=8000, help='Number of epochs, default = 4000')
@click.option('--batch-size', '-b', default=64, help='Batch size, default = 64')
@click.option('--loss', default = "mse", help='mse or huber')
@click.option('--restore', is_flag = True, help='restore')
def main(device, epochs, batch_size, loss, restore):
    params = Parameters()

    # seed: resultados repetibles
    seed = 32
    np.random.seed(seed=seed)
    random.seed(seed)

    # dataget
    dataset = data(
        "udacity-selfdriving-simulator",
        camera_steering_correction = params.camera_steering_correction,
        angle_bins = params.nbins,
        angle_straight_tol = params.straight_tol,
        normal_angle_tol = params.normal_angle_tol,
    ).get(process=False)

    # utils.process_steering(dataset.training_set, params.alpha, params.straight_tol, params.steering_filter)
    # print(dataset.training_set.pure_dataframe().columns)

    # obtener todas las imagenes (lento)
    def data_generator_fn():
        data_generator = dataset.training_set.random_batch_arrays_generator(batch_size, uniform = True, extra_features=["angle_class"])
        return utils.process_generator(data_generator, keys = ["image", "angle_class", "steering"])

    graph = tf.Graph()
    sess = tf.Session(graph=graph)

    # inputs
    inputs = get_inputs_t(sess, graph)


    # create model template
    template = get_model_t(sess, graph, seed)

    # model

    with tf.device(device):
        inputs = inputs()
        model = template(inputs)

    # initialize variables
    print("Initializing Model: restore = {}".format(restore))
    model.initialize(restore = restore)

    # start queue
    # inputs.start_queue(data_generator_fn)

    # fit
    print("training")
    model.fit(
        data_generator = data_generator_fn(),
        epochs = epochs,
        # log_summaries = True,
        log_interval = 10,
        print_test_info = True,
        on_train = [dict(
            when = lambda step, **kwargs: step % 1000 == 0,
            do = lambda **kwargs: model.save()
        )]
    )

    # save
    print("saving model")
    model.save()


if __name__ == '__main__':
    main()
