python_sources()

python_tests(
    dependencies=[
        "//packages/shared-utils",
    ]
)

pex_binary(
    name="main",
    entry_point="{{cookiecutter.namespace}}.main.cli:main",
)

docker_image(
    name="service",
    dependencies=[":main"],
)
