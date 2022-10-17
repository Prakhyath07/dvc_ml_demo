from src.utils.all_utils import read_yaml
import argparse
import pandas as pd
import os
from src.utils.all_utils import create_directory, save_local_df

def get_data(config_path):
    config = read_yaml(config_path)
    remote_data_path = config["data_source"]

    df= pd.read_csv(remote_data_path, sep=";")

    ## save data locally
    artifacts_dir = config["artifacts"]["artifacts_dir"]
    local_data_path = config["artifacts"]["raw_local_dir"]
    local_file_name = config["artifacts"]["raw_local_file"]
    
    raw_local_dir_path = os.path.join(artifacts_dir,local_data_path)
    raw_local_file_path = os.path.join(raw_local_dir_path,local_file_name)

    create_directory([raw_local_dir_path])

    save_local_df(data=df,data_path= raw_local_file_path)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default="config/config.yaml")

    parsed_args = args.parse_args()

    get_data(config_path= parsed_args.config)