from __future__ import annotations

from beamngpy.types import StrDict

from .base import Api


class SettingsApi(Api):
    def change_setting(self, key: str, value: str) -> None:
        """
        Changes a setting in the game. Examples of the key and value pairs
        given to this method can be found in your game's settings ini files.
        These are usually in <userpath>/settings/game-settings.ini or
        <userpath>/settings/cloud/game-settings-cloud.ini.

        Args:
            key: The key of the setting that is to be changed
            value: The desired value.
        """
        data = dict(type='ChangeSetting')
        data['key'] = key
        data['value'] = value
        return self._send(data).ack('SettingsChanged')

    def apply_graphics_setting(self) -> None:
        """
        Makes the game apply a graphics setting that has been changed since
        startup or the last time settings were applied. A call to this is
        required after changing settings like whether or not the game is
        in fullscreen or the resolution, otherwise those settings will only
        take effect after the next launch.
        """
        data = dict(type='ApplyGraphicsSetting')
        self._send(data).ack('GraphicsSettingApplied')

    def set_deterministic(self) -> None:
        """
        Sets the simulator to run in deterministic mode. For this to function
        properly, an amount of steps per second needs to have been specified
        in the simulator's settings, or through
        :meth:`~.BeamnGpy.set_steps_per_second`.
        """
        data = dict(type='SetPhysicsDeterministic')
        self._send(data).ack('SetPhysicsDeterministic')

    def set_nondeterministic(self) -> None:
        """
        Disables the deterministic mode of the simulator. Any steps per second
        setting is retained.
        """
        data = dict(type='SetPhysicsNonDeterministic')
        self._send(data).ack('SetPhysicsNonDeterministic')

    def set_steps_per_second(self, sps: int) -> None:
        """
        Specifies the temporal resolution of the simulation. The setting can be
        understood to determine into how many steps the simulation divides one
        second of simulation. A setting of two, for example, would mean one
        second is simulated in two steps. Conversely, to simulate one second,
        one needs to advance the simulation two steps.

        Args:
            sps (int): The steps per second to set.
        """
        data = dict(type='FPSLimit', fps=sps)
        self._send(data).ack('SetFPSLimit')

    def remove_step_limit(self) -> None:
        """
        Removes the steps-per-second setting, making the simulation run at
        undefined time slices.
        """
        data = dict(type='RemoveFPSLimit')
        self._send(data).ack('RemovedFPSLimit')

    def set_particles_enabled(self, enabled: bool) -> None:
        """
        Enable / disable visual particle emission.

        Args:
            enabled: Whether to enable or disable effects.
        """
        data: StrDict = dict(type='ParticlesEnabled')
        data['enabled'] = enabled
        self._send(data).ack('ParticlesSet')
