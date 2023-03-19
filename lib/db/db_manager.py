import sqlite3
from lib.utils.base import Base
from lib.settings.settings_manager import SettingsManager

class DBManager(Base):
    def __init__(self):
        super().__init__()

        settings_manager = SettingsManager()

        self.__db_name: str = settings_manager.get(self.setting_db_name)

        self.db_connection = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_connection.cursor()

    @property
    def db_name(self) -> str:
        return self.__db_name

    @db_name.setter
    def db_name(self, name: str) -> None:
        self.__db_name = name

    @db_name.deleter
    def db_name(self):
        raise Exception("db_name cannot be deleted")
