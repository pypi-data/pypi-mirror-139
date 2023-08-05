## Functions included in data processing:

### 1. remove outlier  
### data.remove_outlier(df, column_name, n_outlier=0.25)    
|parameter|data type|description|default value|
|:---|:---|:---|:---| 
|**df**|dataframe|which need to filter the outlier|-|  
|**column_name**|string|column which need to filter the outlier|-|
|**n_outlier**|float|range (0, 1), quantile number|0.25|
|**return**|dataframe|new dataframe|-|  
  
example:  
```
from ds_common_tool import data  
  
new_df = data.remove_outlier(df, 'column_name', 0.25)
```  
  
### 2. Transfor period column into datetime   
### data.add_period_to_time(df, date_column_name='DATE', period_column_name='PERIOD', period_minutes=30)  
|parameter|data type|description|default value|  
|:---|:---|:---|:---|  
|**df**|dataframe|which need to transfer period columns into datetime|-|  
|**date_column_name**|string|date column|'DATE'|  
|**period_column_name**|string|period column|'PERIOD'|  
|**period_minutes**|int|time period|30|  
|**return**|dataframe|new dataframe|-|  

example:  
```
from ds_common_tool import data  
  
new_df = data.add_period_to_time(df, date_column_name='DATE', period_column_name='PERIOD', period_minutes=30) 
```  
     
  
## Functions included in model:
### 1. lstm model
### lstm_model(look_back, look_forward, n_features, dropout=0.5, print_summary=False, size = 'small')  
  
|parameter|data type|description|default value|  
|:---|:---|:---|:---|  
|**size**|string|size of lstm model, [small, medium, large], small: 1 layer with neurons number 128, medium: 1 layer with neurons number 256, large: with 2 layers, first layer neurons number 258, second layer neurons number 128. |'small'|  
|**look_back**|int|input size|-|  
|**look_forward**|int|output size|-|  
|**n_features**|int|number of features|-|  
|**dropout**|float|range (0,1)|0.5|   
|**print_summary**|boolean|True: will print out model summary. |False|  
|**return**|Model|lstm model|-|  
  
example:  
```
from ds_common_tool import model  
  
lstmModel = model.lstm_model(look_back=30, look_forward=30, n_features=4, dropout=0.5, print_summary=False, size = 'small')
```  
### 2. lstm model customized  
### lstm_model_custmize(look_back, look_forward, n_features, dropout=0.5, print_summary=False, n_neurons = [128])  
  
|parameter|data type|description|default value|  
|:---|:---|:---|:---|  
|**look_back**|int|input size|-|  
|**look_forward**|int|output size|-|  
|**n_features**|int|number of features|-|  
|**dropout**|float|range (0,1)|0.5| 
|**n_neurons**|int[]|neurons number of each layer, eg. [256, 128, 64]|[128| 
|**print_summary**|boolean|True: will print out model summary. |False|    
|**return**|Model|lstm model|-|  
  
example:    
```
from ds_common_tool import model  
  
lstmModel = model.lstm_model_custmize(look_back=30, look_forward=30, n_features=4, dropout=0.5, print_summary=False, n_neurons = [128])
```  
  
## [pypi](https://pypi.org/project/ds-common-tool/#description)