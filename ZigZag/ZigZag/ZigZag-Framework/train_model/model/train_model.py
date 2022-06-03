# -*- coding: utf-8 -*-
#
# datetime:2022/3/6 20:45
from tensorflow_core.python.keras.callbacks import EarlyStopping

from preprocess.process_data import *
from preprocess.load_data import *
from tools.oth_tools import *
from model.bgru_generator_model import *
import time
from tensorflow.keras.models import Model

from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger

from tools.utils import get_all_files

"""
description：
"""


class TranModel(object):
    """
            model train 
            model_kind:  TODO:deal different model
        """

    def __init__(self, model_kind, dataset_path, model_path, result_path, batch_size, max_len, vector_dim,
                 drop_out,
                 serial_number, threshold, epoch_times, learning_rate, file_len, step_len):
        self.model_kind = model_kind
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.batch_size = batch_size
        self.max_len = max_len
        self.vector_dim = vector_dim
        self.drop_out = drop_out
        self.serial_number = serial_number
        self.threshold = threshold  # Threshold
        self.result_path = result_path
        self.epoch_times = epoch_times
        self.learning_rate = learning_rate
        self.file_len = file_len
        self.step_len = step_len
        self.generatorModel = GeneratorModel(self.max_len, self.vector_dim, self.drop_out, self.threshold,
                                             self.model_path, self.learning_rate)

    def train_3_1(self, model_name):
        """
            3.1:train  origin
        """
        print("build model 3.1...")
        # Model Callback
        checkpoint_model_name = model_name + \
                                "-{epoch:02d}-{val_loss:.5f}-{val_classifier1_binary_accuracy:.5f}-val.h5"
        checkpoint_filepath = os.path.join(
            self.model_path, checkpoint_model_name)
        checkpoint_val_loss = ModelCheckpoint(checkpoint_filepath, monitor='val_loss', verbose=1,
                                              save_best_only=True,
                                              save_weights_only=False, mode='min')
        checkpoint_val_acc = ModelCheckpoint(checkpoint_filepath, monitor='val_classifier1_binary_accuracy',
                                             verbose=1,
                                             save_best_only=True,
                                             save_weights_only=False, mode='max')
        callbacks_list = [checkpoint_val_loss, checkpoint_val_acc,
                          CSVLogger(os.path.join(self.result_path, model_name + 'log.csv'), append=True, separator=',')]
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        EarlyStopping(monitor='val_classifier1_binary_accuracy', min_delta=0.01, patience=6, verbose=0, mode='max',
                      baseline=None, restore_best_weights=False)
        model_name = os.path.join(self.model_path, model_name)
        model_3_1 = self.generatorModel.generator_model_3_1()
        # 1.  origin
        print("Loading train_3_1 data...")
        all_file_full_path_list = []
        all_file_name_list = []
        dataset_path_list, *_ = get_all_files(os.path.join(self.dataset_path, 'train', 'origin'),
                                              all_file_full_path_list,
                                              all_file_name_list)
        all_data_len = self.file_len * len(dataset_path_list)
        # dataset_path_list, all_data_len = get_file_path_list(
        #     os.path.join(self.dataset_path, 'train'), 'origin', self.file_len)
        train_generator = data_generator_from_list(
            dataset_path_list, self.batch_size, self.step_len)

        val_x, val_y = load_data_once(
            os.path.join(self.dataset_path, 'validation'))
        # 公式3
        print("train_3_1 begin ...")
        steps_epoch = int(all_data_len / self.batch_size)
        history = model_3_1.fit_generator(train_generator, epochs=self.epoch_times[0], steps_per_epoch=steps_epoch,
                                          validation_data=(
                                              val_x, [val_y, val_y]),
                                          callbacks=callbacks_list)
        print(history.history.keys())
        print(history.params)

        print("train_3_1 end ...")
        model_3_1.summary()
        mkdir(self.model_path)
        model_3_1.save(model_name)
        print(checkpoint_filepath)
        print("model 3.1 saved...")
        print("step 3.1 has been trained ...")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return model_3_1

    def train_3_2_1(self, model_last, model_name):
        """
            3.2:train  tigress
        """
        print("build model 3.21...")
        # Model Callback
        checkpoint_model_name = model_name + \
                                "-{epoch:02d}-{val_loss:.5f}-{val_classifier1_binary_accuracy:.5f}-val.h5"

        checkpoint_filepath = os.path.join(
            self.model_path, checkpoint_model_name)
        checkpoint_val_loss = ModelCheckpoint(checkpoint_filepath, monitor='val_loss', verbose=1,
                                              save_best_only=True,
                                              save_weights_only=False, mode='min')
        checkpoint_val_acc = ModelCheckpoint(checkpoint_filepath, monitor='val_classifier1_binary_accuracy',
                                             verbose=1,
                                             save_best_only=True,
                                             save_weights_only=False, mode='max')

        callbacks_list = [checkpoint_val_loss, checkpoint_val_acc,
                          CSVLogger(os.path.join(self.result_path, model_name + 'log.csv'), append=True, separator=',')]
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        model_name = os.path.join(self.model_path, model_name)
        model_3_21 = self.generatorModel.generator_model_3_2_1(model_last)
        #
        print("Loading train_3_21 data...")
        all_file_full_path_list = []
        all_file_name_list = []
        dataset_path_list, *_ = get_all_files(os.path.join(self.dataset_path, 'train', 'origin'),
                                              all_file_full_path_list,
                                              all_file_name_list)
        all_file_full_path_list = []
        all_file_name_list = []
        dataset_path_list1, *_ = get_all_files(os.path.join(self.dataset_path, 'train', 'tigress'),
                                               all_file_full_path_list,
                                               all_file_name_list)

        dataset_path_list.extend(dataset_path_list1)
        all_data_len = self.file_len * len(dataset_path_list)
        # dataset_path_list, all_data_len = get_file_path_list(
        #     os.path.join(self.dataset_path, 'train'), 'tigress', self.file_len)
        # dataset_path_list2, all_data_len2 = get_file_path_list(
        #     os.path.join(self.dataset_path, 'train'), 'origin', self.file_len)
        # all_data_len = all_data_len + all_data_len2

        train_generator = data_generator_from_list(
            dataset_path_list, self.batch_size, self.step_len)

        # train_generator = data_generator(
        #     dataset_path_list, self.batch_size)
        val_x, val_y = load_data_once(
            os.path.join(self.dataset_path, 'validation'))
        print("train_3_21 begin ...")
        steps_epoch = int(all_data_len / self.batch_size)
        history = model_3_21.fit_generator(train_generator, epochs=self.epoch_times[1], steps_per_epoch=steps_epoch,
                                           validation_data=(
                                               val_x, [val_y, val_y]),
                                           callbacks=callbacks_list)
        print(history.history.keys())
        print(history.params)
        model_3_21.summary()
        mkdir(self.model_path)
        model_3_21.save(model_name)
        print(checkpoint_filepath)
        print("model 3.21 saved...")
        return model_3_21

    def train_3_2_2(self, model_last, model_last2, model_name, hard_name):
        """
            train hard
            3.2
        """
        model_3_2_2 = self.generatorModel.generator_model_3_2_2(
            model_last, model_last2)
        # 1.
        print("Loading train_3_22 hard data...", time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()))
        model_name = os.path.join(self.model_path, model_name)
        data_list_all = []
        dataset_path_list, all_data_len = get_file_path_list(
            os.path.join(self.dataset_path, 'train'), 'origin', self.file_len)
        data_list_all.append(dataset_path_list)

        dataset_path_list2, all_data_len2 = get_file_path_list(
            os.path.join(self.dataset_path, 'train'), hard_name, self.file_len)
        data_list_all.append(dataset_path_list2)
        train_generator = data_generator_two(data_list_all, self.batch_size)

        if all_data_len < all_data_len2:
            all_data_len = all_data_len2

        print("train_3_22 begin ...")
        steps_epoch = int(all_data_len / self.batch_size)

        # 公式3
        print("train_3_22 begin ...")
        history = model_3_2_2.fit_generator(
            train_generator, steps_per_epoch=steps_epoch, epochs=self.epoch_times[2])
        #  model
        print(history.history.keys())
        print(history.params)
        print("train_3_22 end ...")
        model322 = Model(inputs=model_3_2_2.get_layer('inputs').output,
                         outputs=[model_3_2_2.get_layer('classifier1').output,
                                  model_3_2_2.get_layer('classifier2').output])
        model322.summary()
        mkdir(self.model_path)
        model322.save(model_name)

        print("model 3.22 saved...")
        print("step 3.22 has been trained ...")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return model322

    def train_3_3(self, model_last, model_name):
        """
            train  tigress
            3.3
        """
        model_3_3 = self.generatorModel.generator_model_3_3(model_last)

        print("Loading train_3_3 tigress data...")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        model_name = os.path.join(self.model_path, model_name)
        dataset_path_list, all_data_len = get_file_path_list(
            os.path.join(self.dataset_path, 'train'), 'tigress', self.file_len)
        train_generator = data_generator(dataset_path_list, self.batch_size)

        # 公式3
        print(" train_3_3 begin ...")
        steps_epoch = int(all_data_len / self.batch_size)
        history = model_3_3.fit_generator(
            train_generator, steps_per_epoch=steps_epoch, epochs=self.epoch_times[3])

        print(history.history.keys())
        print(history.params)
        # save model
        model33 = Model(inputs=model_3_3.get_layer('inputs').output,
                        outputs=[model_3_3.get_layer('classifier1').output,
                                 model_3_3.get_layer('classifier2').output])
        print("train_3_3 end ...")
        model33.summary()
        mkdir(self.model_path)
        model33.save(model_name)
        print("model 3.3 saved...")
        print("step 3.3 has been trained ...")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return model33
