from fdrtd.plugins.simon.microservice import MicroserviceSimon


def list_root_objects():
    return [
        {
            "identifiers": {
                "namespace": "fdrtd",
                "protocol": "Simon",
                "version": "0.5.2"
            },
            "object": MicroserviceSimon()
        }
    ]
