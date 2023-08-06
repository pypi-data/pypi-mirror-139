"""Display cpu temperature."""

__program__: str = "bargets-cpu"
__author__: str = "Niklas Larsson"
__credits__: list = ["Niklas Larsson"]
__license__: str = "MIT"
__maintainer__: str = "Niklas Larsson"
__status__: str = "Alpha"

import logging
import pathlib
import subprocess

import ruamel.yaml

from bargets import configparser


class CPUTemperature:
    """Represents the CPU temperatures."""

    def __init__(self) -> None:
        """Set up cpu data."""
        self._unit: str = "celcius"
        self._temp: str = ""
        self._indicator: str = "°C"
        self._prefix: str = ""
        self._suffix: str = ""
        self._set_temperature()

    def _set_temperature(self) -> None:
        """Set temperature reading, if possible."""
        try:
            cmd: list = ["sensors"]
            data: object = subprocess.run(cmd, capture_output=True, text=True)
            text: list = []
            for row in data.stdout.split("\n"):
                if row.startswith("CPU"):
                    text = row.split()
                    break
            for field in text:
                if "°C" in field:
                    self._temp = field.replace("+", "").replace("°C", "")
                    break
                elif "°F" in field:
                    self._temp = field.replace("+", "").replace("°F", "")
                    break
        except FileNotFoundError:
            self._temp = "N/A"
            self._indicator = ""

    @property
    def suffix(self) -> str:
        """Get suffix that is displayed after temperature reading."""
        return self._suffix

    @suffix.setter
    def suffix(self, value: str) -> str:
        """Set suffix."""
        if not isinstance(value, str):
            raise ValueError("Suffix has to be of type str")
        self._suffix = value

    @property
    def prefix(self) -> str:
        """Get prefix that is displayed before cpu temperature reading."""
        return self._prefix

    @prefix.setter
    def prefix(self, value: str) -> None:
        """Set prefix."""
        if not isinstance(value, str):
            raise ValueError("Prefix has to be a string")
        self._prefix = value

    @property
    def indicator(self) -> str:
        """Get indicator that is used next to temperature."""
        return self._indicator

    @indicator.setter
    def indicator(self, value: str) -> None:
        """Set indicator."""
        if not isinstance(value, str):
            raise ValueError("Symbol has to be of type str")
        self._indicator = value

    @property
    def temp(self) -> str:
        """Get cpu temperature."""
        if self._temp:
            if self._temp == "N/A":
                return self._temp
            # Due to floating point errors, round temp with 1 decimal precision
            return str(round(float(self._temp), 1))

    @property
    def unit(self) -> str:
        """Get temperature measurement unit."""
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        """Set temperature measurement unit. Convert temp if necessary."""

        if value not in {"fahrenheit", "celcius"}:
            raise ValueError("Unit can be either celcius of fahrenheit")

        if self._unit == "celcius" and value == "fahrenheit":
            self._unit = value
            self._indicator = "°F"
            self._temp = str(float((float(self._temp) * 1.8) + 32))

        if self._unit == "fahrenheit" and value == "celcius":
            self._unit = value
            self._indicator = "°C"
            self._temp = str(float((float(self._temp) -32) / 1.8))


def main() -> None:
    """Main function."""

    cpu: object = CPUTemperature()
    config: CPUConfigParser = configparser.CPUConfigParser()
    config.parse()

    # Parse config (if such exists) and set widget's looks
    if config.indicator:
        cpu.indicator = config.indicator
    if config.unit:
        cpu.unit = config.unit
    if config.prefix:
        cpu.prefix = config.prefix
    if config.suffix:
        cpu.suffix = config.suffix

    # Display cpu temperature
    print(f"{cpu.prefix}{cpu.temp}{cpu.indicator}{cpu.suffix}")


if __name__ == "__main__":
    main()
