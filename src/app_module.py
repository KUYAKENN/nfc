from nest.core import PyNestFactory, Module
        
from .app_controller import AppController
from .app_service import AppService
from .contact_controller import ContactController
from .static_controller import StaticController
from .contact_service import ContactService


@Module(
    imports=[], 
    controllers=[AppController, ContactController, StaticController], 
    providers=[AppService, ContactService]
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="NFC Contact Sharing Application",
    title="NFC Contact App",
    version="1.0.0",
    debug=True,
)

http_server = app.get_server()

                