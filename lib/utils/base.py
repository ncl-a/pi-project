import os
import pathlib
import sys


class Base:

    def __init__(self):
        pass

    @staticmethod
    def exit():
        print("Exit...")
        sys.exit()

    @property
    def settings_file_name(self) -> str:
        """
        Return the settings file name

        :rtype: str
        """

        return "settings.json"

    @property
    def base_directory(self) -> str:
        """
        Return the base directory path

        :rtype: str
        """

        this_file_path = os.path.abspath(__file__)
        path = pathlib.Path(this_file_path)
        project_path = path.parent.parent.parent.absolute()

        return str(project_path)

    @property
    def settings_path(self) -> str:
        """
        Return the settings path of the project

        :rtype: str
        """

        return os.path.join(self.base_directory, self.settings_file_name)

    @property
    def setting_db_name(self):
        """
        Return the db name property name

        :rtype: str
        """

        return "db_name"

    @property
    def base_db_name(self) -> str:
        """
        Return the base db name

        :rtype: str
        """

        return "database.db"

    @property
    def setting_project_path(self) -> str:
        """
        Return project path (to manage) property name

        :rtype: str
        """

        return "path"

    @property
    def base_settings(self) -> dict:
        """
        Return base settings

        :rtype: dict
        """

        return {
            self.setting_db_name: self.base_db_name
        }
