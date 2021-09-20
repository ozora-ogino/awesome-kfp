# [WIP] Awesome KubeFlow Pipeline [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)
A collection of awesome examples and tips regarding KubeFlow Pipeline.

## Examples
 - [v1](/examples/v1)
	- [func_to_container_op](/examples/v1/func_to_container_op)
	<!-- - [ContainerOp](/examples/v1/container_op) -->
	- [ResourceOp](/examples/v1/resource_op)
	<!-- - [VolumeOp](/examples/v1/volume_op) -->
	- [Condition](/examples/v1/condition)
	- [ExitHandler](/examples/v1/exithandler)
	- [ParallelFor](/examples/v1/parallel_for)


## Tips
 - [func_to_container_op](#func_to_container_op)
 - [Condition](#condition)
 - [ExitHandler](#exithandler)
 - [ParallelFor](#parallelfor)
 - [Caching](#caching)

### [func_to_container_op](https://kubeflow-pipelines.readthedocs.io/en/latest/source/kfp.components.html#kfp.components.func_to_container_op)

#### Use additional package

You can specify additional packages as `package_to_install`. This enables to use additional packages without building new docker image.

#### [Example](/examples/v1/func_to_container_op/simple.py)
```python
slack_post_op = func_to_container_op(slack_post, packages_to_install=["slack_sdk"])
```

### [Condition](https://kubeflow-pipelines.readthedocs.io/en/latest/source/kfp.dsl.html#kfp.dsl.Condition)

You can use `dsl.Condition` like an if statement in a pipeline function.

#### [Example](/examples/v1/condition/flip_coint.py)

```python
with dsl.Condition(flip_task.output == "heads"):
	# Will be executed in the case flip_task.output is 'heads'.
	print_op("You got heads!!")
```


### [ExitHandler](https://kubeflow-pipelines.readthedocs.io/en/latest/source/kfp.dsl.html#kfp.dsl.ExitHandler)

ExitHandler will be executed whether the pipeline succeeds or fails.

#### Example

```python
exit_op = ContainerOp(...)
with ExitHandler(exit_op):
	op1 = ContainerOp(...)
	op2 = ContainerOp(...)
```

Note: ExitHandler requires ContainerOp as a argument, not ResourceOp or something else.
If you want to create/delete/apply k8s resources with ExitHandler, please see [this example](/example/v1/resource_op/delete_resource_with_exithandler.py).

### [ParallelFor](https://kubeflow-pipelines.readthedocs.io/en/latest/source/kfp.dsl.html#kfp.dsl.ParallelFor)

ParallelFor represents a parallel for loop over a static set of items.

#### Example:

Simple literal example.
In this case op1 would be executed twice, once with case `args=['echo 1']` and once with case `args=['echo 2']`

```python
with dsl.ParallelFor([{'apple': 2, 'banana': 4}, {'apple': 3, 'banana': 20}]) as item:
	op1 = ContainerOp(..., args=['echo apple:{}'.format(item.apple)])
	op2 = ContainerOp(..., args=['echo banana:{}'.format(item.banana])
```

#### [Example2]((/examples/v1/parallel_for/parallel.py))

In this example, the previous task's output will be used for loop arguments.

```python
list_task = list_generator_op(parallelism)
parallel_tasks = dsl.ParallelFor(list_task.output)
with parallel_tasks as msg:
	print_op(msg)
```

#### Set the number of parallel tasks

You can set the number of prallel tasks inside of the pipeline function.

```python
def pipeline(parallelism: int):
    # set the number of parallel
    default_conf = kfp.dsl.get_pipeline_conf()
    default_conf.set_parallelism(2)
```

Please refer [official document](https://kubeflow-pipelines.readthedocs.io/en/latest/source/kfp.dsl.html#kfp.dsl.PipelineConf.set_parallelism) or [our example](/examples/v1/parallel_for/parallel.py).


### Caching
I recommend to read KubeFlow official documents about caching.
 - [Caching v1](https://www.kubeflow.org/docs/components/pipelines/caching/#disablingenabling-caching)
 - [Cacing v2](https://www.kubeflow.org/docs/components/pipelines/caching-v2/)

#### Disabling/Enabling Caching in the namespace

For disabling:

```bash
# Make sure mutatingwebhookconfiguration exists in your cluster
export NAMESPACE=<Namespace where KFP is installed>
kubectl get mutatingwebhookconfiguration cache-webhook-${NAMESPACE}

kubectl patch mutatingwebhookconfiguration cache-webhook-${NAMESPACE} --type='json' -p='[{"op":"replace", "path": "/webhooks/0/rules/0/operations/0", "value": "DELETE"}]'
```

For enabling:

```bash
kubectl patch mutatingwebhookconfiguration cache-webhook-${NAMESPACE} --type='json' -p='[{"op":"replace", "path": "/webhooks/0/rules/0/operations/0", "value": "CREATE"}]'
```

#### Managing caching staleness
 To control the maximum staleness of the reused cached data, you can set the step’s `max_cache_staleness` parameter which is in [RFC3339 Duration](https://www.ietf.org/rfc/rfc3339.txt) format (so 10 days = "P30D").

For disabling cache of ContainerOP:

```python
task = dsl.ContainerOp(...)
task.execution_options.caching_strategy.max_cache_staleness = "P30D"
```

Because ResourceOp doesn't have `execution_options` parameter, you can use`add_pod_annotation` instead:

```python
rop = dsl.ResourceOp(...)
rop.add_pod_annotation("pipelines.kubeflow.org/max_cache_staleness", "P0D")
```

If you're using KubeFlow Pipeline SDK v2, you can use `enable_caching` for both of ContainerOp and ResourceOp:
```python
task = dsl.ContainerOp(...)
task.set_caching_options(False)

rop = dsl.ResourceOp(...)
rop.set_caching_options(False)
```

See [our example](/examples/v1/commons/caching.py) for more information.

## Contributing

Interested in contributing? Awesome😎

Fork and run `make init` to setup.

Then create PR and let us review!

See the Google's best practices which we follow in this repository.
 - [The CL author’s guide to getting through code review](https://google.github.io/eng-practices/review/developer/)
 - [Python Style Guide](https://google.github.io/styleguide/pyguide.html)