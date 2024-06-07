import shutil
import os


def move_dir(src_path, dest_path, new_name):
    new_path = f"{dest_path}/{new_name}"
    shutil.move(f"{src_path}", new_path)


#check if their is already a folder with images and delte it if it exists 
if os.path.isdir("/home/ethan/d2.cattle/datasets/keypoints/coco_format/test_imgs"):
    shutil.rmtree("/home/ethan/d2.cattle/datasets/keypoints/coco_format/test_imgs")

#get one video from Frames folder
frames = "datasets/keypoints/coco_format/Frames"
files = os.listdir(frames)
num = files[0]


src = frames+ "/" + num

done = "/home/ethan/d2.cattle/datasets/keypoints/coco_format/done/" + num
shutil.copytree(src, done)

#move the folder to right place and name it properly for inference
dst = "/home/ethan/d2.cattle/datasets/keypoints/coco_format/"
move_dir(src,dst,"test_imgs")

#copy right json file too
src = "/home/ethan/d2.cattle/datasets/keypoints/coco_format/image_jsons/" + num + ".json"
dst = "/home/ethan/d2.cattle/datasets/keypoints/coco_format/annotations/test_infer.json"
if os.path.isfile(dst):
    os.remove(dst)
shutil.copyfile(src,dst)


#after inference convert file to right format and move it to folder with inferences 
exec(open('json_convert.py').read())

src = "/home/ethan/d2.cattle/data/train_outputs/test/inference/metadata_csharp.json"
dst = "/home/ethan/d2.cattle/datasets/keypoints/coco_format/inferences/" + num + ".json"
shutil.copyfile(src,dst)