import kfp
from kfp import dsl
from kfp.components import func_to_container_op


@func_to_container_op
def flip_coin_op() -> str:
    """Flip a coin"""
    import random

    result = random.choice(["heads", "tails"])
    return result


@func_to_container_op
def print_op(msg: str):
    """Print message"""
    print(msg)


@dsl.pipeline(name="Flip coin", description="Shows hot to use dsl.Condition()")
def pipeline():
    flip_task = flip_coin_op()
    with dsl.Condition(flip_task.output == "heads"):
        # Will be executed in the case flip_task.output is 'heads'.
        print_op("You got heads!!")
    with dsl.Condition(flip_task.output == "tails"):
        # Will be executed in the case flip_task.output is 'tails'.
        print_op("You got tails!!")


if __name__ == "__main__":
    # Compiling the pipeline
    kfp.compiler.Compiler.compile(pipeline, "pipeline.yaml")
