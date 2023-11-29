import json
import os

#Opens raw data json file and creates a json object
with open('data/train_outputs/test/inference/coco_instances_results.json', 'r') as f:
    raw_data = json.load(f)
with open('datasets/keypoints/coco_format/annotations/test_infer.json', 'r') as g:
    id_data = json.load(g)
#Creates empty list to add dictionaries to
convert_data = []
image_name = {}

id = 0
current_index = 0
ids = id_data["images"]

for dict in id_data["images"]:
    image_id = {ids[id]["id"]: ids[id]["file_name"].replace(".jpg","")}
    image_name.update(image_id)
    id += 1
    
print(image_name)
id = 0
for dict in raw_data:
    #Rounds all float elements to integers
    current = raw_data[id]
    if current_index == current['image_id']:
        for i in range(13): 
            current['keypoints'][i*3] = round(current['keypoints'][i*3])
            current['keypoints'][i*3+1] = round(current['keypoints'][i*3+1])  
            current['keypoints'][i*3+2] = 1 
        for i in range(4):
            current['bbox'][i] = round(current['bbox'][i])
        #Adds a dictionary containing the keypoints and box data for each image to the list 'convert data' 
        convert_data.append({'id' : image_name[current["image_id"]], 'points': current['keypoints'], 'box' : current['bbox']})
        current_index += 1
    id += 1
#Overwrites raw data with new data
with open('data/train_outputs/test/inference/coco_instances_results.json', 'w') as j:
    json.dump(convert_data, j, indent =4) 


