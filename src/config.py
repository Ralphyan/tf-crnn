#!/usr/bin/env python
__author__ = 'solivr'

import os
import json


class Alphabet:
    BLANK_SYMBOL = '$'
    LettersLowercase = 'abcdefghijklmnopqrstuvwxyz'  # 26
    LettersCapitals = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # 26
    Digits = '0123456789'  # 10
    Symbols = "'.,:-="  # 6
    LETTERS_DIGITS = Digits + LettersCapitals + LettersLowercase + BLANK_SYMBOL
    LETTERS_DIGITS_LOWERCASE = Digits + LettersLowercase + BLANK_SYMBOL
    LETTERS_ONLY = LettersCapitals + LettersLowercase + BLANK_SYMBOL
    LETTERS_ONLY_LOWERCASE = LettersLowercase + BLANK_SYMBOL
    LETTERS_EXTENDED = LettersCapitals + LettersLowercase + Symbols + BLANK_SYMBOL
    LETTERS_EXTENDED_LOWERCASE = LettersLowercase + Symbols + BLANK_SYMBOL


class Params:
    def __init__(self, **kwargs):
        self._train_batch_size = kwargs.get('train_batch_size', 100)
        self._eval_batch_size = kwargs.get('eval_batch_size', 200)
        self._learning_rate = kwargs.get('learning_rate', 1e-4)
        self._decay_rate = kwargs.get('decay_rate', 0.96)
        self._decay_steps = kwargs.get('decay_steps', 1000)
        self._optimizer = kwargs.get('optimizer', 'adam')
        self._n_epochs = kwargs.get('n_epochs', 50)
        self._evaluate_every_epoch = kwargs.get('evaluate_every_epoch', 5)
        self._save_interval = kwargs.get('save_interval', 1e3)
        self._input_shape = kwargs.get('input_shape', (32, 100))
        self._digits_only = kwargs.get('digits_only', False)
        self._alphabet_decoding = kwargs.get('alphabet_decoding', 'same')
        self._csv_delimiter = kwargs.get('csv_delimiter', ';')
        self._gpu = kwargs.get('gpu', '')
        self._alphabet = kwargs.get('alphabet')
        # self._nclasses = kwargs.get('n_classes')
        self._csv_files_train = kwargs.get('csv_files_train')
        self._csv_files_eval = kwargs.get('csv_files_eval')
        self._output_model_dir = kwargs.get('output_model_dir')
        self._keep_prob_dropout = kwargs.get('keep_prob')

        assert self._optimizer in ['adam', 'rms', 'ada'], 'Unknown optimizer {}'.format(self._optimizer)

        assert self._alphabet in ['letters_digits', 'letters_only', 'letters_extended'], \
            'Unknown alphabet {}'.format(self._alphabet)
        assert self._alphabet_decoding in ['same', 'lowercase'], \
            'Unknown alphabet decoding {}'.format(self._alphabet_decoding)
        if self._alphabet == 'letters_digits':
            self._alphabet = Alphabet.LETTERS_DIGITS
            if self._alphabet_decoding == 'lowercase':
                self._alphabet_decoding = Alphabet.LETTERS_DIGITS_LOWERCASE
                self._alphabet_codes = list(range(len(Alphabet.Digits))) + \
                                       list(range(len(Alphabet.Digits),
                                                  len(Alphabet.Digits) + len(Alphabet.LettersCapitals))) + \
                                       list(range(len(Alphabet.Digits),
                                                  len(Alphabet.Digits) + len(Alphabet.LettersLowercase) + 1))
                self._blank_label_code = self._alphabet_codes[-1]
        elif self._alphabet == 'letters_only':
            self._alphabet = Alphabet.LETTERS_ONLY
            if self._alphabet_decoding == 'lowercase':
                self._alphabet_decoding = Alphabet.LETTERS_ONLY_LOWERCASE
                self._alphabet_codes = list(range(len(Alphabet.LettersCapitals))) + \
                                       list(range(len(Alphabet.LettersLowercase) + 1))
                self._blank_label_code = self._alphabet_codes[-1]
        elif self._alphabet == 'letters_extended':
            self._alphabet = Alphabet.LETTERS_EXTENDED
            if self._alphabet_decoding == 'lowercase':
                self._alphabet_decoding = Alphabet.LETTERS_EXTENDED_LOWERCASE
                self._alphabet_codes = list(range(len(Alphabet.LettersCapitals))) + \
                                       list(range(len(Alphabet.LettersLowercase))) + \
                                       list(range(2*len(Alphabet.LettersCapitals),
                                                  2*len(Alphabet.LettersCapitals) + len(Alphabet.Symbols) + 1))
                self._blank_label_code = self._alphabet_codes[-1]

        if self._alphabet_decoding == 'same':
            self._alphabet_decoding = self._alphabet
            self._alphabet_codes = list(range(len(self._alphabet)))
            self._blank_label_code = len(self._alphabet)

        self._nclasses = self._alphabet_codes[-1] + 1
        self._blank_label_symbol = Alphabet.BLANK_SYMBOL

    def export_experiment_params(self):
        if not os.path.isdir(self.output_model_dir):
            os.mkdir(self.output_model_dir)
        with open(os.path.join(self.output_model_dir, 'model_params.json'), 'w') as f:
            json.dump(vars(self), f)

    @property
    def n_classes(self):
        return self._nclasses

    @property
    def train_batch_size(self):
        return self._train_batch_size

    @property
    def eval_batch_size(self):
        return self._eval_batch_size

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def decay_rate(self):
        return self._decay_rate

    @property
    def decay_steps(self):
        return self._decay_steps

    @property
    def optimizer(self):
        return self._optimizer

    @property
    def n_epochs(self):
        return self._n_epochs

    @property
    def save_interval(self):
        return self._save_interval

    # @property
    # def model_dir(self):
    #     return self._model_dir

    @property
    def input_shape(self):
        return self._input_shape

    @property
    def csv_files_train(self):
        return self._csv_files_train

    @property
    def csv_files_eval(self):
        return self._csv_files_eval

    @property
    def output_model_dir(self):
        return self._output_model_dir

    @property
    def gpu(self):
        return self._gpu

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def alphabet_decoding(self):
        return self._alphabet_decoding

    @property
    def alphabet_codes(self):
        return self._alphabet_codes

    @property
    def digits_only(self):
        return self._digits_only

    @property
    def keep_prob_dropout(self):
        return self._keep_prob_dropout

    @keep_prob_dropout.setter
    def keep_prob_dropout(self, value):
        self._keep_prob_dropout = value

    @property
    def csv_delimiter(self):
        return self._csv_delimiter

    @property
    def evaluate_every_epoch(self):
        return self._evaluate_every_epoch

    @property
    def blank_label_code(self):
        return self._blank_label_code

    @property
    def blank_label_symbol(self):
        return self._blank_label_symbol
