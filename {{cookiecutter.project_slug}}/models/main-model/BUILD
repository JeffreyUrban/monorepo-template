# (if ml_framework != "none")
python_sources(resolve="data-science")

python_tests(
    resolve="data-science",
    dependencies=[
        "//packages/shared-utils",
    ]
)

pex_binary(
    name="train",
    entry_point="{{cookiecutter.namespace}}.models.main.train:main",
    resolve="data-science",
)

pex_binary(
    name="serve",
    entry_point="{{cookiecutter.namespace}}.models.main.inference:serve",
    resolve="python-default",
)

docker_image(
    name="training",
    dependencies=[":train"],
    source="Dockerfile.training",
)

docker_image(
    name="serving",
    dependencies=[":serve"],
    source="Dockerfile.serving",
)
