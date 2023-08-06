import logging

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from ykman.device import connect_to_device
from yubikit.core.smartcard import SmartCardConnection, ApduError, SW
from yubikit.piv import PivSession, MANAGEMENT_KEY_TYPE, SLOT, OBJECT_ID


class PivIOErrors:
    class UnauthenticatedWriteException(Exception):
        pass


class PivIo:

    def __init__(self, pin: str, key_slot: str, slot_size: int, device_serial: int):
        self.connection, self.device, self.info = connect_to_device(
            serial=device_serial,
            connection_types=[SmartCardConnection],
        )
        self.piv = PivSession(self.connection)
        self.pin = pin
        self.pin_attempts = self.piv.get_pin_attempts()
        if self.pin_attempts == 0:
            raise RuntimeError('PIN blocked!')
        self.piv.verify_pin(pin)
        self.key_slot = SLOT[key_slot]
        self.key_slot_meta = self.piv.get_slot_metadata(self.key_slot)
        self.key_slot_publickey = self.piv.get_certificate(self.key_slot).public_key()
        self.hash_algorithm = hashes.SHA256()
        self.crypt_padding = padding.OAEP(
            mgf=padding.MGF1(algorithm=self.hash_algorithm),
            algorithm=self.hash_algorithm,
            label=None
        )
        self.sign_padding = padding.PSS(
            mgf=padding.MGF1(algorithm=self.hash_algorithm),
            salt_length=0
        )
        self.message_block_size = self.key_slot_publickey.key_size - self.hash_algorithm.digest_size * 2 - 2
        self.slot_block_size = slot_size

    def __del__(self):
        self.connection.close()

    def authenticate(self, management_key: bytes, management_key_type: str):
        self.piv.authenticate(MANAGEMENT_KEY_TYPE[management_key_type], management_key)

    @staticmethod
    def check_slot_data(f):
        def wrapper(*args, **kwargs):
            self, data = args[0], args[1]
            if len(data) > self.slot_block_size:
                raise ValueError('Argument data exceeds maximum block size of %s' % self.slot_block_size)
            return f(*args, **kwargs)
        return wrapper

    @staticmethod
    def check_message_data(f):
        def wrapper(*args, **kwargs):
            self, data = args[0], args[1]
            if len(data) > self.message_block_size:
                raise ValueError('Argument data exceeds maximum block size of %s' % self.message_block_size)
            return f(*args, **kwargs)
        return wrapper

    def read(self, slot: str):
        logging.debug('reading block on %s' % slot)
        data = bytes(self.slot_block_size)
        try:
            data = self.piv.get_object(OBJECT_ID[slot])[:self.slot_block_size]
        except ApduError as e:
            if e.sw != SW.FILE_NOT_FOUND:
                raise e
        logging.debug('read %s on %s' % (hash(data), slot))
        return data

    @check_slot_data
    def write(self, data: bytes, slot: str):
        logging.debug('writing %s on %s' % (hash(data), slot))
        try:
            self.piv.put_object(OBJECT_ID[slot], data)
        except ApduError as e:
            if e.sw == SW.SECURITY_CONDITION_NOT_SATISFIED:
                raise PivIOErrors.UnauthenticatedWriteException()

        logging.debug('wrote %s on %s' % (hash(data), slot))

    @check_message_data
    def encrypt(self, data: bytes):
        return self.key_slot_publickey.encrypt(data, self.crypt_padding)

    @check_message_data
    def decrypt(self, data: bytes):
        return self.piv.decrypt(self.key_slot, data, self.crypt_padding)

    @check_message_data
    def sign(self, data: bytes):
        return self.piv.sign(self.key_slot, self.key_slot_meta.key_type, data, self.hash_algorithm, self.sign_padding)

    @check_message_data
    def hash(self, data: bytes):
        hasher = hashes.Hash(self.hash_algorithm)
        hasher.update(self.sign(data))
        return hasher.finalize()
