# Guide for Developers

## Getting Started

`censusdis` welcomes contributions from the community. 
If you would like to contribute, we recommend you start
by opening a new 
[issue](https://github.com/vengroff/censusdis/issues)
in our GitHub repository. That way you can get advice, 
guidance, and potential collaboration from others before 
you start. If you would like to contribute but aren't
sure how, you can browse the issues and look for
ones labeled with the tag 
[good first issue](https://github.com/vengroff/censusdis/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

If you find a bug in `censusdis`, we also encourage
you to submit an [issue](https://github.com/vengroff/censusdis/issues),
ideally with a reproducible test case, even if you
are not sure how to fix the bug.

## Fork and Pull Request

We encourage contributors to fork our GitHub repository,
do their development work locally, and then submit a 
pull request back to the main repository. One of the 
maintainers will then review and approve the contribution.

If you are not familiar with the fork and pull request
workflow, here is a 
[guide](https://gist.github.com/Chaser324/ce0505fbed06b947d962)
to starting out.

## Development with Poetry

We use [poetry](https://python-poetry.org/) to manage the dependencies
in `censusdis`. Many modern IDEs will recognize a 
poetry project and download the dependencies necessary
for development. If yours does not, or you want to 
download dependencies manually, simply
[install poetry](https://python-poetry.org/docs/#installation)
and then use
```shell
poetry install
```
to install all the necessary dependencies for your project.

Next, you can use
```shell
poetry shell
```
to start a shell in a virtual environment with all 
the dependencies. From this shell you can run
a python interpreter with the `censusdis` source
code and all the necessary external dependencies.

If you need to
add a dependency to do you work, which shoud be 
rare, please consult the 
[poetry documentation](https://python-poetry.org/docs/)
for
how to use `poetry add`, `poetry lock` and `poetry update`.

## Census License

If you are going to be doing development on `censusdis`
you could very well exceed the limits on queries from
the U.S. Census servers that can be 

## Testing

We pride ourselves on the quality and coverage of our
unit tests. Most submissions, especially those that
add new features, change behavior, or fix bugs, should
also include new or updated tests.

All of the tests are in the `tests` directory in the
repository. All of these tests will be run on your
branch as soon as you submit a pull request, so it is
a good idea to run them all before you submit the
pull request. You can do this from your IDE, usually
by right clicking on the test directory and choosing
to run the tests in contains.

Alternatively, you can run them from the command line
inside your poetry shell using 

```shell
 poetry run python -m pytest
```

(note that if you are already in a shell started with
`poetry shell` you do not need the `poetry run` part.)

If you would like to see if the new code you wrote is
covered by tests, you can generate a full test coverage
report with

```shell
poetry run coverage run -m pytest --junitxml=reports/junit/junit.xml
poetry run coverage html -d ./reports/coverage 
```

Now open `./reports/coverage/index.html` in a browser
and you should be able to see test coverage for the
entire project, including the code you have been
working on. If you want to see how it compares to
the main branch of the code, go back to the 
[censusdis Github page](https://github.com/vengroff/censusdis) 
and click the code coverage
icon at the top of the README.md file.

## Flake8 and Black

Before you commit your code, we recommend you run
[flake8](https://flake8.pycqa.org/en/latest/)
and 
[black](https://black.readthedocs.io/en/stable/)
as follows:

```shell
poetry run flake8 .
poetry run black .
```

and correct any errors that are found. If you submit
a pull request with errors, the GitHub action we have
set up to lint the code will fail and it will not be
possible to merge your pull request. Please do not
add `# noqa` comments to the code unless they are 
absolutely necessary, e.g. because you stumbled upon
one of the rare cases where `flake8` and `black`
disagree.

## Maintaining `datasets.py`

Over time, the U.S. Census adds new data sets. While
`censusdis` can access any of them as they are added,
it can be convenient to be able to access them with 
symbolic names like `ACS5`. We maintain there is the 
file `datasets.py` using a utility called `symbolic.py`.

You can be a good citizen by running

```shell
 poetry run python utils/symbolic.py datasets.py
```

from the root directory of your clone of the repository
and commiting any resulting changes before you submit
a pull request. The changes are likely unrelated to what
you are doing, but will catch any late-breaking new 
data sets the U.S. Census has published.