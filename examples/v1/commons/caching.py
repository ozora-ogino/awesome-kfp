import kfp
from kfp import dsl
from kfp.components import func_to_container_op

pod = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "labels": [{"app": "redis"}],
        "name": "redis",
    },
    "spec": {
        "containers": [
            {
                "image": "redis",
                "name": "redis",
            }
        ]
    },
}


@func_to_container_op
def print_op(msg: str):
    """Print message"""
    print(msg)


@dsl.pipeline(name="sample pipeline", description="Shows how to use func_to_container_op")
def pipeline():
    # Disabling caching of ContainerOP
    add_task = print_op("Hello world!")
    add_task.execution_options.caching_strategy.max_cache_staleness = "P30D"

    # Disabling caching of ResourceOp
    dsl.ResourceOp(
        name="Create pos",
        action="create",
        k8s_resource=pod,
        success_condition="status.phase=Running",
        failure_condition="status.phase=Failed",
    ).add_pod_annotation("pipelines.kubeflow.org/max_cache_staleness", "P0D")


if __name__ == "__main__":
    # Compile the pipeline
    kfp.compiler.Compiler.compile(pipeline, "pipeline.yaml")
