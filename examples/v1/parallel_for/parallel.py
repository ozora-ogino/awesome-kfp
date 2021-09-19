import kfp
from kfp import dsl
from kfp.components import func_to_container_op


@func_to_container_op
def list_generator_op(parallelism: int) -> str:
    """Generate list for parallel"""
    import json

    # JSON payload is required for ParallelFor
    return json.dumps([x for x in range(parallelism)])


@func_to_container_op
def print_op(msg: str):
    """Print message."""
    print(msg)


@dsl.pipeline(
    name="ParallelFor example",
    description="Shows how to use dsl.ParallelFor()",
)
def pipeline(parallelism: int):
    # set the number of parallel
    default_conf = kfp.dsl.get_pipeline_conf()
    default_conf.set_parallelism(2)

    list_task = list_generator_op(parallelism)
    parallel_tasks = dsl.ParallelFor(list_task.output)
    with parallel_tasks as msg:
        print_op(msg)

    print_op("Finished").after(parallel_tasks)


if __name__ == "__main__":
    # Compile the pipeline
    kfp.compiler.Compiler().compile(pipeline, "pipeline.yaml")
