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
import utils



@click.command()
@click.option('--device', '-d', default="/gpu:0", help='Device, default = gpu:0')
@click.option('--epochs', '-e', default=8000, help='Number of epochs, default = 4000')
@click.option('--batch-size', '-b', default=64, help='Batch size, default = 64')
@click.option('--loss', default = "mse", help='mse or huber')
@click.option('--restore', is_flag = True, help='restore')
def main(device, epochs, batch_size, loss, restore):

    # seed: resultados repetibles
    seed = 32
    np.random.seed(seed=seed)
    random.seed(seed)

    # dataget
    dataset = data(
        "visual-words"
    ).get(process=False)

    # utils.process_steering(dataset.training_set, params.alpha, params.straight_tol, params.steering_filter)
    # print(dataset.training_set.pure_dataframe().columns)

    # obtener todas las imagenes (lento)
    def data_generator_fn():
        return dataset.training_set.random_batch_arrays_generator(batch_size)

    graph = tf.Graph()
    sess = tf.Session(graph=graph)

    # inputs
    input_t, model_t = get_templates(dataset.n_classes, seed = seed)

    # model

    with tf.device(device):
        inputs = input_t()
        model = model_t(inputs)

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
