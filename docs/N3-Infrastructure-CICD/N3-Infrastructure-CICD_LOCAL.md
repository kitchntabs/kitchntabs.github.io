
# LOCAL DEVELOPMENT ENVIRONMENT

# Windows setup: use wsl.

wsl --list --online
wsl --install -d Ubuntu
set a user and password

wsl -d Ubuntu
sudo apt install openssl
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt install docker-ce -y
sudo usermod -aG docker $USER  # Add your user to the docker group
sudo apt install curl git 
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
node --version
npm --version
sudo npm install --global yarn

## Fresh setup

- cd dash-backend
- wsl -d Ubuntu (in windows)

- yarn install
- yarn new

- Enter the new app name: e.g: myapp
- Do you want to set up this app as a Git submodule? (y/n)
- Select y, yes if you will version your domain code in a separated client repository
- Do you have a remote Git repository URL? (y/n) n
- Select n, if you don't have your git repo url yet

### Output

Successfully created new app as a submodule at domain

Instructions for clients:
=======================
1. Clone the repository with: git clone --recurse-submodules [main-repo-url]
2. To work on their app:
   cd domain # e.g, ./dash-backend/domain
   # Make changes
   git add .
   git commit -m "Your commit message"
   git push

3. To pull updates from the main repository:
   cd [main-repo-root] # e.g, ./dash-backend
   git pull
   git submodule update --remote

The command copies the demo example_domain included in the project, to the  ./domain folder and initializes a git repository to track your changes in the domain folder separatedly from the main dash-backend repository. 

Note: The dash-backend is readable, can only push to the domain submodule, not to the dash-backend repository
For collaboration, fork the dash-backend repo, and create pull-requests for revisions. 

# SETUP THE LOCAL ENVIRONMENT
# REQUIREMENTS

- Docker
- brew
- Sail (brew install sail)

# INSTRUCTIONS

- Install composer packages
  This command sets up a PHP 8.2 environment within Docker and installs Laravel dependencies

```sh
docker run --rm -u "$(id -u):$(id -g)" -v "$(pwd):/var/www/dash -w /var/www/dash laravelsail/php82-composer:latest composer install --ignore-platform-reqs
```

- Copy environment variables

```sh
cp .env.example .env.local
# replace the env vars. e.g:
# The important vars to replace at this stage are:
# SYSTEM_ADMIN_PASSWORD=
# (optional) DB_DATABASE=
# Save the file and continue with the rest of the steps.
```

- Set database name

```sh
sed -i '' 's/DB_DATABASE=boilerplate/DB_DATABASE=dashpanel/' .env
```

- Set Superadmin password

```sh
sed -i '' 's/SYSTEM_ADMIN_PASSWORD=/SYSTEM_ADMIN_PASSWORD=dash.pan.2025...!/' .env
```

- Configure alias for sail commands (You can see how to configure an alias [here](https://laravel.com/docs/9.x/sail#configuring-a-shell-alias).)

```sh
alias sail='[ -f sail ] && sh sail || sh vendor/bin/sail'
#chmod +x localsail.sh
#alias sail='./localsail.sh'
```

- Note: export the alias to ~/.bashrc 
- Uses .env for local development
- Requires local.staging or local.production for docker build. reference BUILD.md

### Run Seed for first time run

```sh

cp .env.example .env


sail up -d
sail artisan key:generate
sail artisan migrate:fresh --seed
sail artisan db:sync_roles
```

## Start containers
- Open 3 terminals for development. one for the backend, one to the queue system with horizon/redis, one for reverb for socket messaging. 


```sh

sail up
sail artisan horizon
sail artisan reverb:start --debug
```

- backend should be online at http://localhost:8000
- when runing the horizon, reverb and the frontend you can go to  http://localhost:8000/ws and test a public message.

## Build Docker Image (Review)

```sh
sail build --no-cache
```

# Known Issues:

- The repository at "/var/www/dash" does not have the correct ownership and git refuses to use it:

```sh
git config --global --add safe.directory /var/www/dash
# this is a warning only, you can ignore it.
```

- TODO: The bootstrap/cache folder is missing from the base, remove it from gitignore, add the folder but exclude all its contents.

```sh
mkdir bootstrap/cache
# this is a warning only, you can ignore it.
```

# USEFUL COMMANDS FOR DEVELOPMENT

## Instal or update composer dependencies

- sail composer update

## CLI Connect to database

- psql -W -h localhost -p 54321 -d dashadmin -U sail

# DEVELOPMENT FIRST TIME NOTES:

sail up -d
sail artisan migrate:fresh --seed
sail composer dump-autoload
sail artisan key:generate
sail artisan clear-compiled
sail artisan optimize:clear


# Run some tests:

- tests will run on the testing database. make sure you have the .env.testing with the proper db credentials.
  sail artisan migrate:fresh --seed --env=testing
  sail artisan test --filter SystemAdminLoginTest --env=testing
  sail artisan test --filter TabsBasicFlowTest --env=testing

# Production tests:

sail artisan test --configuration=phpunit.local.xml

look for system default variables at .env to login using the endpoints
SYSTEM_ADMIN_EMAIL=
SYSTEM_ADMIN_PASSWORD=

# browse the api
http://localhost:8000

the application should be available at the port specified at .env
APP_PORT=8000

# list all the api endpoints

sail artisan route:list

e.g: http://localhost:8000

# mailhog

http://localhost:8025/


# initializing with custom env. this will mount .env.pinoywok as .env in the docker container
ENV_FILE=.env.pinoywok sail up
sail shell
# DEPRECATION NOTICES

Package biscolab/laravel-recaptcha is abandoned, you should avoid using it. No replacement was suggested.
Package box/spout is abandoned, you should avoid using it. No replacement was suggested.
Package daltcore/lara-pdf-merger is abandoned, you should avoid using it. No replacement was suggested

For biscolab/laravel-recaptcha, consider using:

anhskohbo/no-captcha for Google reCAPTCHA
Or the official google/recaptcha package
For box/spout, consider using:

openspout/openspout (the community-maintained fork of box/spout)
Or phpoffice/phpspreadsheet for Excel file handling
For daltcore/lara-pdf-merger, consider using:

iio/libmergepdf for PDF merging
Or barryvdh/laravel-dompdf for PDF generation in Laravel


sail artisan optimize:clear && sail artisan cache:clear && sail artisan config:clear && sail artisan route:clear && sail artisan view:clear