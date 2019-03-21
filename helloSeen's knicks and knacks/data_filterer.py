import json
import pandas as pd
import os

with open("truth.json","r") as read_file:
    data = json.load(read_file)

column_details = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
train_list = []
test_list = []
data_split = 1867
for image_name, coord in data.items():
     data_split = data_split-1
     de_list = coord[0]
     if (len(de_list)==0):
         os.rename("Data_Training/"+ image_name, "Data_Training/removed/" + image_name)
         continue
     loop_dict = {"filename": image_name, "width": 1296, "height": 864, "class": "drone_gate"}
     x_list = de_list[::2]
     x_max = max(x_list)
     x_min = min(x_list)
     y_list = de_list[1::2]
     y_max = max(y_list)
     y_min = min(y_list)
     loop_dict.update({"xmin": x_min,"ymin": y_min,"xmax": x_max,"ymax": y_max})
     if (data_split > 0):
         test_list.append(loop_dict)
         os.rename("Data_Training/"+ image_name, "Data_Training/Train/" + image_name)
     else:
         train_list.append(loop_dict)
        test_df.append([image_name,1296,864,'drone_gate',x_min,y_min,x_max,y_max])
train_df = pd.DataFrame(train_list)
test_df = pd.DataFrame(test_list)
train_df.to_csv('train_labels.csv', index = None)
test_df.to_csv('test_labels.csv', index = None)
