# Common utilities available to every service / model.

python_sources(
    name="src",
    # Everything under src/{{cookiecutter.project_slug}}/utils/** is bundled here.
)

python_tests(
    name="tests",
    dependencies=[":src"],
)

# (Optional) Build a wheel so other repos can consume this package.
python_distribution(
    name="dist",
    dependencies=[":src"],
    provides=setup_py(
        name="{{cookiecutter.namespace}}.utils",
        version="0.1.0",
        description="Shared utility functions for {{cookiecutter.project_name}}.",
    ),
)
