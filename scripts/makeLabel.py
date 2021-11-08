import os
import glob
import io
import argparse
import json # 추가

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
# import tensorflow.compat.v1 as tf

# Initiate argument parser
parser = argparse.ArgumentParser(
    description="JSON-to-TEXT converter") # 수정
parser.add_argument("-j", # 수정
                    "--json_dir", # 수정
                    help="Path to the folder where the input .json files are stored.",
                    type=str)

args = parser.parse_args()


def json_to_txt(path): # 수정
    print(path)
    
    for json_file in glob.glob(path +"/**/*.json"):
        print(json_file)
        with open(json_file) as jf:
            json_data = json.load(jf)
                
            points = json_data['label_info']['shapes'][0]['points']
                    
            min_x = 3000000
            min_y = 3000000
            max_x = -1
            max_y = -1
                
            for i in range(len(points)):
                points[i][0] = int(points[i][0])
                points[i][1] = int(points[i][1])
                if points[i][0] > max_x:
                    max_x = points[i][0]
                if points[i][0] < min_x:
                    min_x = points[i][0]
                if points[i][1] > max_y:
                    max_y = points[i][1]
                if points[i][1] < min_y:
                    min_y = points[i][1]
        
            width = json_data['label_info']['image']['width']
            height = json_data['label_info']['image']['height']
            
            if json_data['label_info']['shapes'][0]['grade'] == '1++':
                label = 0
            elif json_data['label_info']['shapes'][0]['grade'] == '1+':
                label = 1
            elif json_data['label_info']['shapes'][0]['grade'] == "1":
                label = 2
            elif json_data['label_info']['shapes'][0]['grade'] == "2":
                label = 3
            elif json_data['label_info']['shapes'][0]['grade'] == "3":
                label = 4

            min_x /= width
            max_x /= width
            min_y /= height
            max_y /= height

            center_x = (min_x + max_x)/2
            center_y = (min_y + max_y)/2
 
            object_width = (max_x - min_x)
            object_height = (max_y- min_y)
            
            SAVE_PATH = json_file.split(".")[0]+".txt"

            with open(SAVE_PATH, 'wt') as fw:
                print(SAVE_PATH)
                str = f"{label} {center_x} {center_y} {object_width} {object_height}" 
                fw.writelines(str)
            


def remove_json(path):
    for json_file in glob.glob(path +"/**/*.json"):
        os.remove(json_file)


def main():
    json_to_txt(args.json_dir) # JSON 파일  
    remove_json(args.json_dir) # JSON 파일 삭제
    

if __name__ == '__main__':
    main()