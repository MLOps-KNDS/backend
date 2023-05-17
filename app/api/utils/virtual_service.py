from kubernetes import client, config

# from utils.constants import Constants

class VirtualService: 
    """
    Creates virtual service for our
    API endpoints
    """

    def __init__(self) -> None:
        """
        :param name: Name of the deployment and service. Must be unique 
        :param host: website, an API endpoint, or any other service accessible via a domain name
        """
        
        self.name = "example_name"
        self.host = "example_host"
        # [services]?

        config.load_incluster_config()

    def create(self):

        custom_api = client.CustomObjectsApi()

        group = "networking.istio.io"
        version = "v1alpha3"
        namespace = "default"

        body = {
        "apiVersion": f"{group}/{version}",
        "kind": "VirtualService",
        "metadata": {"name": self.name},
        "spec": {
            "hosts": self.host,  # what is a valid host?
            "http": [
                {
                    "route": [
                        {
                            "destination": {
                                "host": "my_service",  # service where we should be forwarded
                                "port": {
                                    "number": 80
                                },
                                "weight": 100  # % of traffic which goes here
                            },
                            "match": {
                                "uri": {
                                    "prefix": "/user",
                                }
                            }
                        }
                    # (...) for every router we have, it has to be manually written more or less like above.
                    # more over the moment we implement OAuth the code will be changed again
                    # eventually we can write some kind  of "generator" of the router dicts, what shouldn't be that hard
                    ]
                }
            ]
            }
        }


        custom_api.create_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural="virtualservices",
            body=body
        )

#  based on:

# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CustomObjectsApi.md#create_namespaced_custom_object

# https://stackoverflow.com/questions/67252594/k8s-volumesnapshot-is-created-but-it-returns-409-error-message-in-python-k8s-cli


