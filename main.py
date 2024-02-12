import random
import os
def main(input_dir, mask_dir,weight_dir,
    image_height=256,
    image_width=256,
    image_channel=3,
    img_size = (256,256),
    num_classes = 1,
    batch_size = 8,
    epochs=100,
    val_samples = 40,):

    img_size = (image_height,image_width)
    input_img_paths = sorted(
    [
        os.path.join(input_dir, fname)
        for fname in os.listdir(input_dir)
    ]
    )
    mask_img_paths = sorted(
    [
        os.path.join(mask_dir, fname)
        for fname in os.listdir(mask_dir)
    ]
    )
    random.Random(1337).shuffle(input_img_paths)
    random.Random(1337).shuffle(mask_img_paths)
    train_input_img_paths = input_img_paths[:-val_samples]
    train_mask_img_paths = mask_img_paths[:-val_samples]
    val_input_img_paths = input_img_paths[-val_samples:]
    val_mask_img_paths = mask_img_paths[-val_samples:]

    # Instantiate data Sequences for each split
    train_gen = Loader(
        batch_size, img_size, train_input_img_paths, train_mask_img_paths,image_channel,num_classes
    )
    val_gen = Loader(batch_size, img_size, val_input_img_paths, val_mask_img_paths,image_channel,num_classes)
    
    model=SAC_UWNet((image_height,image_width,image_channel),num_classes, dropout_rate=0.0, batch_norm=True)

    model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=weight_dir+"\\weights.h5",
    save_weights_only=True,
    monitor='val_loss',
    mode='min',
    save_best_only=True
    )
    rlp =tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.001,
    patience=10,
    verbose=1,
    mode='auto',
    min_delta=0.00005)
    #es=tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=15)
    history = model.fit(train_gen,validation_data=val_gen,epochs=epochs,callbacks=[checkpoint_callback,rlp])

if __name__ == "__main__":
    img_dir = sys.argv[1]
    mask_dir = sys.argv[2]
    weight_dir = sys.argv[3]
    main(img_dir,mask_dir,weight_dir)