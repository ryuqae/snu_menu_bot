import os
import tensorflow as tf

if tf.config.list_physical_devices("GPU"):
    print("GPU is available")
else:
    print("GPU is NOT available")