"""Display laptop battery charge and state."""

__program__: str = "bargets-battery"
__author__: str = "Niklas Larsson"
__credits__: list = ["Niklas Larsson"]
__license__: str = "MIT"
__maintainer__: str = "Niklas Larsson"
__status__: str = "Alpha"

import logging
import os
import pathlib
import sys
import subprocess

import ruamel.yaml

from bargets import configparser


class Acpi:
    """For fetching the quantity of batteries connected to laptop."""

    def __init__(self) -> None:
        self._batteries: int = 0
        cmd: list = ["acpi", "-b"]
        data: object = subprocess.run(cmd, capture_output=True, text=True)
        for _ in data.stdout.split("\n"):
            if _.startswith("Battery"):
                self._batteries += 1

    @property
    def batteries(self) -> int:
        """Get the number of batteries."""
        return self._batteries


class Battery:
    """Represents a battery."""

    def __init__(self, index: int) -> None:
        """
        Set up a battery.

        Parameters:
            index.... Basically, the row number from `acpi -b`s output.
            i.e. if [index] is 1, then the first row is selected.
        """

        if not isinstance(index, int):
            raise ValueError("Index must be of type int")

        self._index: str = index
        self._suspend: bool = True
        self._indicator: str = "%"
        self._state: str = ""
        self._charge: str = ""
        self._charges: dict[str, bool] = {"low": False, "critical": False}

        self._thresholds: dict[str, int] = {
            "full": 99,
            "low": 5,
            "critical": 3
        }

        self._symbols: dict[str, str] = {
            "charging": "↑",
            "discharging": "↓"
        }

        try:
            cmd: list = ["acpi", "-b"]
            info: object = subprocess.run(cmd, capture_output=True, text=True)
            self._set_state(info)
            self._set_charge(info)
        except FileNotFoundError:
            self._state = "N/A"
            self._charge = "N/A"
            self._indicator = ""
            self._symbols["charging"] = ""
            self._symbols["discharging"] = ""

    def _set_state(self, info: object) -> None:
        """Initialize and set battery state, reading it from `acpi -b`."""
        for idx, line in enumerate(info.stdout.split("\n"), 1):
            if line.startswith("Battery"):
                if idx == self._index:
                    line = line.lower()
                    data: list = line.split()
                    if "not charging" in line:
                        self._state = " ".join(data[2:4]).replace(",", "")
                    elif "discharging" in line or "charging" in line:
                        self._state = data[2].replace(",", "")
                    del data, line
                    break

    def _set_charge(self, info: object) -> None:
        """Initialize and set battery charge, reading it from `acpi -b`."""
        for idx, line in enumerate(info.stdout.split("\n"), 1):
            if line.startswith("Battery"):
                if idx == self._index:
                    line = line.lower()
                    data: list = line.split()
                    if "not charging" in line:
                        self._charge = data[4].replace(",", "").replace("%", "")
                    elif "discharging" in line or "charging" in line:
                        self._charge = data[3].replace(",", "").replace("%", "")
                    del data, line
                    break

    @property
    def indicator(self) -> str:
        """Get indicator."""
        return self._indicator

    @indicator.setter
    def indicator(self, value: str) -> None:
        """Set indicator."""
        if not isinstance(value, str):
            raise ValueError("Indicator has to be of type str")
        self._indicator = value

    @property
    def suspend(self) -> bool:
        """Get if suspend mode is on."""
        return self._suspend

    @suspend.setter
    def suspend(self, value: bool) -> None:
        """Set suspend mode."""
        if value not in {True, False}:
            raise ValueError("Suspend can be either True or False")
        self._suspend = value

    @property
    def charge(self) -> str:
        """Get battery's charge."""
        return self._charge

    @property
    def full(self) -> bool:
        """Check if battery is fully charged."""
        if self._charge:
            if self._charge in {"N/A"}:
                return False
            if int(self._charge) >= self._thresholds["full"]:
                return True

        return False

    @full.setter
    def full(self, value: int) -> None:
        """Set what the threshold for 'full' is."""
        if not isinstance(value, int):
            raise ValueError("Threshold for 'full' has to be of type integer")
        if 90 > value > 100:
            raise ValueError("Threshold for 'full' has to be > 90 and < 100")
        self._thresholds["full"] = value

    @property
    def low(self) -> bool:
        """Check if battery charge is low."""
        if self._charge:
            if self._charge in {"N/A"}:
                return False
            if int(self._charge) >= 0:
                return int(self._charge) <= self._thresholds["low"]

        return False

    @low.setter
    def low(self, value: int) -> None:
        """Set what the threshold for 'low' is."""
        if not isinstance(value, int):
            raise ValueError("Threshold for 'low' has to be of type integer")
        if value <= 0:
            raise ValueError("Threshold for 'low' has to be greater than zero")
        self._thresholds["low"] = value

    @property
    def critical(self) -> bool:
        """Check if battery charge is critically low."""
        if self._charge:
            if self._charge in {"N/A"}:
                return False
            if int(self._charge) >= 0:
                return int(self._charge) <= self._thresholds["critical"]

        return False

    @critical.setter
    def critical(self, value: int) -> None:
        """Set what the threshold for 'critical' is."""
        if not isinstance(value, int):
            raise ValueError("Threshold for 'critical' has to be of type int")
        if value <= 0:
            raise ValueError("Threshold for 'critical' has to be greater than zero")
        self._thresholds["critical"] = value

    @property
    def charging(self) -> bool:
        """Check if battery is charging."""
        if self._state in {"charging", "discharging", "not charging"}:
            return self._state == "charging"
        return False

    @property
    def symbol(self) -> str:
        """Get a symbol corresponding to battery's state."""
        if self._state in {"charging", "discharging"}:
            if self.charging:
                return self._symbols["charging"]
            return self._symbols["discharging"]
        return ""

    @symbol.setter
    def symbol(self, values: dict) -> None:
        """Set new symbol indicators for charge and discharge states."""
        if not isinstance(values, dict):
            raise ValueError("Symbols must be provided in form of dict")
        if "charging" in values:
            if not isinstance(values.get("charging"), str):
                raise ValueError("Symbol must be a string")
            self._symbols["charging"] = values.get("charging")
        if "discharging" in values:
            if not isinstance(values.get("discharging"), str):
                raise ValueError("Symbol must be a string")
            self._symbols["discharging"] = values.get("discharging")


class Notification:
    """For setting up other Notification classes."""

    def __init__(self, language: str) -> None:
        """Set up language to display notifications in."""
        self._language: str = language


class FullBatteryNotification(Notification):
    """Notifications that nag about full battery."""

    def __init__(self, language: str) -> None:
        super().__init__(language)
        self._pending: int = 0
        self._notif_server: bool = True
        self._set_pending()
        self._subject: str = self._set_subject()
        self._body: str = self._set_body()

    def _set_pending(self) -> None:
        """Set the status of pending, i.e. the number of pending messages."""
        try:
            cmd: list = ["dunstctl", "count", "displayed"]
            data: object = subprocess.run(cmd, capture_output=True, text=True)
            self._pending = int(data.stdout.split("\n")[0])
        except FileNotFoundError:
            self._notif_server = False

    def _set_subject(self) -> str:
        """Initialize notification subject."""

        subject: dict[str, str] = {
            "fi_FI.UTF-8": "Akku",
            "en_US.UTF-8": "Battery",
        }

        return subject.get(self._language, subject.get("en_US.UTF-8"))

    def _set_body(self) -> str:
        """Initialize notification body."""

        body: dict[str, str] = {
            "fi_FI.UTF-8": "Akku on ladattu täyteen!",
            "en_US.UTF-8": "Battery fully charged!",
        }

        return body.get(self._language, body.get("en_US.UTF-8"))

    def display(self) -> None:
        """Notify about full battery."""
        if self._notif_server:
            cmd: list[str] = ["notify-send"]
            if self._subject:
                cmd.append(self._subject)
            if self._body:
                cmd.append(self._body)
            subprocess.run(cmd)

    def close(self) -> None:
        """Close all the notifications."""
        if self._notif_server:
            subprocess.run(["dunstctl", "close"])

    @property
    def subject(self) -> str:
        """Get notification subject."""
        return self._subject

    @subject.setter
    def subject(self, value: str) -> None:
        """Set new notification subject."""
        if not isinstance(value, str):
            raise ValueError("Subject has to be a string")
        self._subject = value

    @property
    def body(self) -> str:
        """Get notification body."""
        return self._body

    @body.setter
    def body(self, value: str) -> None:
        """Set new notification body."""
        if not isinstance(value, str):
            raise ValueError("Body has to be a string")
        self._body = value

    @property
    def pending(self) -> bool:
        """Check if any pending notifications exist."""
        return self._pending > 0


class LowBatteryNotification(Notification):
    """For notifications that nag about low battery."""

    def __init__(self, language: str) -> None:
        super().__init__(language)
        self._pending: int = 0
        self._notif_server: bool = True
        self._set_pending()
        self._subject: str = self._set_subject()
        self._body: str = self._set_body()

    def _set_pending(self) -> None:
        """Set the status of pending, i.e. the number of pending messages."""
        try:
            cmd: list = ["dunstctl", "count", "displayed"]
            data: object = subprocess.run(cmd, capture_output=True, text=True)
            self._pending = int(data.stdout.split("\n")[0])
        except FileNotFoundError:
            self._notif_server = False

    def _set_subject(self) -> str:
        """Initialize notification subject."""

        subject: dict[str, str] = {
            "fi_FI.UTF-8": "Akku",
            "en_US.UTF-8": "Battery",
        }

        return subject.get(self._language, subject.get("en_US.UTF-8"))

    def _set_body(self) -> str:
        """Initialize notification body."""

        body: dict[str, str] = {
            "fi_FI.UTF-8": "Akun taso matala!",
            "en_US.UTF-8": "Battery charge low!",
        }

        return body.get(self._language, body.get("en_US.UTF-8"))

    @property
    def subject(self) -> str:
        """Get notification subject."""
        return self._subject

    @subject.setter
    def subject(self, value: str) -> None:
        """Set new notification subject."""
        if not isinstance(value, str):
            raise ValueError("Subject has to be a string")
        self._subject = value

    @property
    def body(self) -> str:
        """Get notification body."""
        return self._body

    @body.setter
    def body(self, value: str) -> None:
        """Set new notification body."""
        if not isinstance(value, str):
            raise ValueError("Body has to be a string")
        self._body = value

    def display(self) -> None:
        """Notify about low battery."""
        if self._notif_server:
            cmd: list[str] = ["notify-send", "--urgency", "critical"]
            if self._subject:
                cmd.append(self._subject)
            if self._body:
                cmd.append(self._body)
            subprocess.run(cmd)

    def close(self) -> None:
        """Close all notifications."""
        if self._notif_server:
            subprocess.run(["dunstctl", "close"])

    @property
    def pending(self) -> bool:
        """Check if any pending notifications exist."""
        return self._pending > 0


def main() -> None:
    """Main function."""

    language: str = os.environ["LANG"]
    notifications: dict[str, Notification] = {
        "battery_low": LowBatteryNotification(language),
        "battery_full": FullBatteryNotification(language)
    }

    # Automatically determine the number of batteries
    acpi: Acpi = Acpi()
    batteries: list[Battery] = [Battery(b) for b in range(1, acpi.batteries + 1)]

    # Parse config file (if such exists)
    config: BatteryConfigParser = configparser.BatteryConfigParser()
    config.parse()

    # If notifications are configured in config file, use those values
    if config.subject_low:
        notifications["battery_low"].subject = config.subject_low
    if config.body_low:
        notifications["battery_low"].body = config.body_low
    if config.subject_full:
        notifications["battery_full"].subject = config.subject_full
    if config.body_full:
        notifications["battery_full"].body = config.body_full

    # If other battery settings are configured in config file, use those values
    for battery in batteries:
        if config.suspend:
            battery.suspend = config.suspend
        if config.threshold_full:
            battery.full = config.threshold_full
        if config.threshold_low:
            battery.low = config.threshold_low
        if config.threshold_critical:
            battery.critical = config.threshold_critical
        if config.symbol:
            battery.symbol = config.symbol
        if config.indicator:
            battery.indicator = config.indicator

    # Display battery data
    for idx, i in enumerate(batteries):
        if 0 < idx < len(batteries):
            print(" ", end="")
        print(f"{i.symbol}{i.charge}{i.indicator}", end="")
    print()

    # Display warning notification if the last battery that
    # still has juice left, is running on low charge
    if not any([battery.charging for battery in batteries]):
        # Suspend system if the last (or in this case, the "first")
        # battery is running on critically low charge. I'm not sure
        # in what order batteries are usually used, but it seems that
        # at least on my Thinkpad X240 (has internal battery + external
        # one) the inner battery is used first (I guess?), and then the
        # outer one.
        if batteries[0].critical and batteries[0].suspend:
            subprocess.run(["dunstctl", "set-paused", "true"])
            subprocess.run(["systemctl", "suspend"])
        if batteries[0].low:
            if not notifications["battery_low"].pending:
                notifications["battery_low"].display()
                sys.exit(0)

    # Display notification when battery is fully charged
    if any([battery.charging for battery in batteries]):
        if notifications["battery_low"].pending:
            notifications["battery_low"].close()
        if all([battery.full for battery in batteries]):
            if not notifications["battery_full"].pending:
                notifications["battery_full"].display()
                sys.exit(0)


if __name__ == "__main__":
    main()
