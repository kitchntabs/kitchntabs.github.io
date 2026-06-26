# CI Toolchain 

### Notes: 
- CodePipeline and CodeBuild projects are configured manually through AWS Console. 
- The process to create the Toolchain in AWS is described in this document

## AWS CodePipeline

1. AWS CodePipeline - Source Stage - Bitbucket
    When a push is release into staging or master branches, CodePipeline clones the bitbucket source projects to be available in the build stage. 
2. Build Stage - CodeBuild (aws/build/build.yml)
   2.1 Read environment variables from different inputs 
            
            - AWS CodeBuild Project Environment variables, specific for the target build environment
            
                $ENVIRONMENT
                $SERVER_NAME
                $APP_URL
                $SOCKETS_APP_AUTH_HOST
            
            - AWS CodeBuild Spec File YML Variables
            
                $AWS_ACCOUNT_ID
                $AWS_REGION
                $PROJECT_NAME
                $VPCID
                $SUBNET1ID
                $SUBNET2ID
                $APP_PATH
                $REDIS_PREFIX
                $REDIS_PORT
                $REDIS_HOST
                $REDIS_PASSWORD
                $SOCKETS_APP_AUTH_ENDPOINT
                $SOCKETS_APP_DATABASE
                $SOCKETS_APP_PORT
                $SOCKETS_APP_PROTOCOL
                $SOCKETS_APP_CORS_ORIGIN
                $SOCKETS_APP_SSL_CERT
                $SOCKETS_APP_SSL_KEY
                $SOCKETS_APP_SSL_CHAIN
                $SOCKETS_APP_SSL_PHRASE
                $SOCKETS_APP_DEVMODE
            
            - AWS Secrets Manager
            
                $DOCKER_HUB_USER
                $DOCKER_HUB_PASS
                $AWS_KEY
                $AWS_SECRET
                $GOOGLE_MAPS_API_KEY
                $WELIVERY_TOKEN
                $RECAPTCHA_SITE_KEY
                $RECAPTCHA_SECRET_KEY

    2.2 Build the docker image (docker.build.$ENVIRONMENT.sh)
        2.2.1 Login into DockerHub (A docker hub account is required to avoid the limit of daily docker pull commands, even if they are to an ECR repository)
        2.2.2 Login into ECR (Elastic Container Repository), where the built images are stored.
        2.2.3 Reads and validate for the required environment variables to build a docker image
        2.2.4 Replaces template variables for several application env files, accordingly the build envs. 
        2.2.5 Build the image (docker build)
        2.2.6 Tag de image with the Code Build Number and latest, ans pushes it to the respective ECR Repository
        2.2.7 Upload config and env files to S3; In some cases a configuration env file, formatted in the build process, is uploaded to S3, so the CloudFormation script can use it as input for docker environment variables. 
        2.2.8 AWS Systems Manager Parameter Store is used to persist shared build parameters, so they can be used in later project build stages. 

3. Deploy Stage  (aws/build/deploy.yml)
    3.1 Read environment variables from different inputs 
        - AWS CodeBuild Project Environment variables, specific for the target build environment: none
        - AWS CodeBuild Spec File YML Variables
            $VPCID
            $SUBNET1ID
            $SUBNET2ID
        - AWS Secrets Manager
            $SSLCertificateARN: "arn:aws:secretsmanager:us-east-1:823156438814:secret:dash/build-yKeyjc:SSLCertificateARN"

    3.2 Reads the SSM Parameter store variables required in the pre_build stage
    3.3 Replaces ./aws/stack.$ENVIRONMENT.yml cloudformation variables accordingly
    3.4 For backup reasons we store the computed update stack command ./update-stack-command.txt and upload it to an AWS S3 Bucket.
    3.5 the AWS CloudFormation Update Stack is performed (aws cloudformation update-stack)

        
