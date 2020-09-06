from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
from .dependencies.redis import MessageStore


class KonnichiwaService:
    name = 'konnichiwa_service'

    @rpc
    def konnichiwa(self):
        return 'Konnichiwa!'


class WebServer:
    name = 'web_server'
    konnichiwa_service = RpcProxy('konnichiwa_service')

    @http('GET', '/')
    def home(self, request):
        return self.konnichiwa_service.konnichiwa()


class MessageService:
    name = 'message_service'
    message_store = MessageStore()

    @rpc
    def get_message(self, message_id):
        return self.message_store.get_message(message_id)
