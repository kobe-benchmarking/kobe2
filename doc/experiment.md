# Experiment Specification

An _experiment_ compares the results from several _runs_ where each
run comprises multiple _steps_ executed consecutively. An experiment
is specified by a set of YAML files, where each file specifies a run.

The structure of the YAML file is the following:

```
metadata:
   parent_id: str
   id: str
   version: str
   name: str
   description: str


implementation:
   module: path.to.module
   |
   service: url
   |
   container: url


steps:
  - id: str
    type: prepare | work
    parameters:
       any YAML fragment
    data:
       loader: path.to.module
       location: url
       parameters:
          any YAML fragment
    metrics:
       list of metrics   
```

## Metadata

The `id` is any string that is unique for this run. The `parent_id`
is any string that is unique for the experiment that this run is
part of. At this stage, it is not possible to make experiments by
combining pre-existing runs, but we are considering including
importing and templating at a later stage.

The `version` is any string that has the property that the
lexicographically last version should be considered the latest and be
used by default. Can be used to maintain record of minor changes that
do not need to be considered separate runs when compiling comparative
reports.

The `name` is a string meant to be used as column header or plot
annotation. It should be meaningful and short. It does not need to be
unique, although it makes sense that it is unique within each
experiment.

The `description` is a paragraph meant to be used to provide more
information in, e.g., a hover popup or similar "more info" elements.


## Implementation

The implementation of the method being benchmarked can be provided in
any of the following _mutually exclusive_ ways:

* Using the `module` field to provide a string that is appropriate argument for Python's `importlib.import_module` method.

* Using the `service` field to provide the URL to an independently provisioned system.

* Using the `container` field to provide the URL to a Docker image that should be used by KOBE to deploy a Docker container.


## Steps

The benchmarking steps. Each run may (but does not need to) start with
a step of type `prepare`, followed by one or more steps of type `work`.
The KOBE Orchestrator will invoke the `prepare()` or `work()` method of
the wrapper/connector of the benchmarked system.

The `data` field has the following subfields:
`loader` is a string that is appropriate argument for Python's
`importlib.import_module` method, `location` is the path to the data,
and `parameters` is the parameters (besides the location) that will be
passed to initialze the loader. More on `parameters` below.

The `metrics` field has a list of keywords, each one indicating a
different benchmarking metric. The available metrics are implemented
in the KOBE codebase and cannot be extended by the user, but we are
considering including a plugin mechanism at a later stage.
Each step produces its own set of benchmarking metrics that are
reported individually. This can be used to, for example, compare
results from the same system on different parameterizations or
different testing workloads.

Besides the required method parameters (data and metrics), the
Orchestrator will also pass the `parameters` field to the
the wrapper/connector.

The `parameters` fields of both `steps` and `data` are parsed into
a Python dict/JSON string and passed to the wrapper/connector
(respectively). They are meant to be any parameters specific to the
implementation being benchmarked or the data loader being used.
It is user's responsibility to pass meaninful parameters and the
wrapper's/connector's responsibility to translate them into the
syntax expected by the benchmarked system. It is also the user's
responsibility to _not_ use any idiomatic YAML expresions that cannot
be serialized as JSON.
