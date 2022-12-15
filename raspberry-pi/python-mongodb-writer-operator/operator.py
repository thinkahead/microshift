import kopf
from utils import initialize_kube, mongodb_client_from_env

initialize_kube()
mongodb_client = mongodb_client_from_env()

@kopf.on.create("demo.karve.com", "v1", "mongodb-writer")
def create_fn(spec, **kwargs):
    resource_namespace = kwargs["body"]["metadata"]["namespace"]
    resource_name = kwargs["body"]["metadata"]["name"]
    spec = kwargs["body"]["spec"]
    
    primary_id = resource_namespace + "/" + resource_name
    table, name, age, country = spec["table"], spec["name"], spec["age"], spec["country"]

    mongodb_client.insert_row(table, primary_id, name, age, country)
    
    return "Successfully wrote data corresponding to id: {id}, name: {name}, age: {age}, country: {country}".format(
        id=primary_id, 
        name=name, 
        age=age, 
        country=country
    )

@kopf.on.update("demo.karve.com", "v1", "mongodb-writer")
def update_fn(spec, **kwargs):
    resource_namespace = kwargs["body"]["metadata"]["namespace"]
    resource_name = kwargs["body"]["metadata"]["name"]
    spec = kwargs["body"]["spec"]
    
    primary_id = resource_namespace + "/" + resource_name
    table, name, age, country = spec["table"], spec["name"], spec["age"], spec["country"]

    mongodb_client.update_row(table, primary_id, name, age, country)
    
    return "Successfully updated data corresponding to id: {id}, name: {name}, age: {age}, country: {country}".format(
        id=primary_id, 
        name=name, 
        age=age, 
        country=country
    )

@kopf.on.delete("demo.karve.com", "v1", "mongodb-writer")
def delete_fn(spec, **kwargs):
    resource_namespace = kwargs["body"]["metadata"]["namespace"]
    resource_name = kwargs["body"]["metadata"]["name"]
    spec = kwargs["body"]["spec"]
    
    primary_id = resource_namespace + "/" + resource_name
    table = spec["table"]

    mongodb_client.delete_row(table, primary_id)

    return "Successfully delete data corresponding to id: {id}".format(id=primary_id)
