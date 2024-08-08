import os
import certifi
import grpc

from proto import nezha_pb2
from proto import nezha_pb2_grpc


class AuthGateway(grpc.AuthMetadataPlugin):
    def __init__(self, token):
        self.token = token

    def __call__(self, context, callback):
        metadata = (('client_secret', self.token),)
        callback(metadata, None)


def load_credentials():
    with open(certifi.where(), 'rb') as f:
        return f.read()


def main():
    # 未接入CDN的面板服务器域名/IP
    address = os.getenv('NEZHA_SERVER_ADDRESS')

    # 密钥
    secret = os.getenv('NEZHA_SERVER_SECRET')

    channel_credentials = grpc.ssl_channel_credentials(load_credentials())

    call_credentials = grpc.metadata_call_credentials(AuthGateway(token=secret))

    composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)

    channel = grpc.secure_channel(address, composite_credentials)

    stub = nezha_pb2_grpc.NezhaServiceStub(channel)

    host = nezha_pb2.Host()
    host.platform = 'platform'
    host.platform_version = 'platform_version'
    host.cpu.append('cpu')
    host.mem_total = 1
    host.disk_total = 2
    host.arch = 'arch'
    host.swap_total = 3
    host.boot_time = 4
    host.version = 'version'

    response = stub.ReportSystemInfo(host)
    print(response)

    channel.close()


if __name__ == '__main__':
    main()
