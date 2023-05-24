#!/usr/bin/env python3

import os
import argparse

from time import time

import sklearn.model_selection
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf

from termcolor import colored
from tensorflow import keras

# own libs
import lib.data_utils as data_utils


def mlp(nfeats, dense_layers, nodes, loss, optimizer, activation):
    model_ = keras.models.Sequential()
    model_.add(keras.layers.Input(shape=(nfeats)))
    for i in range(dense_layers):
        model_.add(
            keras.layers.Dense(
                nodes, activation=activation, kernel_initializer="lecun_normal"
            )
        )
    model_.add(keras.layers.Dense(1))
    model_.compile(loss=loss, optimizer=optimizer)
    model_.summary()
    return model_


def parse_args():
    parser = argparse.ArgumentParser(description="ML fun with higgsinos.")
    parser.add_argument(
        "--in_sig",
        help="Path to training signal sample.",
        default="data/higgs_sig.root",
    )
    # orig name:
    #  higfeats_raw_pico_SMS-TChiHH_HToBB_HToBB_3D_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISummer16NanoAODv5__PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7_train.root
    parser.add_argument(
        "--in_bkg",
        help="Path to training background sample.",
        default="data/higgs_bkg.root",
    )
    # orig name:
    #   higfeats_merged_pico_preselect_higloose_met150_TTJets_SingleLeptFromT_genMET-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_higmc_higloose_nfiles_28.root

    parser.add_argument("--cpu", help="Use cpu", action="store_true")
    parser.add_argument(
        "-t", "--tag", help="Any tag to add to output filenames.", default="MLP"
    )
    parser.add_argument("-e", "--epochs", type=int, help="Number of epochs", default=30)
    parser.add_argument(
        "-d", "--dense", type=int, help="Number of dense layers", default=5
    )
    parser.add_argument(
        "-n", "--nodes", type=int, help="Number of nodes per dense layer.", default=200
    )
    parser.add_argument(
        "--nent", type=int, help="Number of entries to read from data.", default=-1
    )
    parser.add_argument("--activation", help="Activation function", default="elu")
    parser.add_argument("--loss", help="Loss function.", default="mean_absolute_error")
    parser.add_argument("--optimizer", help="Optimizer.", default="adam")
    parser.add_argument(
        "--train_bkg",
        action="store_true",
        help="Use a mix of background and signal for the training",
    )
    parser.add_argument(
        "--log_transform",
        action="store_true",
        help="Take the log of jet_pt, jet_m, mjj, mhiggs, i.e. all variables in GeV as of now.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.cpu:
        print("Force to running on CPU instead of GPU")
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        print("Using " + colored(gpus[0], "green"))
    else:
        print("Using " + colored("CPU", "yellow"))

    t0 = time()
    np.set_printoptions(precision=2, suppress=True)
    # np.set_printoptions(threshold=sys.maxsize)

    model_name = args.tag + "-%ix%i_%s_%s_%s_e%i" % (
        args.dense,
        args.nodes,
        args.loss,
        args.optimizer,
        args.activation,
        args.epochs,
    )
    if args.log_transform:
        model_name += "_log"
    model_name = model_name.replace(".", "p")
    print("Model name set to: " + colored(model_name, "green"))

    x_data, y_data = data_utils.get_data(
        model_name="gen/" + model_name,
        path_sig=args.in_sig,
        path_bkg="",  # NOTE: the 'higgs_bkg.root' is UNUSED!
        do_log=args.log_transform,
        training=True,
        nent=args.nent,
    )
    x_train, x_val, y_train, y_val = sklearn.model_selection.train_test_split(
        x_data, y_data, test_size=0.1, shuffle=False
    )

    print(colored("\nTook %.0f seconds to prepare data." % (time() - t0), "green"))
    t1 = time()

    model = mlp(
        x_train.shape[1],
        args.dense,
        args.nodes,
        args.loss,
        args.optimizer,
        args.activation,
    )

    history = model.fit(
        x_train,
        y_train,
        epochs=int(args.epochs),
        validation_data=(x_val, y_val),  # validation_split=args.val_frac,
        batch_size=1024,
    )
    # callbacks=[tensorboard_callback])

    print(colored("\nTook %.0f seconds to train data." % (time() - t1), "green"))

    model.save("gen/" + model_name + ".h5")

    hdf = pd.DataFrame(history.history)
    hdf.plot(figsize=(8, 5))
    plt.grid(True)
    plt.savefig("gen/history_" + model_name + ".pdf")
    print("\nLoss - validation loss plot:")
    print("    gen/history_" + model_name + ".pdf")

    print(
        colored(
            "\nProgram took %dm %.0fs." % ((time() - t0) // 60, (time() - t0) % 60),
            "green",
        )
    )
