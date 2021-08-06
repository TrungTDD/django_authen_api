
# BUILD TUTORIAL

## Required tools  
Before run application, make sure you has installed virtualenv in your environment. If not, please type into below command to install virtualenv:  `pip install virtualenv`

## Build steps
1. Setup environment and install inpendencies
* In application folder, create an environment: `virtualenv venv`
* Make virtualenv run: source venv/bin/activate
* Locate into folder containing file requirements, typing into this command: pip install -r requirement

2. Build and run the application
* Locate into the foot folder containing file `manage.py`, running below command to migrate data:
		`python manage.py migrate`
* After successfully migrate data, typing into below command to run the server
		`python manage.py runserver`

## Pre-commit source

For making source more cleaner, we must setup some configurations before commit source.

Install these package below:
` pip install black flake8 isort pre-commit`

Create file `.pre-commit-config.yaml" with content blow:

<pre><code>
repos:
-   repo: https://github.com/ambv/black
    rev: 20.8b1
    hooks:
    - id: black
-   repo: https://gitlab.com/pycqa/flake8
    rev: 3.8.4
    hooks:
    - id: flake8
-   repo: https://github.com/timothycrosley/isort
    rev: 5.7.0
    hooks:
    -   id: isort
<code><pre>

Create `.flake8` for customize flake8

<pre><code>
[flake8]
ignore = E203, E266, E501, W503, F403, F401
max-line-length = 120
max-complexity = 18
select = B,C,E,F,W,T4,B9
<code><pre>

Running the below command:
`pre-commit install`





