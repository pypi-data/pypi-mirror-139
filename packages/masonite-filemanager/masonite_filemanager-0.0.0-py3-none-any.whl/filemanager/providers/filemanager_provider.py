"""A FilemanagerProvider Service Provider."""
from masonite.packages import PackageProvider


class FileManagerProvider(PackageProvider):
        
    def configure(self):
        (
            self.root("filemanager")
            .name("filemanager")
            .config("config/filemanager.py", publish=True)
            .views("views")
            .assets("assets")
            .routes("routes/route.py")
            
        )
    
    def register(self):
        super().register()
