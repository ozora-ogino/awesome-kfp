import kfp
from kfp import dsl
from kfp.components import func_to_container_op


@func_to_container_op
def add_op(a: float, b: float) -> float:
    """Calculates sum of two arguments"""
    return a + b


@func_to_container_op
def print_op(msg: str):
    """Print message"""
    print(msg)


@dsl.pipeline(name="ExitHandler example", description="Shows how to use ExitHandler")
def pipeline():
    exit_task = print_op("Exit!")
    with dsl.ExitHandler(exit_task.output):
        add_task = add_op(1.2, 2.4)
        print_op(f"Result: {add_task.output}")


if __name__ == "__main__":
    # Compile the pipeline
    kfp.compiler.Compiler.compile(pipeline, "pipeline.yaml")
