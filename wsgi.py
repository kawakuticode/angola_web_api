from application.application_factory import create_app
from os import path
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), "application/logs.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('angolaWebApi')
print(logger)

app = create_app()
if __name__ == "__main__":
    app.run()
