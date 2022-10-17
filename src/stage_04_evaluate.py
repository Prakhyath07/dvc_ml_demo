from src.utils.all_utils import read_yaml, store_reports, create_directory
import argparse
import pandas as pd
import os
import joblib
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import math


def evaluate_metrics(preds,test_y):

    r2_= r2_score(test_y,preds)
    mae = mean_absolute_error(test_y,preds)

    mse = mean_squared_error(test_y,preds)

    rmse = math.sqrt(mse)


    return r2_, rmse, mae

def evaluate(config_path):
    config = read_yaml(config_path)
    
    
    artifacts_dir = config["artifacts"]["artifacts_dir"]

    split_data_dir = config["artifacts"]["split_data_dir"]
    test_data_filename = config["artifacts"]["test_data"]
    
    
    split_data_dir_path = os.path.join(artifacts_dir,split_data_dir)
   
    test_data_filename_path = os.path.join(split_data_dir_path,test_data_filename)

    test_df= pd.read_csv(test_data_filename_path)
    target = "quality"

    test_y = test_df[target]
    test_x = test_df.drop(target,axis=1)

    model_dir = config["artifacts"]["model_dir"]
    model_name = config["artifacts"]["model_name"]
    model_dir_path = os.path.join(artifacts_dir,model_dir)
    model_name_path = os.path.join(model_dir_path,model_name)

    model = joblib.load(model_name_path)

    preds = model.predict(test_x)
    
    r2_score, rmse, mae = evaluate_metrics(preds= preds, test_y= test_y)

    report_dir = config["artifacts"]["report_dir"]
    report_name = config["artifacts"]["report_name"]
    
    
    report_dir_path = os.path.join(artifacts_dir,report_dir) 
    report_name_path = os.path.join(report_dir_path,report_name)

    create_directory([report_dir_path])

    report_dict ={"r2_score": r2_score,
                "rmse": rmse,
                "mae": mae
                }

    store_reports(report_dict,report_name_path)




    

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default="config/config.yaml")

    parsed_args = args.parse_args()

    evaluate(config_path= parsed_args.config)