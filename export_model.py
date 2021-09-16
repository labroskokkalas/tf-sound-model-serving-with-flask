model.load_weights('./weights.h5')
MODEL_DIR = 'tensorflow-server'
version = 1
export_path = os.path.join(MODEL_DIR, str(version))

tf.keras.models.save_model(
    model_predict,
    export_path,
    overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None
)

