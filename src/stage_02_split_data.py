from src.utils.all_utils import read_yaml
import argparse
import pandas as pd
import os
from src.utils.all_utils import create_directory, save_local_df
from sklearn.model_selection import train_test_split

def split_and_save(config_path,params_path):
    config = read_yaml(config_path)
    params = read_yaml(path_to_yaml=params_path)
    
    artifacts_dir = config["artifacts"]["artifacts_dir"]
    local_data_path = config["artifacts"]["raw_local_dir"]
    local_file_name = config["artifacts"]["raw_local_file"]
    
    
    raw_local_dir_path = os.path.join(artifacts_dir,local_data_path)
    raw_local_file_path = os.path.join(raw_local_dir_path,local_file_name)
    df= pd.read_csv(raw_local_file_path)

    split_data_dir = config["artifacts"]["split_data_dir"]
    train_data_filename = config["artifacts"]["train_data"]
    test_data_filename = config["artifacts"]["test_data"]

    test_size =  params["base"]["test_size"]
    random_state = params["base"]["random_state"]
    
    split_data_dir_path = os.path.join(artifacts_dir,split_data_dir)
    create_directory([split_data_dir_path])

    train_data_filename_path = os.path.join(split_data_dir_path,train_data_filename)
    test_data_filename_path = os.path.join(split_data_dir_path,test_data_filename)

    

    train,test = train_test_split(df,test_size= test_size,random_state= random_state)

    save_local_df(train,train_data_filename_path)
    save_local_df(test,test_data_filename_path)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default="config/config.yaml")
    args.add_argument("--params","-p",default="params.yaml")

    parsed_args = args.parse_args()

    split_and_save(config_path= parsed_args.config,params_path= parsed_args.params)