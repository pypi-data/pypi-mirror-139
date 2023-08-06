#----- 16th Feb 2022 -----#
#----- ZhangLe -----------#
#----- Modeling ----------#

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from keras.callbacks import EarlyStopping
import tensorflow as tf
import numpy as np
from ds_common_tool import suite_data

# 1. lstm (simple)
# tested
def lstm_model(look_back, look_forward, n_features, dropout=0.5, print_summary=False, size = 'small'):
  if size == 'small':
    NUM_NEURONS_FirstLayer = 128
  elif size == 'medium':
    NUM_NEURONS_FirstLayer = 256
  else:
    NUM_NEURONS_FirstLayer = 256
    NUM_NEURONS_SecondLayer = 128
  modelLSTM = Sequential(name='LSTM_Model_'+ size)
  modelLSTM.add(LSTM(NUM_NEURONS_FirstLayer, input_shape=(look_back, n_features), name='LSTM_layer_1', return_sequences=True))
  modelLSTM.add(Dropout(dropout, name='dropout_layer_1'))
  if size == 'large':
    modelLSTM.add(LSTM(NUM_NEURONS_SecondLayer, input_shape=(NUM_NEURONS_FirstLayer, 1), name='LSTM_layer_2'))
    modelLSTM.add(Dropout(dropout, name='dropout_layer_2'))
  modelLSTM.add(Dense(look_forward, name='dense_output_layer'))
  modelLSTM.compile(loss='mean_squared_error', optimizer='adam')
  if print_summary:
    print(modelLSTM.summary())
  return modelLSTM


# 2. lstm (customize)
def lstm_model_custmize(look_back, look_forward, n_features, dropout=0.5, print_summary=False, n_neurons = [128]):
  modelLSTM = Sequential(name='LSTM_Model_customized')
  modelLSTM.add(LSTM(n_neurons[0], input_shape=(look_back, n_features), name='LSTM_layer_1', return_sequences=True))
  modelLSTM.add(Dropout(dropout, name='dropout_layer_1'))
  if len(n_neurons) == 1:
    modelLSTM.add(LSTM(look_forward, name='LSTM_layer_2'))
  for layer_i in range(1, len(n_neurons) - 1):
    modelLSTM.add(LSTM(n_neurons[layer_i], input_shape=(n_neurons[layer_i - 1], n_features), name='LSTM_layer_'+str(layer_i + 1), return_sequences=True))
    modelLSTM.add(Dropout(dropout, name='dropout_layer_'+str(layer_i + 1)))
  if len(n_neurons) > 1:
    modelLSTM.add(LSTM(n_neurons[-1], input_shape=(n_neurons[-2], 1), name='LSTM_layer_'+str(len(n_neurons))+''))
  modelLSTM.add(Dense(look_forward, name='dense_output_layer'))
  modelLSTM.compile(loss='mean_squared_error', optimizer='adam')
  if print_summary:
    print(modelLSTM.summary())
  return modelLSTM

# 3. train model
# tested
def train_model(model, X_train_seq, y_train_seq, X_val_seq, y_val_seq, 
                epochs=100, early_stop = True, patience=10, 
                save_model = False, model_path='', checkpoint_path='',
                show_loss = True):
  if not early_stop:
    patience = epochs
  early_stopping = EarlyStopping(monitor='val_loss', 
                              min_delta=0, 
                              patience=patience, 
                              verbose=0, 
                              mode='auto', 
                              baseline=None, 
                              restore_best_weights=False)
  if save_model:
    cp_callback = tf.keras.callbacks.ModelCheckpoint(model_path, 
                                                 monitor='val_loss', 
                                                 save_best_only=True, 
                                                 # save_weights_only=True,
                                                 verbose=1)
    history = model.fit(X_train_seq, y_train_seq,
                    epochs=epochs,
                    validation_data=(X_val_seq, y_val_seq),
                    shuffle=True,
                    batch_size=32,
                    verbose=1,
                    callbacks=[early_stopping, cp_callback])
    model.save_weights(checkpoint_path)
  else:
    history = model.fit(X_train_seq, y_train_seq,
                    epochs=epochs,
                    validation_data=(X_val_seq, y_val_seq),
                    shuffle=True,
                    batch_size=32,
                    verbose=1,
                    callbacks=[early_stopping])
  if show_loss:
    label_list = [i for i in range(0, len(history.history['loss']))]
    suite_data.show_draft_plot(datas = [history.history['loss'], history.history['val_loss']], x_label = label_list, title = 'Loss of Model', legend=['loss', 'val loss'])
  return model

# 4. check matric mae, mape, mse, rmse
def check_result_metric(y_true, y_pred, methods=['mae'], print_result=True):
  mae, mape = 0, 0
  if 'mae' in methods:
    mae = np.mean(np.abs(y_true - y_pred))
    if print_result:
      print('MAE :', round(mae, 2))
  if 'mape' in methods:
    mape = 100 - np.mean(np.abs(y_true - y_pred) / y_true) * 100
    if print_result:
      print('MAPE :', round(mape, 2), '%')
  return mae, mape
  