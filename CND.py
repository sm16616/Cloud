import hashlib
import threading
import time
import multiprocessing
import boto3
import json
import sys
# import logging
# logging.basicConfig(filename="log.log",level=logging.DEBUG)


sqs = boto3.client('sqs', region_name='us-east-1')
InputQ = sqs.get_queue_url(QueueName='InputQ')
queue_url = InputQ['QueueUrl']


messages = sqs.receive_message(
	QueueUrl=queue_url,
 	MaxNumberOfMessages=1
)

received = 0
while not received:
    for msg in messages['Messages']:
        dict_queue = msg['Body']
        dict_queue = json.loads(dict_queue)
        print(dict_queue)
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg['ReceiptHandle']
        )
    received = 1

x = dict_queue['Diffculty_level']

datablock = 'COMSM0010cloud'
step = dict_queue['num_instances']


def noncediscovery(nonce, datablock2):
    runtime = time.time()
    found = 0
    while found == 0:
        blockAndNonce = datablock2 + str(nonce)
        hash = hashlib.sha256(blockAndNonce.encode('utf-8')).hexdigest()
        second_hash = hashlib.sha256(hash.encode('utf-8')).hexdigest()
        hashBinary = bin(int(second_hash, 16)) [2:].zfill(256)
        if hashBinary[:x] == '0'*x:
            found = 1
            break
        nonce += step

    complete_time = str(time.time() - runtime)
    dict_result_queue = dict(
		timeresult = complete_time,
		hashresult = second_hash,
		nonceresult = nonce
	)
    return dict_result_queue

dict_result_queue = noncediscovery(dict_queue['instance_id'], datablock)

OutputQ = sqs.create_queue(QueueName='OutputQ')
queuee_url = OutputQ['QueueUrl']
dict_result_queue = json.dumps(dict_result_queue)
sqs.send_message(QueueUrl=queuee_url, MessageBody=dict_result_queue)



#
# FOR LOCAL
#



# nonce_array = []
# #
# for i in range(0,int(N)):
#     nonce_array.append(i)
#
# x = 26
# step = int(N)
#
# def noncediscovery(nonce, datablock2):
#     runtime = time.time()
#     found = 0
#     while found == 0:
#         blockAndNonce = datablock2 + str(nonce)
#         hash = hashlib.sha256(blockAndNonce.encode('utf-8')).hexdigest()
#         second_hash = hashlib.sha256(hash.encode('utf-8')).hexdigest()
#         hashBinary = bin(int(second_hash, 16)) [2:].zfill(256)
#         if hashBinary[:x] == '0'*x:
#             found = 1
#             break
#         nonce += step
#
#
#     print("done in: " + str(time.time() - runtime) + "for difficulty: " + str(x) + " for process: " + str(step) + " for nonce: " + str(nonce) )
    # print(hash)
    # print(hashBinary)
    # print(nonce)

# noncediscovery(step, datablock)
#
# if __name__ == '__main__':
#     processes = []
#     for i in range(0, (len(nonce_array))):
#         p = multiprocessing.Process(target=noncediscovery, args=(nonce_array[i], datablock))
#         processes.append(p)
#         p.start()
#
#     for process in processes:
#         process.join()


# thread_list = []
# for i in range(0, (len(nonce_array))):
#     t=threading.Thread(target=noncediscovery, args=(nonce_array[i], nonce_array[i]+add, datablock))
#     thread_list.append(t)
#
# for thread in thread_list:
#     thread.start()
#
# for thread in thread_list:
#     thread.join()
