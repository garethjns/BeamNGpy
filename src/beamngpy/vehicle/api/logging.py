from __future__ import annotations

from .base import VehicleApi


class LoggingApi(VehicleApi):
    def set_in_game_logging_options_from_json(self, file_name: str) -> None:
        """
        Updates the in game logging with the settings specified
        in the given file/json. The file is expected to be in
        the following location:
        <userpath>/<version_number>/<file_name>

        Args:
            file_name
        """
        data = dict(type='ApplyVSLSettingsFromJSON', fileName=file_name)
        self.send(data).ack('AppliedVSLSettings')

    def write_in_game_logging_options_to_json(self, file_name: str = 'template.json') -> None:
        """
        Writes all available options from the in-game-logger to a json file.
        The purpose of this functionality is to facilitate the acquisition of
        a valid template to adjust the options/settings of the in game logging
        as needed.
        Depending on the executable used the file can be found at the following
        location:
        <userpath>/<BeamNG version number>/<fileName>

        Args:
            file_name: not the absolute file path but the name of the json
        """
        data = dict(type='WriteVSLSettingsToJSON', fileName=file_name)
        self.send(data).ack('WroteVSLSettingsToJSON')

    def start_in_game_logging(self, output_dir: str) -> None:
        """
        Starts in game logging. Beware that any data
        from previous logging sessions is overwritten
        in the process.

        Args:
            output_dir: to avoid overwriting logging from other vehicles,
                        specify the output directory, overwrites the
                        output_dir set through the json. The data can be
                        found in: <userpath>/<BeamNG version number>/<output_dir>
        """
        data = dict(type='StartVSLLogging', outputDir=output_dir)
        self.send(data).ack('StartedVSLLogging')
        log_msg = ('Started in game logging.'
                   'The output for the vehicle stats logging can be found in '
                   f'userfolder/<BeamNG version number>/{output_dir}.')
        self.logger.info(log_msg)

    def stop_in_game_logging(self) -> None:
        """
        Stops in game logging.
        """
        data = dict(type='StopVSLLogging')
        self.send(data).ack('StoppedVSLLogging')
        self.logger.info('Stopped in game logging.')
