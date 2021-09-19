from typing import Dict, Iterable

import kfp
from kfp import dsl

redis1 = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "labels": [{"app": "redis"}],
        "name": "redis1",
    },
    "spec": {
        "containers": [
            {
                "image": "redis",
                "name": "redis1",
            }
        ]
    },
}

redis2 = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "labels": [{"app": "redis"}],
        "name": "redis2",
    },
    "spec": {
        "containers": [
            {
                "image": "redis",
                "name": "redis2",
            }
        ]
    },
}


def cleanup_op(resources: Iterable[Dict]) -> dsl.ContainerOp:
    """Cleanup all the resources created by ResourceOp.
    Args:
        resources (Iterable[Dict]): List of k8s Manifests.
    Returns:
        dsl.ContainerOp: Container OP to delete the resources by k8s API.
    """

    script = ""
    for r in resources:
        # script += `kubectl delete <kind> <name>`
        script += f"kubectl delete {r['kind'].lower()} {r['metadata']['name']};"

    return dsl.ContainerOp("cleanup", "bitnami/kubectl", ["/bin/bash", "-c", script])


@dsl.pipeline(
    name="ContainerOp with ExitHandler",
    description="Shows how to delete resources created by dsl.ResourceOp by using dsl.ExitHandler",
)
def pipeline():
    exit_task = cleanup_op([redis1, redis2])
    with dsl.ExitHandler(exit_task):
        _ = kfp.dsl.ResourceOp(
            name="create-redis1",
            k8s_resource=redis1,
            action="create",
            success_condition="status.phase=Running",
            failure_condition="status.phase=Failed",
            attribute_outputs={"name": "{.metadata.name}"},
        )
        _ = kfp.dsl.ResourceOp(
            name="create-redis2",
            k8s_resource=redis2,
            action="create",
            success_condition="status.phase=Running",
            failure_condition="status.phase=Failed",
            attribute_outputs={"name": "{.metadata.name}"},
        )


if __name__ == "__main__":
    kfp.compiler.Compiler.compile(pipeline, "pipeline.yaml")
