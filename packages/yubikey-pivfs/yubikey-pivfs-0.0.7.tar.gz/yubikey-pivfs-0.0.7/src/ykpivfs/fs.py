import os
import stat
import fs.memoryfs

from threading import RLock


class PickleableDirEntry(fs.memoryfs._DirEntry):

    def __init__(self, resource_type, name):
        super().__init__(resource_type, name)
        self.st_nlink = 2 if self.is_dir else 1
        self.st_uid = os.getuid()
        self.st_gid = os.getgid()
        self._st_mode = self.default_st_mode(resource_type)
        self.attributes = {}
        self.link = None

    @property
    def accessed_time(self):
        return self.modified_time

    @accessed_time.setter
    def accessed_time(self, value):
        pass

    @staticmethod
    def default_st_mode(resource_type):
        st_mode = None

        # apply filetype part
        if resource_type == fs.memoryfs.ResourceType.directory:
            st_mode = stat.S_IFDIR
        elif resource_type == fs.memoryfs.ResourceType.character:
            st_mode = stat.S_IFCHR
        elif resource_type == fs.memoryfs.ResourceType.block_special_file:
            st_mode = stat.S_IFBLK
        elif resource_type == fs.memoryfs.ResourceType.file:
            st_mode = stat.S_IFREG
        elif resource_type == fs.memoryfs.ResourceType.fifo:
            st_mode = stat.S_IFIFO
        elif resource_type == fs.memoryfs.ResourceType.symlink:
            st_mode = stat.S_IFLNK
        elif resource_type == fs.memoryfs.ResourceType.socket:
            st_mode = stat.S_IFSOCK
        else:
            raise ValueError(resource_type)

        # apply permission part
        permissions = 0o644
        if resource_type == fs.memoryfs.ResourceType.directory:
            permissions = 0o755
        elif resource_type == fs.memoryfs.ResourceType.symlink:
            permissions = 0o777
        st_mode |= permissions

        return st_mode

    @property
    def st_mode(self):
        return self._st_mode

    @st_mode.setter
    def st_mode(self, value):
        value &= 0o7777
        st_mode = stat.S_IFMT(self.st_mode) | value
        self._st_mode = st_mode

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_open_files']
        del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._open_files = []
        self.lock = RLock()

    @property
    def is_link(self):
        return self.resource_type == fs.memoryfs.ResourceType.symlink

    def to_info(self, namespaces=None):
        info = super().to_info(namespaces).raw
        namespaces = namespaces or ()
        if 'stat' in namespaces:
            info['stat'] = {
                'st_mode': self.st_mode,
                'st_nlink': self.st_nlink,
                'st_uid': self.st_uid,
                'st_gid': self.st_gid,
                'st_ctime': self.created_time,
                'st_mtime': self.modified_time,
                'st_atime': self.accessed_time,
                'st_size': self.size
            }
        if 'attributes' in namespaces:
            info['attributes'] = self.attributes.copy()
        if 'link' in namespaces:
            info['link'] = {'target': self.link}
        return fs.memoryfs.Info(info)


PickleableMemoryFSErrors = fs.memoryfs.errors


class PickleableMemoryFS(fs.memoryfs.MemoryFS):

    def _make_dir_entry(self, resource_type, name):
        return PickleableDirEntry(resource_type, name)

    def makesymlink(self, source_path, target_path):
        _source_path = self.validatepath(source_path)
        _target_path = self.validatepath(target_path)
        with self._lock:
            target_name = os.path.basename(target_path)
            target_parent_path = os.path.dirname(target_path)
            target_parent_dir_entry = self._get_dir_entry(target_parent_path)

            target_dir_entry = target_parent_dir_entry.get_entry(target_path)
            if target_dir_entry is not None:
                raise fs.memoryfs.errors.DestinationExists(target_path)

            target_dir_entry = self._make_dir_entry(fs.memoryfs.ResourceType.symlink, target_name)
            target_parent_dir_entry.set_entry(target_name, target_dir_entry)
            self.setlink(target_path, source_path)

    def setinfo(self, path, info):
        if path == '/':
            return

        super().setinfo(path, info)
        dir_entry = self._get_dir_entry(path)
        if 'stat' in info:
            stat = info['stat']
            if 'st_mode' in stat:
                dir_entry.st_mode = stat['st_mode']
            if 'st_nlink' in stat:
                dir_entry.st_nlink = stat['st_nlink']
            if 'st_uid' in stat:
                dir_entry.st_uid = stat['st_uid']
            if 'st_gid' in stat:
                dir_entry.st_gid = stat['st_gid']
        if 'attributes' in info:
            dir_entry.attributes = info['attributes']
        if 'link' in info:
            dir_entry.link = info['link']['target']

    def getstat(self, path):
        return self.getinfo(path, namespaces=["stat"]).raw['stat']

    def getmode(self, path):
        return self.getstat(path)['st_mode']

    def setmode(self, path, st_mode):
        self.setinfo(path, {'stat': {'st_mode': st_mode}})

    def getnlink(self, path):
        return self.getstat(path)['st_nlink']

    def setnlink(self, path, st_nlink):
        self.setinfo(path, {'stat': {'st_nlink': st_nlink}})

    def getuid(self, path):
        return self.getstat(path)['st_uid']

    def setuid(self, path, st_uid):
        self.setinfo(path, {'stat': {'st_uid': st_uid}})

    def getgid(self, path):
        return self.getstat(path)['st_gid']

    def setgid(self, path, st_gid):
        self.setinfo(path, {'stat': {'st_gid': st_gid}})

    def getattributes(self, path):
        return self.getinfo(path, namespaces=["attributes"]).raw['attributes']

    def setattributes(self, path, attributes):
        self.setinfo(path, {'attributes': attributes})

    def getlink(self, path):
        return self.getinfo(path, namespaces=["link"]).raw['link']['target']

    def setlink(self, path, link):
        self.setinfo(path, {'link': {'target': link}})
