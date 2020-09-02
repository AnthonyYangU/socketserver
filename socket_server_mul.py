# 非阻塞模块
import socketserver
import os
import buffer
import redisTest
import uuid
# import pymysql
# 首先我们需要定义一个类

# If server and client run in same local directory,
# need a separate place to store the uploads.
try:
    os.mkdir('uploads')
except FileExistsError:
    pass


# redisTest.cleanRedis()


class MySocketServer(socketserver.BaseRequestHandler):
    def setup(self):
        pass

    def handle(self):
        # 定义连接变量
        conn = self.request
        print("client address:", self.client_address)
        connbuf = buffer.Buffer(conn)
        directory = {
            "directoryName": "",
            "files": {
            }
        }

        directoryName = connbuf.get_utf8()
        if not directoryName:
            conn.close()
            return
        directory.update({"directoryName": directoryName})
        print("directoryName ", directoryName)

        directoryHash = connbuf.get_utf8()
        if not directoryHash:
            conn.close()
            return
        directory.update({"directoryHash": directoryHash})
        print("directoryHash ", directoryHash)

        if redisTest.existDirInDb(directoryHash):
            connbuf.put_utf8("find")
            print("directory exist")
            conn.close()
            return
        else:
            connbuf.put_utf8("not find")

        while True:
            file_name = connbuf.get_utf8()
            if not file_name:
                break
            print("file_name ", file_name)

            originPath = connbuf.get_utf8()
            if not originPath:
                break
            print("originPath ", originPath)

            extensionName = file_name[file_name.rfind(".")+1:]
            dirpath = os.path.abspath('./uploads') + "/" + extensionName
            print("extension name ", "."+extensionName)
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)

            local_path = dirpath + '/' + \
                str(uuid.uuid1()) + '.' + extensionName
            fileDictionary = {'local_path': local_path}
            file_name = local_path
            print("local_path is ", local_path)

            file_size = int(connbuf.get_utf8())
            print('file size: ', file_size)

            hash_code = connbuf.get_utf8()
            if not hash_code:
                break
            print('hash code: ', hash_code)
            if redisTest.existInDb(hash_code):
                connbuf.put_utf8("find")
                local_path = redisTest.getFromDb(hash_code).get('local_path')
                print("file exists")
            else:
                connbuf.put_utf8("ok")
                redisTest.insertIntoDb(hash_code, fileDictionary)
                with open(local_path, 'wb') as f:
                    remaining = file_size
                    while remaining:
                        chunk_size = 4096 if remaining >= 4096 else remaining
                        chunk = connbuf.get_bytes(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)
                    if remaining:
                        print('File incomplete.  Missing', remaining, 'bytes.')
                    else:
                        print('File received successfully.')
            directory.get("files").update(
                {originPath: {"filehash": hash_code, "localPath": local_path}})

        redisTest.createDictory(directoryHash, directory)
        print('Connection closed.')
        conn.close()

    def finish(self):
        pass


if __name__ == '__main__':
    # 提示信息
    print("正在等待接收数据。。。。")
    # 创建多线程实例
    server = socketserver.ThreadingTCPServer(
        ("127.0.0.1", 8888), MySocketServer)
    # 开启异步多线程，等待连接
    server.serve_forever()
