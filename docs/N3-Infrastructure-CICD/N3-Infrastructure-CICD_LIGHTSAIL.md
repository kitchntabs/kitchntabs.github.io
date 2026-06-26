
# MINIMAL COST PREVIEW ENV SETUP ON LIGHTSAIL.

A minimal preview setup that can be scaled in staging and production environments later. 

Backend main service requirements:

In a production environment, the docker containers should be created in at least 2 instances behind a load balancer.
Everything the instances processes must not reside on the fargate instances, therefore everything that generates an output, such as logs, files, etc, they need to be segregated. 
The database layer should be segregated from the application layer, running on independent rds instances. 
The asset storage should be segregated from the application layer, running on independent s3 buckets. 

- Postgres Database
- Redis Server
- Storage
- Mail Server
- Socket Server

For a minimal preview setup, even if we can implement all the components within a single EC2 instance, it is suggested to at least segregate the database and asset storage due persistance issues. If you update the docker image, to update changes, all data and system configurations will be lost.

Therefore the postgres database and the storage of assets such as user images will be segregated. 

./docker.build.sh --skip-push --env staging
brew install aws/tap/lightsailctl
#aws lightsail push-container-image --region us-west-2 --service-name dash-staging --label dash-staging --image dash-staging:latest

022648472487.dkr.ecr.us-east-1.amazonaws.com/pinoywok:latest

aws ecr get-login-password --region us-east-1 --profile pw | docker login --username AWS --password-stdin 022648472487.dkr.ecr.us-east-1.amazonaws.com
docker tag dash-staging:latest 022648472487.dkr.ecr.us-east-1.amazonaws.com/pinoywok:latest
docker push 022648472487.dkr.ecr.us-east-1.amazonaws.com/pinoywok:latest

