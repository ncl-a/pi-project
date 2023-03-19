from lib.utils.base import Base
import json
from lib.file.file_manager import FileManger


class SettingsManager(Base):
    create_settings_file_if_not_exist = True

    def __init__(self):
        super().__init__()

        self.settings: dict = self.base_settings  # set base settings

        try:
            self.override_settings()

        except IOError as io_error:
            print(f"Configuration file {self.settings_file_name} not found")

            if SettingsManager.create_settings_file_if_not_exist:
                self.create_settings_file()
                self.override_settings()

        except json.JSONDecodeError as json_decode_error:
            print(f"Configuration file {self.settings_file_name} JSON syntax error")
            Base.exit()


    def override_settings(self) -> None:
        """
        Override project settings with settings configuration file
        """

        self.settings.update(FileManger.read_json(self.settings_path))

    def create_settings_file(self) -> None:
        """
        Create settings file if it does not exist with base settings
        """

        FileManger.write_json(self.settings_path, self.base_settings)

    def set(self, key: str, value: str) -> None:
        """
        Modify settings

        :param key: settings' key
        :param value: key's value

        :rtype: None
        """
        self.settings[key] = value

    def get(self, key: str) -> str:
        """
        Return the value of key passed

        :param key: A key of settings
        :type key: str

        :rtype: str
        """

        return self.settings[key]
