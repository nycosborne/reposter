
# Reposter

A service for posting content across multiple platforms

## Authors

- [@nycosborne](https://www.github.com/nycosborne)


## Tests Status

![example workflow](https://github.com/nycosborne/reposter/actions/workflows/checks.yml/badge.svg)



## React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

# Deployment


## Server Setup

### Creating an SSH Deploy Key

To create a new SSH key which can be used as the deploy key, run the command below:

```sh
ssh-keygen -t ed25519 -b 4096
```

Note: This will create a new `ed25519` key, which is the recommended key for GitHub.

To display the public key, run:

```sh
cat ~/.ssh/id_ed25519.pub
```

Then configer the public key in the GitHub repository settings.
### Install and Configure Depdencies

Use the below commands to configure the EC2 virtual machine running Amazon Linux 2.

Install Git:

```sh
sudo yum install git -y
```

Install Docker, make it auto start and give `ec2-user` permissions to use it:

```sh
sudo amazon-linux-extras install docker -y
sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo usermod -aG docker ec2-user
```

Note: After running the above, you need to logout by typing `exit` and re-connect to the server in order for the permissions to come into effect.

Install Docker Compose:

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```


## Running Docker Service


### Cloning Code

Use Git to clone your project:

```sh
git clone <project ssh url>
```

Note: Ensure you create an `.env` file before starting the service.


### Running Service

To start the service, run:

```sh
docker-compose -f docker-compose-deploy.yml up -d
```

### Stopping Service

To stop the service, run:

```sh
docker-compose -f docker-compose-deploy.yml down
```

To stop service and **remove all data**, run:

```sh
docker-compose -f docker-compose-deploy.yml down --volumes
```


### Viewing Logs

To view container logs, run:

```sh
docker-compose -f docker-compose-deploy.yml logs
```

Add the `-f` to the end of the command to follow the log output as they come in.


### Updating App

If you push new versions, pull new changes to the server by running the following command:

```
git pull origin
```

Then, re-build the `app` image so it includes the latest code by running:

```sh
docker-compose -f docker-compose-deploy.yml build app
```

To apply the update, run:

```sh
docker-compose -f docker-compose-deploy.yml up --no-deps -d app
```

The `--no-deps -d` ensures that the dependant services (such as `proxy`) do not restart.


## Tests

![example workflow](https://github.com/nycosborne/reposter/actions/workflows/checks.yml/badge.svg)

To run tests from the docker container, use the following commands:
```shell
docker-compose run --rm app sh -c "python manage.py test"
```
```shell
docker-compose run --rm app sh -c "flake8"
```
```shell
docker-compose run --rm node-frontend sh -c "npm run lint"
```
