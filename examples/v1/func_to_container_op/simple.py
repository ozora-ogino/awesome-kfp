import kfp
from kfp import dsl
from kfp.components import func_to_container_op


@func_to_container_op
def add_op(a: float, b: float) -> float:
    """Calculates sum of two arguments"""
    return a + b


def slack_post(msg: str, channel: str = "#random") -> float:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    client = WebClient(token="YOUR_TOKEN")
    try:
        response = client.chat_postMessage(channel=channel, text=msg)
        assert response["message"]["text"] == "Hello world!"

    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


# `packages_to_install` helps to install additional packages.
slack_post_op = func_to_container_op(slack_post, packages_to_install=["slack_sdk"])


@dsl.pipeline(name="sample pipeline", description="Shows how to use func_to_container_op")
def pipeline():
    add_task = add_op(1.2, 2.4)
    slack_post_op(f"Result: {add_task.output}")


if __name__ == "__main__":
    # Compile the pipeline
    kfp.compiler.Compiler.compile(pipeline, "pipeline.yaml")
