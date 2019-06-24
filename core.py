from dialog_api import registration_pb2_grpc, messaging_pb2_grpc, media_and_files_pb2_grpc, \
    sequence_and_updates_pb2_grpc, authentication_pb2_grpc, contacts_pb2_grpc, search_pb2_grpc, users_pb2_grpc, \
    registration_pb2, authentication_pb2, sequence_and_updates_pb2, groups_pb2_grpc, contacts_pb2, peers_pb2

import grpc
from queue import Queue
from threading import Thread
from google.protobuf import empty_pb2


class SDK:
    def __init__(self, endpoint):
        self.app_id = 10
        self.app_title = "Monitoring"
        self.channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials())
        self.registration = self.wrap_service(registration_pb2_grpc.RegistrationStub)
        self.token = self.get_session_token()
        self.messaging = self.wrap_service(messaging_pb2_grpc.MessagingStub)
        self.media_and_files = self.wrap_service(media_and_files_pb2_grpc.MediaAndFilesStub)
        self.updates = self.wrap_service(sequence_and_updates_pb2_grpc.SequenceAndUpdatesStub)
        self.auth = self.wrap_service(authentication_pb2_grpc.AuthenticationStub)
        self.contacts = self.wrap_service(contacts_pb2_grpc.ContactsStub)
        self.groups = self.wrap_service(groups_pb2_grpc.GroupsStub)
        self.search = self.wrap_service(search_pb2_grpc.SearchStub)
        self.users = self.wrap_service(users_pb2_grpc.UsersStub)
        self.seq_update_queue = Queue()
        self.seq_update_thread = Thread(target=self.seq_update_handler)
        self.user_info = None
        self.phone = None

    def run_seq_updates_thread(self):
        self.seq_update_thread.start()

    def wrap_service(self, stub_func):
        """Wrapper for authenticating of gRPC service calls.

        :param stub_func: name of gRPC service
        :return: wrapped gRPC service
        """
        return AuthenticatedService(
            lambda: self.token if hasattr(self, 'token') else None,
            stub_func(self.channel)
        )

    def get_session_token(self):
        """Requests for sessions token for device.

        :return: session token
        """
        registration_response = self.registration.RegisterDevice(
            registration_pb2.RequestRegisterDevice(
                app_id=self.app_id,
                app_title=self.app_title,
                device_title=self.app_title
            )
        )
        return registration_response.token

    def bot_authorize(self, token):
        self.token = self.get_session_token()
        return self.auth.StartTokenAuth(
            authentication_pb2.RequestStartTokenAuth(
                token=token,
                app_id=self.app_id
            )
        )

    def login_authorize(self, login, password):
        auth_response = self.auth.StartUsernameAuth(
            authentication_pb2.RequestStartUsernameAuth(
                username=login,
                app_id=self.app_id,
                device_title=self.app_title,
                preferred_languages=['EN']
            )
        )

        validation_result = self.auth.ValidatePassword(
            authentication_pb2.RequestValidatePassword(
                transaction_hash=auth_response.transaction_hash,
                password=password
            )
        )

        return validation_result

    def logout(self):
        self.auth.SignOut(authentication_pb2.RequestSignOut())

    def seq_update_handler(self):
        for update in self.updates.SeqUpdates(empty_pb2.Empty()):
            up = sequence_and_updates_pb2.UpdateSeqUpdate()
            up.ParseFromString(update.update.value)
            self.seq_update_queue.put(up)
            break

    def get_next_seq_update(self):
        yield self.seq_update_queue.get()

    def find_user_outpeer_by_nick(self, nick):
        """Returns user's Outpeer object by nickname for direct messaging

        :param nick: user's nickname
        :return: Outpeer object of user
        """
        users = self.contacts.SearchContacts(
            contacts_pb2.RequestSearchContacts(
                request=nick
            )
        ).users

        for user in users:
            if user.data.nick.value == nick:
                outpeer = peers_pb2.OutPeer(
                    type=peers_pb2.PEERTYPE_PRIVATE,
                    id=int(user.id),
                    access_hash=int(user.access_hash)
                )
                return outpeer
        return None


class AuthenticatedService(object):
    """Initialization class for gRPC services.

    """

    def __init__(self, auth_token_func, stub):
        self.stub = stub
        self.auth_token_func = auth_token_func
        for method_name in dir(stub):
            method = getattr(stub, method_name)
            if not method_name.startswith('__') and callable(method):
                setattr(self, method_name, self.__decorated(method_name, method))

    def __decorated(self, method_name, method):
        # print(method_name)
        def inner(param):
            auth_token = self.auth_token_func()
            print('Calling %s with token=`%s`' % (method_name, auth_token))
            if auth_token is not None:
                metadata = (('x-auth-ticket', auth_token),)
            else:
                metadata = None
            return method(param, metadata=metadata)

        return inner
