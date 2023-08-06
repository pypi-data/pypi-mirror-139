from masonite.controllers import Controller
from masonite.request import Request
from masonite.request import Request
from masonite.response import Response
from masonite.views import View

from ..drivers.filemanager_driver import FileManagerDriver

class FileManagerController(Controller):
    
    def __init__(self, response: Response) -> None:
        self.response = response
        self.filemanager = FileManagerDriver()

    def index(self, view: View):
        size = self.filemanager.total_size()
        return view.render("filemanager.index", {
            "size": size,
        })
    
    def all_files(self):
        return self.filemanager.all_files()
    
    def upload(self, request: Request):
        file = request.input('file')
        self.filemanager.upload(file)
        
        return self.response.json({
            "message": "File uploaded!",
        })
        
    def rename(self, request: Request):
        name = request.input('name')
        path = request.input('path')
        self.filemanager.rename(path, name)
        
        return self.response.json({
            "message": "File/Folder renamed!",
        })
    
    def create_folder(self, request: Request):
        name = request.input('name')
        
        if not self.filemanager.exists(name):
            self.filemanager.create_folder(name)
            
            return self.response.json({
                "message": 'Folder Created...',
            })
            
        return self.response.json({
            "message": "Folder already exists!",
        })
        
    def delete_folder(self, request: Request):
        path = request.input('path')
        
        try:
            self.filemanager.delete_folder(path)
            
            return self.response.json({
                "message": 'Folder deleted...',
            })
        except Exception as e:
            print(e)
            
        return self.response.json({
            "message": "Folder doesn't exists!",
        })
        
    def delete_file(self, request: Request):
        path = request.input('path')
        
        try:
            self.filemanager.delete_file(path)
            
            return self.response.json({
                "message": 'Folder deleted...',
            })
        except Exception as e:
            print(e)
            
        return self.response.json({
            "message": "Folder doesn't exists!",
        })