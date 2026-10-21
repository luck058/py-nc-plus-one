# Setup instructions for linux
## One time setup
- Clone the repository
    - Navigate to the directory you want the project to live in
        - `cd path/to/parent/directory`
            - Replace `path/to/parent/directory` with the directory you want the project to live in
    - Clone the repository
        - `git clone https://github.com/luck058/py-nc-plus-one.git`
    - Navigate into the project directory
        - `cd py-nc-plus-one`
- Create .env from the .env.example template
    - Copy .env.example as .env
        - Run `cp .env.example .env` from the root of the project
    - Open .env and fill in the missing values. Already filled values are sensible defaults, but can be changes
- Create a .venv and install dependancies
    - `python -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install -r requirements.txt`

## On every startup
- Navigate to the project directory
    - `cd path/to/parent/directory/py-nc-plus-one`
        - Replace `path/to/parent/directory` with the directory you want the project to live in
- Enter the venv
    - `source .venv/bin/activate`