from __future__ import print_function, absolute_import, unicode_literals, division

import os, sys, urllib, zipfile, shutil
from dataget.dataset import ImageDataSet
from dataget.utils import get_file
from dataget.api import register_dataset
import tarfile
import numpy as np


#-------path data------#
TRAINING_SET_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"


@register_dataset
class VisualWords(ImageDataSet):

    def __init__(self, *args, **kwargs):
        super(VisualWords, self).__init__(*args, **kwargs)

        # self.path
        # self.training_set
        # self.training_set.path
        # self.training_set.make_dirs()
        # self.test_set
        # self.test_set.path
        # self.test_set.make_dirs()

    @property
    def _raw_extension(self):
        return "jpeg"

    @property
    def help(self):
        return "" # information for the help command

    def reqs(self, **kwargs):
        return super(VisualWords, self).reqs() + "" # e.g. "numpy pandas pillow"


    def _download(self, **kwargs):
        pass
        # get_file(TRAINING_SET_URL, self.path, "complete-set.tar.gz")



    def _extract(self, train_size = 0.8, **kwargs):
        data_path = os.path.join(self.path, "collected-data")

        i = -1
        n_classes = len(os.listdir(data_path))
        for n_class, folder in enumerate(os.listdir(data_path)):

            folder_path = os.path.join(data_path, folder)

            for img in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img)
                i += 1

                set_dir = "training-set" if i < int(train_size*10) else "test-set"

                set_folder_path = os.path.join(self.path, set_dir, str(n_class))

                if not os.path.exists(set_folder_path):
                    os.makedirs(set_folder_path)

                img_dest_path = os.path.join(set_folder_path, img)

                #print("SOURCE", img_path)
                #print("DEST", img_dest_path)


                shutil.copyfile(img_path, img_dest_path)


                i = i % 10
        #shutil.rmtree(data_path)
