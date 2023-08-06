#----- 16th Feb 2022 -----#
#----- ZhangLe -----------#
#----- Modeling ----------#

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras import Input, Model
from tcn import TCN
from keras.callbacks import EarlyStopping
import tensorflow as tf
import numpy as np
from ds_common_tool import suite_data

# 1. lstm (simple)
# can see the example for understand parameters
def lstm_model_with_data_split(df, 
                              label_column, 
                              train_start, 
                              train_end, 
                              test_start, 
                              test_end, 
                              look_back, 
                              look_forward, 
                              column_set_index = 0,
                              split_n = 30,
                              lstm_n_neurons = [128],
                              print_model_summary = True,
                              dropout = 0.5,
                              epochs = 30,
                              patience = 5,
                              early_stop = True,
                              save_model = False,
                              model_path = '',
                              checkpoint_path = '',
                              show_loss = True,
                              show_result_plot = True,
                              plot_title = '',
                              evauate_metric = ['mape']):
  df = suite_data.switch_y_column(df, column_name=label_column)
  if column_set_index:
    df.set_index(column_set_index, inplace=True)
  train_data = df[train_start : train_end]
  test_data  = df[test_start : test_end]
  X_train_seq, y_train_seq = suite_data.split_sequence(train_data.values, look_back = look_back, look_forward = look_forward)
  X_test_seq, y_test_seq = suite_data.split_sequence(test_data.values, look_back = look_back, look_forward = look_forward)
  X_train_seq, y_train_seq, X_val_seq, y_val_seq = suite_data.time_split_dataset(X_train_seq, y_train_seq, split_n = split_n)
  lstmModel = lstm_model_custmize(look_back=look_back, look_forward=look_forward, n_features=X_train_seq.shape[2], dropout=dropout, print_summary=print_model_summary, n_neurons = lstm_n_neurons)
  if early_stop == False:
    patience = epochs
  if save_model:
    model_train = train_model(lstmModel, X_train_seq, y_train_seq, X_val_seq, y_val_seq, epochs=epochs, early_stop = early_stop, patience=patience, save_model = save_model, model_path=model_path, checkpoint_path=checkpoint_path, show_loss = show_loss)
  else:
    model_train = train_model(lstmModel, X_train_seq, y_train_seq, X_val_seq, y_val_seq, epochs=epochs, early_stop = early_stop, patience=patience, save_model = save_model, show_loss = show_loss)
  # print_result
  prediction = model_train.predict(X_test_seq)
  prediction = prediction[0]
  if show_result_plot:
    suite_data.show_draft_plot(datas=[prediction, y_test_seq[0]], x_label = test_data[test_start : test_end][-look_forward:].index, title=plot_title, legend=['pred', 'real'])
  mae, mape = check_result_metric(y_test_seq[0], prediction, methods=evauate_metric)
  return lstmModel, mae, mape, prediction


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

# 5. tcn model
def tcn_model(look_back, n_features, look_forward, batch_size=None, print_summary=True, n_neurons=[128]):
  tcn_units = []
  for index in range(len(n_neurons)):
    tcn_units.append('x'+str(index)+'_')
  
  input_ = Input(batch_shape=(batch_size, look_back, n_features), name='Input_Layer')
  if len(n_neurons) == 1:
    tcn_units[0] = TCN(nb_filters=n_neurons[0], 
                   kernel_size=2, 
                   nb_stacks=2, 
                   dilations=[1, 2, 4, 8, 16, 32], 
                   padding='causal', 
                   use_skip_connections=True, 
                   dropout_rate=0.5, 
                   return_sequences=False, 
                   activation='relu', 
                   kernel_initializer='he_normal',
                   name = 'TCN_Layer_1', use_batch_norm=True)(input_)
  else:
    tcn_units[0] = TCN(nb_filters=n_neurons[0], 
                   kernel_size=2, 
                   nb_stacks=2, 
                   dilations=[1, 2, 4, 8, 16, 32], 
                   padding='causal', 
                   use_skip_connections=True, 
                   dropout_rate=0.5, 
                   return_sequences=True, 
                   activation='relu', 
                   kernel_initializer='he_normal',
                   name = 'TCN_Layer_1', use_batch_norm=True)(input_)
  for index in range(len(tcn_units) - 2):
    tcn_units[index + 1] = TCN(nb_filters=n_neurons[index + 1], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                  padding='causal', use_skip_connections=True, dropout_rate=0.5, return_sequences=True, 
                  activation='relu', kernel_initializer='he_normal',
                  name = 'TCN_Layer_' + str(index + 2), use_batch_norm=True)(tcn_units[index])  # The TCN layer .
  if len(n_neurons) > 1:
    tcn_units[-1] = TCN(nb_filters=n_neurons[-1], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                  padding='causal', use_skip_connections=True, dropout_rate=0.5, return_sequences=False, 
                  activation='relu', kernel_initializer='he_normal',
                  name = 'TCN_Layer_' + str(len(n_neurons) + 1), use_batch_norm=True)(tcn_units[-2])  # The TCN layer .
  output_ = Dense(look_forward, name='Dense_Layer')(tcn_units[-1])
  modelTCN = Model(inputs=[input_], outputs=[output_], name='TCN_Model_customized')
  modelTCN.compile(optimizer='adam', loss='mse')
  if print_summary:
    print(modelTCN.summary())
  return modelTCN
  