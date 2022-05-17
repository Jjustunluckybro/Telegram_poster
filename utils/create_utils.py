from .db_api.DataTool import DataTool
from .MediaHandler import MediaHandler

data = DataTool(db_name='data\\data.db')
media_handler = MediaHandler(data=data)
