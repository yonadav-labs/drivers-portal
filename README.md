# stable

### Prerequisites

On Linux: [docker][0] and [docker-compose][1].

On Mac: [docker][2] (`docker-compose` is included).

### Installing

    git clone git@github.com:commite/stable.git

### Running

    cd stable
    docker-compose up -d
    
### Load Data
    ./manage.py manual_import_task -t vehicles
    ./manage.py manual_import_task -t insurances
    ./manage.py manual_import_task -t fhv_drivers
    ./manage.py load_base_types
    
### Stopping

    cd django-docker
    docker-compose down

### Can I ssh into the containers?

Sort of. To enter the Django container to run `manage.py` (or any other command)
we have to create a shell instance:

    docker-compose exec web sh

This will start a shell (`sh`) in the Django container (`web`). The different
containers are specified in the `docker-compose.yaml` file.

**Note**: All the files generated inside a container (the ones from `manage.py
startapp`, `manage.py makemigrations`...) will be owned by `root` in the host
machine. To be able to modify them you can run:

    sudo chown -R $USER:$USER backend

Alternative
```
USER_ID=$(stat -c "%u:%g" .) docker-compose run --rm alpine sh
```

## How to configure

- The base Django project lives in `backend/stable`
- The manage file is `backend/manage.py`
- The main settings file is `backend/stableins/settings/common.py`

### Environment variables

The idea is to be able to configure the project using environment variables.
This allows a more modular aproach. These variables can be set both in the host
machine or in the `.env` file.

It's recommended to set the variables in the host machine for **staging and
production** environments, so they aren't in the source code. For development,
using the `.env` file is ok to quickly test things.

These are the variables used:

| Variable | Default | What | Example |
| -------- | ------- | ---- | ------- |
| `ALLOWED_HOSTS` | | A colon separated list with the allowed hosts | `localhost:mywebsite.local` |
| `ENV` | `dev` | The current environment. When `dev`, Django `DEBUG` will be true | `dev`, `staging`, `prod`... |
| `DJANGO_SECRET_KEY` | | The secret key for Django... | |
| `DATABASE_USER` | `django` | User to connect to postgres | |
| `DATABASE_PASS` | `django` | Password to connect to postgres | |
| `DATABASE_HOST` | `django` | Host to connect to postgres | |
| `DATABASE_NAME` | `django` | Name to connect to postgres | |


[0]: https://docs.docker.com/install/
[1]: https://docs.docker.com/compose/install/
[2]: https://docs.docker.com/docker-for-mac/install/
