import redis
import json
import datetime
host = '127.0.0.1'
port = 6379

pool = redis.ConnectionPool(host=host, port=port)

r = redis.StrictRedis(connection_pool=pool)


def insertIntoDb(hashValue, dictionary):
    time = str(datetime.datetime.now())
    dictionary.update({"createTime": time})
    print("file dictionary is ", dictionary)
    data = json.dumps(dictionary)
    r.set(hashValue, data)


def getFromDb(hashValue):
    if r.get(hashValue):
        return json.loads(r.get(hashValue))
    else:
        return False


def existInDb(hashValue):
    if r.get(hashValue):
        return True
    else:
        return False


def cleanRedis():
    keys = r.keys()
    for key in keys:
        r.delete(key)


def createDictory(directoryHash, directory):
    directory.update({"createTime": str(datetime.datetime.now())})
    data = json.dumps(directory)
    print("directory dictionary", data)
    r.set(directoryHash, data)


def existDirInDb(directoryHash):
    if r.get(directoryHash):
        return True
    else:
        return False


def getDicFromDb(directoryHash):
    if r.get(directoryHash):
        return json.loads(r.get(directoryHash))
    else:
        return False


# files = getDicFromDb("2b9984c3f4b3aab6587ae929edbb9c8acfd695ea").get("files")

# for key, value in files.items():
#     print("key ", key)
#     print("value ", value)
# print(getDicFromDb("2b9984c3f4b3aab6587ae929edbb9c8acfd695ea"))
# print(existDirInDb("2b9984c3f4b3aab6587ae929edbb9c8acfd695ea"))
# directory = {
#     "directoryName": "",
#     "createTime": "",
#     "files": {
#         "test/yt": {
#             "originPath": "", "localPath": "", "filehash": ""
#         }
#     }
# }
# directory.get("files").update(
#     {"yuu/hga": {"originPath": 'originPath', "localPath": "local_path"}})

# print(directory)
# directory.update({"createTime": str(datetime.datetime.now())})
# directory.get("files").update(
#     {"15645": {"originPath": "/test", "localPath": "/jj"}})


# print(json.dumps(directory))

# print(datetime.datetime.now())
# dictionary = {'filename': 'test.text', 'story_path': '/uploads'}
# insertIntoDb("3234", dictionary)
# cleanRedis()
# fileDictionary = {'filename': file_name, 'originPath': originPath,
#                   'local_path': local_path}

# value = insertIntoDb(
# "2333", {'filename': 'test.text', 'story_path': '/uploads'})
# print(value)
# value = getFromDb("2333")
# print(value)
