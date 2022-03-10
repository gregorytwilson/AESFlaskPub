import base64
import random
import string

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from Crypto.Cipher import AES
from Crypto import Random

app = Flask(__name__)
api = Api(app)

class AESAPI(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        parser.add_argument('key', type=str)
        args = parser.parse_args()
        plaintext = args['data']
        AESkey = args['key']

        iv = Random.new().read(AES.block_size)
        cipher = AES.new(AESkey, AES.MODE_CBC, iv)
        while len(bytes(plaintext, encoding='utf-8')) % 16 != 0:
            plaintext = plaintext + random.choice(string.ascii_letters)
        res = cipher.encrypt(plaintext)
        print(res)
        ret = str(base64.b64encode(res),'utf-8')
        print(ret)
        return jsonify("encrypted",ret)

api.add_resource(AESAPI, '/aes', endpoint='aes')


if __name__ == '__main__':
    app.run(host="0.0.0.0")

