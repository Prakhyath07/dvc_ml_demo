import yaml
import os

def read_yaml(path_to_yaml: str)->dict:
    with open(path_to_yaml, "r") as yaml_file:
        content = yaml.safe_load(yaml_file)

    return content

def create_directory(dirs: list):
    for dir in dirs:
        os.makedirs(dir,exist_ok =True)
        print(f"created directory {dir}")

def save_local_df(data,data_path, index = False, sep = ","):
    data.to_csv(data_path,index =index,sep=sep)
    print(f"data frame saved at {data_path}")

