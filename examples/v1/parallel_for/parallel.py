import kfp
from kfp import dsl
from kfp.components import func_to_container_op


@func_to_container_op
def list_generator_op(n: int) -> str:
    """Generate list for parallel"""
    import json

    # JSON payload is required for ParallelFor
    return json.dumps([x for x in range(n)])


@func_to_container_op
def print_op(msg: str):
    """Print message."""
    print(msg)


@dsl.pipeline(
    name="ParallelFor example",
    description="Shows how to use dsl.ParallelFor()",
)
def pipeline(n: int):
    list_task = list_generator_op(n)
    parallel_taks = dsl.ParallelFor(list_task.output)
    with parallel_taks as msg:
        print_op(msg)

    print_op("Finished").after(parallel_taks)


if __name__ == "__main__":
    # Compile the pipeline
    kfp.compiler.Compiler().compile(pipeline, "pipeline.yaml")
