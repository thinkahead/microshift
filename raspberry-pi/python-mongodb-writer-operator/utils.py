from kubernetes import config
from clients.mongodb import MongoDBClient
import os

def mongodb_client_from_env():
    MONGODB_HOST = os.getenv("MONGODB_HOST")
    MONGODB_PORT = os.getenv("MONGODB_PORT")
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
    MONGODB_DB = os.getenv("MONGODB_DB")

    client = MongoDBClient(MONGODB_HOST,MONGODB_USERNAME,MONGODB_PASSWORD,MONGODB_DB,MONGODB_PORT)
    return client

def initialize_kube():
    DEV = os.getenv('DEV')
    if DEV:
        print("Loading from local kube config")
        home = os.path.expanduser("~")
        kube_config_path = os.getenv("KUBE_CONFIG", home+"/.kube/config")
        config.load_kube_config(config_file=kube_config_path)
    else:
        print ("Loading In-cluster config")
        config.load_incluster_config()
