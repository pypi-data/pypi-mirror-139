import os
from pathlib import Path
import shutil
import time
import mimetypes
class FileManagerDriver:
    
    def __init__(self):
        from wsgi import application
        
        self.application = application
        self.storage = application.make("storage")
        self.root = self.storage.disk("local")
        self.root_path = self.root.get_path("filemanager")
        
    def _get_path(self, extra=None) -> str:
        request = self.application.make("request")
        folder = request.input('folder', None)
        
        path = self.root_path
        if folder:
            folders = folder.split(",")
            path = os.path.join(self.root_path, *folders)
            
        if extra:
            path = os.path.join(path, extra)
        
        return path
    
    def _get_media_type(self, file) -> any:
        mime = mimetypes.guess_type(file.name)[0]
        return mime
    
    def total_size(self):
        size = sum(file.stat().st_size for file in Path(self.root_path).rglob('*'))
        return self.convert_bytes(size)
    
    def upload(self, file):
        request = self.application.make("request")
        folder = request.input('folder', None)
        path = "filemanager"
        
        if folder:
            path = "filemanager/{}".format(folder.replace(",", "/"))
        
        self.storage.disk('local').put_file(path, file)
        
    def rename(self, path, name):
        if os.path.exists(path):
            # check if path is file
            if os.path.isfile(path):
                name = "{name}.{ext}".format(name=name, ext=path.split(".")[-1])
            os.rename(path, self._get_path(name))
            return True
        return False
        
    def all_files(self):
        data = {
            "folders": [],
            "files": [],
            "total_size": self.total_size(),
        }
        
        path = self._get_path()
        
        with os.scandir(path) as entries:
            for item in entries:
                name = item.name
                byte_size = item.stat().st_size if item.is_file() else sum(file.stat().st_size for file in Path(item.path).rglob('*'))
                size = self.convert_bytes(byte_size)
                created_at = time.ctime(item.stat().st_ctime)
                modified_at = time.ctime(item.stat().st_mtime)
                
                file_url = item.path.replace(self.root.get_path(""), "")
                file_url = "/uploads/" + file_url.replace("\\", "/")
                
                file_item = {
                    "name": name if item.is_dir() else item.name.split('.')[0],
                    "size": size,
                    "created_at": created_at,
                    "modified_at": modified_at,
                    "path": item.path
                }
                
                if item.is_dir():
                    file_item['total_files'] = len(os.listdir(item.path))
                    # get if file is image or video
                    
                    data.get("folders").append(file_item)
                else:
                    file_item['url'] = file_url
                    file_item['mime'] = self._get_media_type(item)
                    data.get("files").append(file_item)
        
        return data
    
    def exists(self, name):
        return os.path.exists(self._get_path(name))
    
    def create_folder(self, name) -> bool:
        # create folder
        try:
            path = self._get_path(name)
            if not self.exists(path):
                os.mkdir(self._get_path(name))
                return True
        except Exception as e:
            print(e)
        return False
        
    def delete_folder(self, path):
        try:
            if os.path.exists(path):
                if len(os.listdir(path)) > 0:
                    shutil.rmtree(path)
                else:
                    os.rmdir(path)
                return True
        except Exception as e:
            print(e)
        return False
        
    def delete_file(self, path):
        try:
            if os.path.exists(path):
                os.remove(path)
                return True
        except Exception as e:
            print(e)
        return False
        
    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        step_unit = 1000.0 #1024 bad the size

        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < step_unit:
                return "%3.1f %s" % (num, x)
            num /= step_unit