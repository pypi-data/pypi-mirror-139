#----- 16th Feb 2022 -----#
#----- ZhangLe -----------#
#----- Modeling ----------#

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense

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
  modelLSTM = Sequential(name='LSTM Model('+ size +')')
  modelLSTM.add(LSTM(NUM_NEURONS_FirstLayer, input_shape=(look_back, n_features), name='LSTM_layer_1', return_sequences=True))
  modelLSTM.add(Dropout(dropout, name='dropout_layer_1'))
  if size == 'large':
    modelLSTM.add(LSTM(NUM_NEURONS_SecondLayer, input_shape=(look_back, n_features), name='LSTM_layer_2', return_sequences=True))
    modelLSTM.add(Dropout(dropout, name='dropout_layer_2'))
  modelLSTM.add(Dense(look_forward, name='dense_output_layer'))
  modelLSTM.compile(loss='mean_squared_error', optimizer='adam')
  if print_summary:
    print(modelLSTM.summary())
  return modelLSTM


# 2. lstm (customize)
def lstm_model_custmize(look_back, look_forward, n_features, dropout=0.5, print_summary=False, layer_number = 1, n_neurons = [128]):
  modelLSTM = Sequential(name='LSTM Model(customized)')
  modelLSTM.add(LSTM(n_neurons[0], input_shape=(look_back, n_features), name='LSTM_layer_1', return_sequences=True))
  modelLSTM.add(Dropout(dropout, name='dropout_layer_1'))
  i = 2
  for layer in n_neurons[1:]:
    modelLSTM.add(LSTM(layer, input_shape=(look_back, n_features), name='LSTM_layer_'+str(i), return_sequences=True))
    modelLSTM.add(Dropout(dropout, name='dropout_layer'+str(i)))
    i = i + 1
  modelLSTM.add(Dense(look_forward, name='dense_output_layer'))
  modelLSTM.compile(loss='mean_squared_error', optimizer='adam')
  if print_summary:
    print(modelLSTM.summary())
  return modelLSTM