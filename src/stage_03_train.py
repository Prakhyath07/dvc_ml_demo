from src.utils.all_utils import read_yaml
import argparse
import pandas as pd
import os
from src.utils.all_utils import create_directory
from sklearn.linear_model import ElasticNet
import joblib

def train(config_path,params_path):
    config = read_yaml(config_path)
    params = read_yaml(path_to_yaml=params_path)
    
    
    artifacts_dir = config["artifacts"]["artifacts_dir"]

    split_data_dir = config["artifacts"]["split_data_dir"]
    train_data_filename = config["artifacts"]["train_data"]
    
    
    
    split_data_dir_path = os.path.join(artifacts_dir,split_data_dir)
   
    train_data_filename_path = os.path.join(split_data_dir_path,train_data_filename)

    train_df= pd.read_csv(train_data_filename_path)
    target = "quality"

    train_y = train_df[target]
    train_x = train_df.drop(target,axis=1)

    alpha = params["model_params"]["ElasticNet"]["alpha"]
    l1_ratio = params["model_params"]["ElasticNet"]["l1_ratio"]
    random_state = params["base"]["random_state"]

    model = ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=random_state)
    model.fit(train_x,train_y)

    model_dir = config["artifacts"]["model_dir"]
    model_name = config["artifacts"]["model_name"]
    model_dir_path = os.path.join(artifacts_dir,model_dir)
    model_name_path = os.path.join(model_dir_path,model_name)

    create_directory([model_dir_path])
    joblib.dump(model,model_name_path)


    

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default="config/config.yaml")
    args.add_argument("--params","-p",default="params.yaml")

    parsed_args = args.parse_args()

    train(config_path= parsed_args.config,params_path= parsed_args.params)