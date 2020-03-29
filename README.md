# ASTRA SMT

>## Subsystem management and tracking software

This software was created by members of the University of Alabama in Huntsville's Space Hardware Club (Project ASTRA) for the purposes of tracking tasks and personnel associated with the University Rover Challenge. 
Please feel free to contact us with any questions or feedback.

### Installation

Start by installing the required dependencies:

```bash
    pip3 install -r requirements.txt
```

This project does not include a database when cloned from the repo.
You must initialize a new one with:

```bash
    python3 manage.py makemigrations smt
    python3 manage.py migrate
```

Once that has completed, you can start the server with:

```bash
    python3 manage.py runserver 0.0.0.0:5000
```

### Usage

When contributing to this project, having access to the admin console is extremely helpful. You can create a login for yourself with:

```bash
    python3 manage.py createsuperuser
```

When the server is running you can use this login on [this page](http://localhost:5000/admin).

>More coming soon

### Tests

>Coming soon
