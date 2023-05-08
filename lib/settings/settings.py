from lib.utils.logger import Logger
import json
from lib.file.file_manager import FileManger
import os
from typing import Any
from lib.utils.base import Base
from lib.utils.utils import Utils


class SettingsBase:
    WORK_DIRECTORY_NAME = "work"
    SETTINGS_FILE_NAME = "settings.json"
    VAULT_FILE_NAME = "vault.json"

    KEY_DB_NAME = "db_name"
    VALUE_BASE_DB_NAME = "database.db"

    KEY_VERBOSE = "verbose"
    VALUE_BASE_VERBOSE = True

    KEY_PROJECT_PATH = "project_path"
    VALUE_BASE_PROJECT_PATH = os.path.expanduser("~/Desktop")

    KEY_VAULT_PATH = "vault_path"
    VALUE_BASE_VAULT_PATH = os.getcwd()

    KEY_DB_LOCALTIME = "use_localtime"
    VALUE_BASE_DB_LOCALTIME = True

    KEY_DEBUG_MODE = "debug"
    VALUE_BASE_DEBUG_MODE = False

    KEY_FRONTEND_DIRECTORY = "frontend"
    VALUE_BASE_FRONTEND_DIRECTORY = os.path.join(os.path.curdir, "../frontend/dist/frontend")

    KEY_FRONTEND_START = "frontend_start"
    VALUE_BASE_FRONTEND_START = "index.html"

    KEY_APP_PORT = "port"
    VALUE_BASE_APP_PORT = 8000

    KEY_FRONTEND_DEBUG_PORT = "frontend_debug_port"
    VALUE_BASE_FRONTEND_DEBUG_PORT = 4200

    BASE_SETTINGS = {
        KEY_DB_NAME: VALUE_BASE_DB_NAME,
        KEY_VERBOSE: VALUE_BASE_VERBOSE,
        KEY_PROJECT_PATH: VALUE_BASE_PROJECT_PATH,
        KEY_DB_LOCALTIME: VALUE_BASE_DB_LOCALTIME,
        KEY_DEBUG_MODE: VALUE_BASE_DEBUG_MODE,
        KEY_FRONTEND_DIRECTORY: VALUE_BASE_FRONTEND_DIRECTORY,
        KEY_FRONTEND_START: VALUE_BASE_FRONTEND_START,
        KEY_APP_PORT: VALUE_BASE_APP_PORT,
        KEY_VAULT_PATH: VALUE_BASE_VAULT_PATH,
        KEY_FRONTEND_DEBUG_PORT: VALUE_BASE_FRONTEND_DEBUG_PORT
    }

    @staticmethod
    def settings_path() -> str:
        """
        Return the settings path of the app

        :rtype: str
        """

        return os.path.join(Base.base_directory(), SettingsBase.SETTINGS_FILE_NAME)


class SettingsManager(SettingsBase):
    create_settings_file_if_not_exist = True

    def __init__(self):

        self.settings: dict = self.BASE_SETTINGS  # set base settings

        try:
            self.override_settings()

        except IOError as io_error:
            print(f"Configuration file {self.SETTINGS_FILE_NAME} not found")

            if SettingsManager.create_settings_file_if_not_exist:
                self.create_settings_file()
                self.override_settings()

        except json.JSONDecodeError as json_decode_error:
            print(f"Configuration file {self.SETTINGS_FILE_NAME} JSON syntax error")
            Utils.exit()

        finally:
            self.verify_mandatory_settings()

    def verify_mandatory_settings(self) -> None:
        """
        Verify mandatory settings and throw exceptions
        """

        try:
            self.get_setting_by_key(self.KEY_PROJECT_PATH)

        except KeyError as key_error:
            print(f"'{self.KEY_PROJECT_PATH}' is mandatory setting")
            Utils.exit()

    def override_settings(self) -> None:
        """
        Override app settings with settings configuration file
        """

        self.settings.update(FileManger.read_json(self.settings_path()))

    def create_settings_file(self) -> None:
        """
        Create settings file if it does not exist with base settings
        """

        FileManger.write_json(self.settings_path(), self.settings_path())

    def set(self, key: str, value: str) -> None:
        """
        Modify settings

        :param key: settings' key
        :param value: key's value

        :rtype: None
        """
        self.settings[key] = value

    def get_setting_by_key(self, key: str) -> Any:
        """
        Return the value of key passed

        :param key: A key of settings
        :type key: str

        :rtype: str
        """

        return self.settings[key]

    @property
    def verbose(self) -> bool:
        """
        Return verbose mode

        :return: verbose
        :rtype bool:
        """

        return self.get_setting_by_key(SettingsBase.KEY_VERBOSE)

    @property
    def project_directory_path(self) -> str:
        """
        Return the app directory

        :rtype: str
        """

        return os.path.abspath(self.get_setting_by_key(self.KEY_PROJECT_PATH))

    @property
    def work_directory_path(self) -> str:
        """
        Return the work directory path inside the app

        :return:
        """

        return os.path.join(self.project_directory_path, self.WORK_DIRECTORY_NAME)

    @property
    def db_name(self) -> str:
        """
        Return the database name

        :rtype: str
        """

        return self.get_setting_by_key(self.KEY_DB_NAME)

    @property
    def db_path(self) -> str:
        """
        Return the database path of the app

        :rtype: str
        """

        return os.path.join(self.work_directory_path, self.get_setting_by_key(self.KEY_DB_NAME))

    @property
    def vault_path(self) -> str:
        """
        Return the vault path of the app.
        Vault is the file where are stored login information

        :rtype: str
        """

        return os.path.join(self.get_setting_by_key(self.KEY_VAULT_PATH), SettingsBase.VAULT_FILE_NAME)

    @property
    def debug_mode(self) -> bool:
        """
        Return True if app is in debug mode

        :return: Mode
        :rtype bool:
        """

        return self.get_setting_by_key(SettingsBase.KEY_DEBUG_MODE)

    @property
    def frontend_directory(self) -> str:
        """
        Return frontend directory of app

        :return: directory
        :rtype str:
        """

        return self.get_setting_by_key(SettingsBase.KEY_FRONTEND_DIRECTORY)

    @property
    def frontend_start(self) -> str:
        """
        Return the start file of frontend.
        If app is in debug mode return { 'port': 4200 } to use Angular in dev mode

        :rtype str:
        """

        if self.debug_mode:

            return { 'port': int(self.get_setting_by_key(SettingsBase.KEY_FRONTEND_DEBUG_PORT))}

        return self.get_setting_by_key(SettingsBase.KEY_FRONTEND_START)

    @property
    def port(self) -> int:
        """
        Return the port to use (in Eel)

        :rtype int:
        """

        return self.get_setting_by_key(SettingsBase.KEY_APP_PORT)

