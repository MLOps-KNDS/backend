from kubernetes import client, config
from fastapi import APIRouter
from utils.model_deployment import ModelDeployment

router = APIRouter(prefix="/deployment", tags=["deployment"])


@router.get("/get-pods")
async def get_pods():
    config.load_incluster_config()

    v1 = client.CoreV1Api()

    result = {}
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for index, i in enumerate(ret.items):
        result[
            index
        ] = f"{i.status.pod_ip} -- {i.metadata.namespace} -- {i.metadata.name}"

    return result


@router.put("/")
async def put_pod():
    model_deployment = ModelDeployment(
        "c48d99d17e5042c18742ab10bfcc5edd", 1, 1, 1, 1, 1
    )
    model_deployment.deploy()
