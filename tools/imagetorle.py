import pycocotools.mask as m
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import json


def mask2rle(img):
    rle = m.encode(np.asfortranarray(img))
    return rle

def rle2mask(rle, imgshape):
    mask = m.decode(rle)
    mask = np.array(mask, dtype=np.uint8)
    mask = mask.reshape(imgshape, order='F')
    return mask

def convertAll():
    folder = "masks/side_masks/train_masks/"
    
    filenamesRLE = {}
    # Iterate over each image file in the folder
    for filename in os.listdir(folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Load the image
            image_path = os.path.join(folder, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            #Convert to binary
            image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
            # Convert the image to RLE
            rle_data = mask2rle(image)
            # Decode the RLE
            #decoded_image = rle2mask(rle_data, (image.shape[0], image.shape[1]))
            #decoded_image = decoded_image.astype(np.uint8)
            #plt.imshow(decoded_image)
            #plt.title(filename)
            #plt.show()
            rle_counts = rle_data.get('counts').decode('utf-8')
            rle_size = rle_data.get('size')
            rle_string = {'size': rle_size, 'counts': rle_counts}
            filenamesRLE[filename] = rle_string

    
    return filenamesRLE

def checkRLE():
    with open('coco/train.json', 'r+') as wfile:
        data = json.load(wfile)
        data_annotations = data['annotations']
        data_images = data['images']
        file_names = {}

        for image in data_images:
            file_names[image['id']] = image['file_name']

        
        for image in data_annotations:
            decoded_image = rle2mask(image['segmentation'], (image['segmentation']['size'][0], image['segmentation']['size'][1]))
            decoded_image = decoded_image.astype(np.uint8) 
            plt.imshow(decoded_image)
            plt.title(file_names[image['image_id']])
            plt.show()


    

def writetoCoco(rledata):
    data = None
    with open('coco/train.json', 'r+') as wfile: 
        data = json.load(wfile)
        data_annotations = data['annotations']
        data_images = data['images']
        file_names = {}

        for image in data_images:
            file_names[image['id']] = image['file_name']

        #For each image print the annotations
        for image in data_annotations:
            id = image['image_id']
            image['segmentation'] = rledata[file_names[id]]

                
    with open('coco/train.json', 'w') as newfile:
        json.dump(data, newfile)


if __name__ == '__main__':
    rledata = convertAll()
    writetoCoco(rledata)
    #checkRLE()

            