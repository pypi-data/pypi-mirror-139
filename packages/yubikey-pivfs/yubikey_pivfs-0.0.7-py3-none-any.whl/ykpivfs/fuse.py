import errno
import logging
import math
import os
import pickle
import threading
import nacl.pwhash
import nacl.secret
import zstd

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from yubikit.piv import MANAGEMENT_KEY_TYPE, SLOT
from .fs import PickleableMemoryFS, PickleableMemoryFSErrors
from .io import PivIo, PivIOErrors


class MemoryFUSE(LoggingMixIn, Operations):

    @staticmethod
    def map_errors(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except PickleableMemoryFSErrors.ResourceNotFound:
                raise FuseOSError(errno.ENOENT)
            except PickleableMemoryFSErrors.PermissionDenied:
                raise FuseOSError(errno.EACCES)
            except PickleableMemoryFSErrors.DestinationExists:
                raise FuseOSError(errno.EEXIST)
            except PickleableMemoryFSErrors.FileExpected:
                raise FuseOSError(errno.EISDIR)
            except PickleableMemoryFSErrors.FileExists:
                raise FuseOSError(errno.EEXIST)
            except PickleableMemoryFSErrors.DirectoryExpected:
                raise FuseOSError(errno.ENOTDIR)
            except PickleableMemoryFSErrors.DirectoryExists:
                raise FuseOSError(errno.EEXIST)
            except PickleableMemoryFSErrors.DirectoryNotEmpty:
                raise FuseOSError(errno.ENOTEMPTY)
        return wrapper

    def __init__(self):
        self.fs = PickleableMemoryFS()
        self.fd = 0

    @map_errors
    def chmod(self, path, mode):
        permissions = self.fs.getmode(path)
        permissions &= 0o0000
        permissions |= mode
        self.fs.setmode(path, permissions)
        return 0

    @map_errors
    def chown(self, path, uid, gid):
        self.fs.setuid(path, uid)
        self.fs.setgid(path, gid)

    @map_errors
    def create(self, path, mode):
        self.fs.create(path)
        self.fd += 1
        return self.fd

    @map_errors
    def getattr(self, path, fh=None):
        return self.fs.getstat(path)

    @map_errors
    def getxattr(self, path, name, position=0):
        attrs = self.fs.getattributes(path)
        try:
            return attrs[name]
        except KeyError:
            return ''  # Should return ENOATTR

    @map_errors
    def listxattr(self, path):
        attrs = self.fs.getattributes(path)
        return attrs.keys()

    @map_errors
    def mkdir(self, path, mode):
        self.fs.makedir(path)

        parent_path = os.path.dirname(path)
        if path != parent_path:
            self.fs.setnlink(parent_path, self.fs.getnlink(parent_path) + 1)

    @map_errors
    def open(self, path, flags):
        self.fd += 1
        return self.fd

    @map_errors
    def read(self, path, size, offset, fh):
        return self.fs.readbytes(path)[offset:offset + size]

    @map_errors
    def readdir(self, path, fh):
        return ['.', '..'] + self.fs.listdir(path)

    @map_errors
    def readlink(self, path):
        link = self.fs.getlink(path)
        return link

    @map_errors
    def removexattr(self, path, name):
        attrs = self.fs.getattributes(path)
        try:
            del attrs[name]
        except KeyError:
            pass  # Should return ENOATTR

    @map_errors
    def rename(self, old, new):
        self.fs.move(old, new, overwrite=True)

    @map_errors
    def rmdir(self, path):
        self.fs.removedir(path)

        parent_path = os.path.dirname(path)
        if path != parent_path:
            self.fs.setnlink(parent_path, self.fs.getnlink(parent_path) - 1)

    @map_errors
    def setxattr(self, path, name, value, options, position=0):
        # Ignore options
        attrs = self.fs.getattributes(path)
        attrs[name] = value

    @map_errors
    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    @map_errors
    def symlink(self, target, source):
        self.fs.makesymlink(source, target)

    @map_errors
    def truncate(self, path, length, fh=None):
        # make sure extending the file fills in zero bytes
        dir_entry_data = self.fs.readbytes(path)
        dir_entry_data = dir_entry_data[:length].ljust(
            length, '\x00'.encode('ascii'))
        self.fs.writebytes(path, dir_entry_data)

    @map_errors
    def unlink(self, path):
        self.fs.remove(path)

    @map_errors
    def utimens(self, path, times=None):
        self.fs.settimes(path)

    @map_errors
    def write(self, path, data, offset, fh):
        dir_entry_data = self.fs.readbytes(path)
        dir_entry_data = (
            # make sure the data gets inserted at the right offset
            dir_entry_data[:offset].ljust(offset, '\x00'.encode('ascii'))
            + data
            # and only overwrites the bytes that data is replacing
            + dir_entry_data[offset + len(data):])
        self.fs.writebytes(path, dir_entry_data)
        return len(data)


class PIVFSErrors:
    class SerializationException(Exception):
        pass

    class DeserializationException(Exception):
        pass


class PIVFS(MemoryFUSE):

    SLOTS = tuple([x.name for x in SLOT])
    SLOTS_RETIRED = tuple(filter(lambda x: 'RETIRED' in x, SLOTS))
    SLOTS_MANAGEMENT_KEY_SLOT = 'KEY_MANAGEMENT'
    MANAGEMENT_KEY_TYPES = tuple([x.name for x in MANAGEMENT_KEY_TYPE])
    DEFAULT_MANAGEMENT_KEY_TYPE = 'TDES'
    DEFAULT_BLOCK_SIZE = 2048

    @staticmethod
    def mount(pivfs, mount_point):
        logging.info('Mounting filesystem on %s.' % mount_point)
        FUSE(pivfs, mount_point, nothreads=True, foreground=True, allow_other=False)

    @classmethod
    def format(cls, management_key, management_key_type, *args, **kwargs):
        logging.info('Initializing new filesystem...')
        fs = cls(*args, **kwargs)
        fs.enable_write(management_key, management_key_type)
        fs.save(record_changes=True)
        fs.save(force_write=True)
        fs.load()
        logging.info('Initialized new filesystem!')

    def __init__(self, pin, key_slot=SLOTS_MANAGEMENT_KEY_SLOT, data_slots=SLOTS_RETIRED, block_size=DEFAULT_BLOCK_SIZE,
                 device_serial=None):
        super().__init__()

        self.read_only = True
        self.permanent_ephemeral_divergence = True
        self.data_slots = data_slots
        self.block_size = block_size
        self.key_size = nacl.secret.SecretBox.KEY_SIZE
        self.block_crypto_overhead = nacl.secret.SecretBox.NONCE_SIZE + nacl.secret.SecretBox.MACBYTES
        self.block_usable_size = self.block_size - self.block_crypto_overhead
        self.serialized_store_padding_size = 4
        self.pivio = PivIo(pin, key_slot, block_size, device_serial)
        self.secretbox = nacl.secret.SecretBox(self.key)
        self._permanent_store = bytes(self.blocks_count * self.block_size)
        self._ephemeral_store = bytes(self._permanent_store)
        self.thread_lock = threading.RLock()
        self.flush_coalescence_timer = None
        self.flush_coalescence_timer_delay = 1

        # sanity checks
        self.is_crypto_sane()
        self.is_serialization_sane()
        self.is_partitioning_sane()

    @property
    def key(self):
        key = ','.join(self.data_slots).encode()
        key = self.pivio.hash(key)[:self.key_size]
        return key

    @property
    def ephemeral_store(self):
        return self._ephemeral_store

    @ephemeral_store.setter
    def ephemeral_store(self, value: bytes):
        self._ephemeral_store = bytes(value)

    @property
    def permanent_store(self):
        return self._permanent_store

    @permanent_store.setter
    def permanent_store(self, value: bytes):
        self._permanent_store = bytes(value)

    @property
    def blocks_count(self):
        return len(self.data_slots)

    @property
    def blocks_used(self):
        return math.ceil(
            (len(self.serialize_store(self.fs.root)) + self.serialized_store_padding_size) / self.block_usable_size
        )

    @property
    def blocks_available(self):
        return self.blocks_count - self.blocks_used

    def encrypt(self, data: bytes):
        return self.secretbox.encrypt(data)

    def decrypt(self, data: bytes):
        return self.secretbox.decrypt(data)

    def is_crypto_sane(self):
        plaintext = b'123456'
        ciphertext = self.encrypt(plaintext)
        assert self.decrypt(ciphertext) == plaintext

    @staticmethod
    def compress(data: bytes):
        logging.debug('compressing %s' % hash(data))
        data_size = len(data)
        cd = zstd.compress(data, 21)
        cd_size = len(cd)
        logging.debug('compressed %s with ratio %s' % (hash(data), (cd_size / data_size)))
        return cd

    @staticmethod
    def decompress(data: bytes):
        logging.debug('decompressing %s' % hash(data))
        data_size = len(data)
        dd = zstd.decompress(data)
        dd_size = len(dd)
        logging.debug('decompressed %s with ratio %s' % (hash(data), (data_size / dd_size)))
        return dd

    @staticmethod
    def serialize_store(store):
        try:
            ss = pickle.dumps(store)
            ss = PIVFS.compress(ss)
        except:
            raise PIVFSErrors.SerializationException
        return ss

    @staticmethod
    def deserialize_store(serialized_store):
        try:
            ds = PIVFS.decompress(serialized_store)
            ds = pickle.loads(ds, encoding='bytes')
        except:
            raise PIVFSErrors.DeserializationException
        return ds

    def is_serialization_sane(self):
        store = {"a": [True, 123, 123456]}
        ss = self.serialize_store(store)
        ds = self.deserialize_store(ss)
        assert store == ds

    def store_to_blocks(self, store_serialized):
        store_serialized_size = len(store_serialized)
        store_serialized = store_serialized.ljust(
            self.blocks_count * self.block_usable_size - self.serialized_store_padding_size,
            b'\x00'
        )
        store_serialized += store_serialized_size.to_bytes(self.serialized_store_padding_size, byteorder='little')
        max_size = max(self.blocks_count * self.block_usable_size, len(store_serialized))
        for x in range(0, max_size, self.block_usable_size):
            block = store_serialized[x:x + self.block_usable_size]
            yield block

    def store_from_blocks(self, blocks):
        store_serialized = bytearray()
        for block in blocks:
            store_serialized.extend(block)
        store_serialized_size = store_serialized[len(store_serialized)-self.serialized_store_padding_size:]
        store_serialized_size = int.from_bytes(store_serialized_size, byteorder='little')
        store_serialized = bytes(store_serialized[0:store_serialized_size])
        return store_serialized

    def is_partitioning_sane(self):
        store = (dict(), dict())
        ss = self.serialize_store(store)
        ssb = self.store_to_blocks(ss)
        dsb = self.store_from_blocks(ssb)
        ds = self.deserialize_store(dsb)
        assert store == ds

    def enable_write(self, management_key, management_key_type):
        self.pivio.authenticate(management_key, management_key_type)
        self.read_only = False

    def write_block(self, block: int, data: bytes):
        data = self.encrypt(data)
        try:
            self.pivio.write(data, self.data_slots[block])
        except PivIOErrors.UnauthenticatedWriteException as e:
            if self.read_only:
                raise FuseOSError(errno.EROFS)
            raise e

    def read_block(self, block: int):
        data = self.pivio.read(self.data_slots[block])
        data = self.decrypt(data)
        return data

    def save(self, record_changes=False, force_write=False):
        logging.debug('save %s %s' % (record_changes, force_write))

        if record_changes:
            self.ephemeral_store = self.serialize_store(self.fs.root)
            return

        ephemeral_store_blocks = tuple(self.store_to_blocks(self.ephemeral_store))
        permanent_store_blocks = tuple(self.store_to_blocks(self.permanent_store))
        for x in range(self.blocks_count):
            if force_write or (hash(ephemeral_store_blocks[x]) != hash(permanent_store_blocks[x])):
                self.write_block(x, ephemeral_store_blocks[x])
                self.permanent_ephemeral_divergence = True

    def load(self):
        logging.debug('load')

        if self.permanent_ephemeral_divergence:
            permanent_store_blocks = [self.read_block(x) for x, s in enumerate(self.data_slots)]
            self.permanent_store = self.store_from_blocks(permanent_store_blocks)
            self.ephemeral_store = self.permanent_store
            self.fs.root = self.deserialize_store(self.ephemeral_store)
            self.permanent_ephemeral_divergence = False

    @staticmethod
    def synchronize_threads(f):
        def wrapper(self, *args, **kwargs):
            self.thread_lock.acquire()
            try:
                r = f(self, *args, **kwargs)
            finally:
                self.thread_lock.release()
            return r
        return wrapper

    @synchronize_threads
    def _flush(self):
        logging.debug('flushing')
        try:
            self.save()
        finally:
            self.load()
        logging.debug('flushed')

    @synchronize_threads
    def flush(self, path=None, fh=None):
        if self.blocks_used > self.blocks_count:
            raise FuseOSError(errno.ENOSPC)
        else:
            self.save(record_changes=True)

        if self.flush_coalescence_timer:
            logging.debug('cancelling scheduled flush')
            self.flush_coalescence_timer.cancel()

        logging.debug('scheduling flush in %s seconds' % self.flush_coalescence_timer_delay)
        self.flush_coalescence_timer = threading.Timer(self.flush_coalescence_timer_delay, self._flush)
        self.flush_coalescence_timer.start()

    @staticmethod
    def flushable(f):
        def wrapper(self, *args, **kwargs):
            try:
                r = f(self, *args, **kwargs)
            finally:
                self.flush()
            return r
        return wrapper

    @flushable
    @synchronize_threads
    def fsync(self, path, datasync, fh):
        pass

    @flushable
    @synchronize_threads
    def fsyncdir(self, path, datasync, fip):
        pass

    @synchronize_threads
    def statfs(self, path):
        return {
            'f_bsize': self.block_size,
            'f_blocks': self.blocks_count,
            'f_bfree': self.blocks_available,
            'f_bavail': self.blocks_available
        }

    @flushable
    @synchronize_threads
    def chmod(self, path, mode):
        return super().chmod(path, mode)

    @flushable
    @synchronize_threads
    def chown(self, path, uid, gid):
        return super().chown(path, uid, gid)

    @flushable
    @synchronize_threads
    def create(self, path, mode):
        return super().create(path, mode)

    @synchronize_threads
    def getattr(self, path, fh=None):
        return super().getattr(path, fh)

    @synchronize_threads
    def getxattr(self, path, name, position=0):
        return super().getxattr(path, name, position)

    @synchronize_threads
    def listxattr(self, path):
        return super().listxattr(path)

    @flushable
    @synchronize_threads
    def mkdir(self, path, mode):
        return super().mkdir(path, mode)

    @synchronize_threads
    def open(self, path, flags):
        return super().open(path, flags)

    @synchronize_threads
    def read(self, path, size, offset, fh):
        return super().read(path, size, offset, fh)

    @synchronize_threads
    def readdir(self, path, fh):
        return super().readdir(path, fh)

    @synchronize_threads
    def readlink(self, path):
        return super().readlink(path)

    @flushable
    @synchronize_threads
    def removexattr(self, path, name):
        return super().removexattr(path, name)

    @flushable
    @synchronize_threads
    def rename(self, old, new):
        return super().rename(old, new)

    @flushable
    @synchronize_threads
    def rmdir(self, path):
        return super().rmdir(path)

    @flushable
    @synchronize_threads
    def setxattr(self, path, name, value, options, position=0):
        return super().setxattr(path, name, value, options, position)

    @flushable
    @synchronize_threads
    def symlink(self, target, source):
        return super().symlink(target, source)

    @flushable
    @synchronize_threads
    def truncate(self, path, length, fh=None):
        return super().truncate(path, length, fh)

    @flushable
    @synchronize_threads
    def unlink(self, path):
        return super().unlink(path)

    @flushable
    @synchronize_threads
    def utimens(self, path, times=None):
        return super().utimens(path, times)

    @flushable
    @synchronize_threads
    def write(self, path, data, offset, fh):
        return super().write(path, data, offset, fh)
