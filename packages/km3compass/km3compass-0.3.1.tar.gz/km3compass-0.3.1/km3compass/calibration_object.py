#!/usr/bin/env python3
import numpy as np


class calibration_object:
    """
    Object to store calibration within km3compass
    """

    def __init__(self, **kwargs):
        self._compass_SN = 0
        self._type = "default"
        self._source = "new"

        # Accelerometer related values
        self._A_norm = 1.0
        self._A_offsets = np.ones(3)
        self._A_rot = np.identity(3)

        # Compass related values
        self._H_norm = 1.0
        self._H_offsets = np.ones(3)
        self._H_rot = np.identity(3)

        # Gyroscope related values
        self._G_norm = 1.0
        self._G_offsets = np.ones(3)
        self._G_rot = np.identity(3)

        self._parent = None

        for key, item in kwargs.items():
            self.set(key, item)

    def set(self, key, value):
        if not hasattr(self, f"_{key}"):
            raise Exception(
                f'Try to set property "{key}" to calibration, which doesn\'t exist !'
            )
        setattr(self, f"_{key}", value)

    def get(self, key):
        if not hasattr(self, f"_{key}"):
            raise Exception(
                f'Try to sget property "{key}" from calibration, which doesn\'t exist !'
            )
        return getattr(self, f"_{key}")

    def __str__(self):
        """Produce str summary of calibration object"""
        output = "-" * 40 + "\n"
        output += f"Calibration for compass {self._compass_SN}\n"
        output += f'Type: "{self._type}", source: "{self._source}"\n'
        output += f"A norm = {self._A_norm}\n"
        output += f"A xyz offsets = {self._A_offsets}\n"
        output += f"A rotation matrix = \n{self._A_rot}\n"
        output += f"H norm = {self._H_norm}\n"
        output += f"H xyz offsets = {self._H_offsets}\n"
        output += f"H rotation matrix = \n{self._H_rot}\n"
        output += "-" * 40
        return output
