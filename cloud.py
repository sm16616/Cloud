import boto3
import json
import sys
import signal

def terminate():
	print("\nPurging queues")

	sqs.purge_queue(
	    QueueUrl='https://sqs.us-east-1.amazonaws.com/422003104180/InputQ'
	)
	sqs.purge_queue(
	    QueueUrl='https://sqs.us-east-1.amazonaws.com/422003104180/OutputQ'
	)

	print("Queues purged")

	print("Terminating instances")

	instanceids = []
	instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	for instance in instances:
		instanceids.append(instance.id)
		print("Shutting down")

	ectwo.terminate_instances(InstanceIds=instanceids)

	print("Instances terminated")

def keyboardInterruptHandler(signal, frame):
	terminate()
	exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)


s3 = boto3.client('s3')
bucket = s3.create_bucket(Bucket='mys3cloudbucket')
s3.upload_file('CND.py', 'mys3cloudbucket', 'CND.py')

# D = input("What difficulty level would you like to use for nonce discovery?\n")
# N = input("How many instances would you like to spawn?\n")
D = sys.argv[1]
N = sys.argv[2]

ec2 = boto3.resource('ec2')
ectwo = boto3.client('ec2')

with open("shellscript.sh", "r") as myFile:
	Userdata = myFile.read()

instances = ec2.create_instances(
	ImageId='ami-00068cd7555f543d5',
	MinCount=1,
	MaxCount=int(N),
	KeyName="key-pair",
	IamInstanceProfile={
        'Name': 'instance-role'
    },
	UserData= Userdata,
	SecurityGroupIds = ['sg-5bca8b0e'],
	InstanceType="t2.micro"
)

sqs = boto3.client('sqs')
InputQ = sqs.create_queue(QueueName='InputQ')
queue_url = InputQ['QueueUrl']

for i in range(0,int(N)):
	dict_queue = dict(
		Diffculty_level = int(D),
		num_instances = int(N),
		instance_id = i+1
	)
	dict_queue = json.dumps(dict_queue)
	sqs.send_message(QueueUrl=queue_url, MessageBody=dict_queue)



OutputQ = sqs.get_queue_url(QueueName='OutputQ')
queuee_url = OutputQ['QueueUrl']

messages = []
while len(messages) != int(N):
	message = sqs.receive_message(
		QueueUrl=queuee_url,
		MaxNumberOfMessages=10
	)
	try:
		for msg in message['Messages']:
			result_queue = msg['Body']
			result_queue = json.loads(result_queue)
			sqs.delete_message(
				QueueUrl=queuee_url,
				ReceiptHandle=msg['ReceiptHandle']
			)
			messages.append(result_queue)
			# print(result_queue)
	except KeyError as e:
		pass

shortest_time = sys.maxsize
for each in messages:
	 result = each['timeresult']
	 hash = each['hashresult']
	 nonce = each['nonceresult']
	 result = float(result)
	 if result < shortest_time:
		 shortest_time = result
		 shortest_hash = hash
		 shortest_nonce = nonce

print("done in: ", shortest_time, "for difficulty", int(D))
print(shortest_hash)
print(shortest_nonce)

f = open( 'output.txt', 'a' )
f.write( "Time: " + str(shortest_time) + " Instances: :" + str(N) + " Difficulty: " + str(D) + " Nonce: " + str(shortest_nonce) + "\n")
f.close()

terminate()



# print("done in: ", shortest_time, "for difficulty", int(D))
# print(messages[0]['hashresult'])
# print(messages[0]['nonceresult'])


# s3.download_file('mys3cloudbucket', 'output.txt', 'output.txt')
# f = open('output.txt','r')
# message = f.read()
# print(message)
# f.close()
