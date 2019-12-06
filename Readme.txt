In order to run my code, you will need to do the following:
1) Create a user with full access to EC2, SQS, S3 and IAM
2) Use the users credential and configure them using AWS configure. Also specify the region us-east-1.
3) Create a role called 'instance-role', with the same permissions as the user.
4) Create a key pair called 'key-pair' and security group which allows all inbound traffic via TCP, then hard code it into the create_instances function.
5) For purging the queue you will need to hardcode the queue URLS.
6) Run the cloud.py file which takes 2 arguments: the difficulty level and number of instances to spawn.
