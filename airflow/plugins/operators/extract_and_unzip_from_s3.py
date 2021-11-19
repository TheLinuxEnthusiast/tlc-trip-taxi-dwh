import boto3
import zipfile
import json
import io
import os
import configparser

#import pandas as pd
import geopandas as gpd

def extract_and_unzip_from_s3(*args, **kwargs):
    """
    Description: 
        Custom function that extracts Shape files to a local S3 bucket, Converts shape data to Latitude, Longitude and Calculates Centroid of Geometry Object.
        Requires aws-master.cfg to be set before running.
    
    Arguments:
        Kwargs: Home directory
                source_bucket_name
                source_key
                dest_bucket_name
                dest_key
    
    Returns:
        None
    """
    
    source_bucket_name = kwargs['source_bucket_name']
    source_key = kwargs['source_key']
    dest_bucket_name = kwargs['dest_bucket_name']
    dest_key = kwargs['dest_key']
    home_=kwargs['HOME_']
    tmp_dir = f"{home_}/tmp"
    
    config = configparser.ConfigParser()
    config.read(f"{home_}/aws-master.cfg")
    
    AWS_ACCESS_KEY = config['MASTER']['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = config['MASTER']['AWS_SECRET_KEY']
    
    #Clear tmp directory
    for f in os.listdir(f"{tmp_dir}"):
        if os.path.isfile(f"{tmp_dir}/{f}"):
            os.remove(f"{tmp_dir}/{f}")
        elif f == "modified":
            for i in os.listdir(f"{tmp_dir}/modified"):
                os.remove(f"{tmp_dir}/modified/{i}")
    
    #Source
    session_source = boto3.session.Session(
        aws_access_key_id=f"{AWS_ACCESS_KEY}", 
        aws_secret_access_key=f"{AWS_SECRET_KEY}"
    )
    s3_source = session_source.resource("s3")
    bucket_source = s3_source.Bucket(f'{source_bucket_name}')
    obj = bucket_source.Object(f'{source_key}')
    
    with io.BytesIO(obj.get()["Body"].read()) as tf:
        
        tf.seek(0)

        with zipfile.ZipFile(tf, mode='r') as zipf:
            zipf.extractall(f"{tmp_dir}")
            #for subfile in zipf.namelist():
            #    print(subfile)
    
    #Read shape file and Add centroid to shape file
    df_geo = gpd.read_file(f"{tmp_dir}/taxi_zones.shp")
    df_geo = df_geo.to_crs(epsg=3035)
    df_geo = df_geo.to_crs(epsg=4326)
    df_geo["x"] = df_geo.geometry.centroid.x
    df_geo["y"] = df_geo.geometry.centroid.y
    df_geo.to_file(f"{tmp_dir}/modified/taxi_zones_adj.shp")
    
    #Destination
    session_dest = boto3.session.Session(
        aws_access_key_id=f"{AWS_ACCESS_KEY}", 
        aws_secret_access_key=f"{AWS_SECRET_KEY}"
    )
    s3_dest = session_dest.resource("s3")
    #bucket_dest = s3_dest.Bucket(f'{dest_bucket_name}')
    
    for file in os.listdir(f"{tmp_dir}/modified"):
        s3_dest.meta.client.upload_file(f"{tmp_dir}/modified/{file}", dest_bucket_name, f"{dest_key}/{file}")
    

if __name__ == "__main__":
    kwargs_custom= {'source_bucket_name':'nyc-tlc', 'source_key':'misc/taxi_zones.zip', 'dest_bucket_name':'tlc-nyc-dwh-df', 'dest_key':'taxi_zones'}
    extract_and_unzip_from_s3(source_bucket_name = kwargs_custom['source_bucket_name'],
                              source_key=kwargs_custom['source_key'],
                              dest_bucket_name=kwargs_custom['dest_bucket_name'],
                              dest_key=kwargs_custom['dest_key'])
    
    
    
    
    
    
    
    