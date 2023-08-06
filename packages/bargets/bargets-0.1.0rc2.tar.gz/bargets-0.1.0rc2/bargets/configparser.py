"""For parsing widgets' config file."""

import pathlib

import ruamel.yaml


class Config:
    """For preparing other ConfigParser classes."""

    def __init__(self) -> None:
        """Set up common values."""
        self._config: object = None
        self._yaml: object = ruamel.yaml.YAML()
        self._path: str = str(
            pathlib.Path("~/.config/bargets/bargets.yaml").expanduser()
        )

    def _load(self) -> None:
        """Load config file (if such exists)."""
        if pathlib.Path(self._path).exists():
            with open(self._path, "r") as f:
                try:
                    self._config = self._yaml.load(f)
                except ruamel.yaml.parser.ParserError:
                    pass


class BatteryConfig:
    """
    Settings that BatteryConfigParser will initialize based on
    settings provided in bargets.yaml.
    """

    def __init__(self) -> None:
        """Set up valid options battery widget accepts."""
        self._settings: dict = dict()
        self._suspend: bool = False
        self._thresholds: dict = dict()
        self._symbols: dict = dict()
        self._indicator: str = ""
        self._subject: dict[str, str] = {"low": "", "full": ""}
        self._body: dict[str, str] = {"low": "", "full": ""}

    @property
    def suspend(self) -> bool:
        """Get suspend, if such is set in bargets.yaml."""
        return self._suspend

    @property
    def threshold_full(self) -> int:
        """Get threshold.full, if such is set in bargets.yaml."""
        return 0 if "full" not in self._thresholds else self._thresholds["full"]

    @property
    def threshold_low(self) -> int:
        """Get threshold.low, if such is set in bargets.yaml."""
        return 0 if "low" not in self._thresholds else self._thresholds["low"]

    @property
    def threshold_critical(self) -> int:
        """Get threshold.critical, if such is set in bargets.yaml."""
        return 0 if "critical" not in self._thresholds else self._thresholds["critical"]

    @property
    def symbol(self) -> dict:
        """Get symbols, if such are set in bargets.yaml."""
        return self._symbols

    @property
    def indicator(self) -> str:
        """Get indicator, if such is set in bargets.yaml."""
        return self._indicator

    @property
    def subject_low(self) -> str:
        """Get subject.low, if such is set in bargets.yaml."""
        return self._subject["low"]

    @property
    def body_low(self) -> str:
        """Get body.low, if such is set in bargets.yaml."""
        return self._body["low"]

    @property
    def subject_full(self) -> str:
        """Get subject.full, if such is set in bargets.yaml."""
        return self._subject["full"]

    @property
    def body_full(self) -> str:
        """Get body.full, if such is set in bargets.yaml."""
        return self._body["full"]


class BatteryConfigParser(Config, BatteryConfig):
    """For parsing battery widget's config options in bargets.yaml."""

    def __init__(self) -> None:
        """Prepare for parsing battery widget's config."""
        Config.__init__(self)
        BatteryConfig.__init__(self)
        Config._load(self)
        self._set_settings()

    def _set_settings(self) -> None:
        """Initialize settings."""
        opts: list = []
        if self._config:
            opts = [s for k, s in self._config.items() if k == "battery"]
        if opts and len(opts) > 1:
            raise ValueError("bargets.yaml must contain only one 'battery' section")
        if opts and isinstance(opts[0], ruamel.yaml.comments.CommentedMap):
            self._settings = {k: v for k, v in opts[0].items()}

    def _parse_suspend(self) -> None:
        """Evaluate suspend option in bargets.yaml."""
        if "suspend" in self._settings:
            if not isinstance(self._settings.get("suspend"), bool):
                raise ValueError("Suspend must be a boolean")
            self._suspend = self._settings.get("suspend")

    def _parse_threshold_full(self) -> None:
        """Evaluate threshold.full option in bargets.yaml."""
        if "threshold.full" in self._settings:
            if not isinstance(self._settings.get("threshold.full"), int):
                raise ValueError("Threshold must be an integer")
            if 90 > self._settings.get("threshold.full") > 100:
                raise ValueError("Threshold must be > 90 and <= 100")
            self._thresholds["full"] = self._settings.get("threshold.full")

    def _parse_threshold_low(self) -> None:
        """Evaluate threshold.low option in bargets.yaml."""
        if "threshold.low" in self._settings:
            if not isinstance(self._settings.get("threshold.low"), int):
                raise ValueError("Threshold must be an integer")
            if self._settings.get("threshold.low") <= 0:
                raise ValueError("Threshold must be > 0")
            self._thresholds["low"] = self._settings.get("threshold.low")

    def _parse_threshold_critical(self) -> None:
        """Evaluate threshold.critical option in bargets.yaml."""
        if "threshold.critical" in self._settings:
            if not isinstance(self._settings.get("threshold.critical"), int):
                raise ValueError("Threshold must be an integer")
            if self._settings.get("threshold.critical") <= 0:
                raise ValueError("Threshold must be > 0")
            self._thresholds["critical"] = self._settings.get("threshold.critical")

    def _parse_symbol_charging(self) -> None:
        """Evaluate symbol.charging option in bargets.yaml."""
        if "symbol.charging" in self._settings:
            if not isinstance(self._settings.get("symbol.charging"), str):
                raise ValueError("Symbol must be a string")
            self._symbols["charging"] = self._settings.get("symbol.charging")

    def _parse_symbol_discharging(self) -> None:
        """Evaluate symbol.discharging option in bargets.yaml."""
        if "symbol.discharging" in self._settings:
            if not isinstance(self._settings.get("symbol.discharging"), str):
                raise ValueError("Symbol must be a string")
            self._symbols["discharging"] = self._settings.get("symbol.discharging")

    def _parse_indicator(self) -> None:
        """Evaluate indicator option in bargets.yaml."""
        if "indicator" in self._settings:
            if not isinstance(self._settings.get("indicator"), str):
                raise ValueError("Indicator must be a string")
            self._indicator = self._settings.get("indicator")

    def _parse_subject_low(self) -> None:
        """Evaluate subject.low in bargets.yaml."""
        if "subject.low" in self._settings:
            if not isinstance(self._settings.get("subject.low"), str):
                raise ValueError("Notification subject must be a string")
            self._subject["low"] = self._settings.get("subject.low")

    def _parse_body_low(self) -> None:
        """Evaluate body.low in bargets.yaml."""
        if "body.low" in self._settings:
            if not isinstance(self._settings.get("body.low"), str):
                raise ValueError("Notification body must be a string")
            self._body["low"] = self._settings.get("body.low")

    def _parse_subject_full(self) -> None:
        """Evaluate subject.full in bargets.yaml."""
        if "subject.full" in self._settings:
            if not isinstance(self._settings.get("subject.full"), str):
                raise ValueError("Notification subject must be a string")
            self._subject["full"] = self._settings.get("subject.full")

    def _parse_body_full(self) -> None:
        """Evaluate body.full in bargets.yaml."""
        if "body.full" in self._settings:
            if not isinstance(self._settings.get("body.full"), str):
                raise ValueError("Notification body must be a string")
            self._body["full"] = self._settings.get("body.full")

    def parse(self) -> None:
        """Evaluate all options."""
        self._parse_suspend()
        self._parse_threshold_full()
        self._parse_threshold_low()
        self._parse_threshold_critical()
        self._parse_symbol_charging()
        self._parse_symbol_discharging()
        self._parse_indicator()
        self._parse_subject_low()
        self._parse_body_low()
        self._parse_subject_full()
        self._parse_body_full()


class CPUConfig:
    """
    Settings that CPUConfigParser will initialize based on
    settings provided in bargets.yaml.
    """

    def __init__(self) -> None:
        """Set up valid options cpu widget accepts."""
        self._settings: dict = dict()
        self._indicator: str = ""
        self._unit: str = ""
        self._prefix: str = ""
        self._suffix: str = ""

    @property
    def indicator(self) -> str:
        """Get indicator, if such is set in bargets.yaml."""
        return self._indicator

    @property
    def unit(self) -> str:
        """Get unit, if such is set in bargets.yaml."""
        return self._unit

    @property
    def prefix(self) -> str:
        """Get prefix, is such is set in bargets.yaml."""
        return self._prefix

    @property
    def suffix(self) -> str:
        """Get suffix, is such is set in bargets.yaml."""
        return self._suffix


class CPUConfigParser(Config, CPUConfig):
    """For parsing cpu widget's config options in bargets.yaml."""

    def __init__(self) -> None:
        """Prepare for parsing cpu widget's config."""
        Config.__init__(self)
        CPUConfig.__init__(self)
        Config._load(self)
        self._set_settings()

    def _set_settings(self) -> None:
        """Initialize settings."""
        opts: list = []
        if self._config:
            opts = [s for k, s in self._config.items() if k == "cpu"]
        if opts and len(opts) > 1:
            raise ValueError("bargets.yaml must contain only one 'cpu' section")
        if opts and isinstance(opts[0], ruamel.yaml.comments.CommentedMap):
            self._settings = {k: v for k, v in opts[0].items()}

    def _parse_indicator(self) -> None:
        """Evaluate indicator option in bargets.yaml."""
        if "indicator" in self._settings:
            if not isinstance(self._settings.get("indicator"), str):
                raise ValueError("Indicator must be a string")
            self._indicator = self._settings.get("indicator")

    def _parse_unit(self) -> None:
        """Evaluate unit option in bargets.yaml."""
        if "unit" in self._settings:
            if self._settings.get("unit") not in {"celcius", "fahrenheit"}:
                raise ValueError("Unit must be either celcius or fahrenheit")
            self._unit = self._settings.get("unit")

    def _parse_prefix(self) -> None:
        """Evaluate prefix option in bargets.yaml."""
        if "prefix" in self._settings:
            if not isinstance(self._settings.get("prefix"), str):
                raise ValueError("Prefix must be a string")
            self._prefix = self._settings.get("prefix")

    def _parse_suffix(self) -> None:
        """Evaluate suffix option in bargets.yaml."""
        if "suffix" in self._settings:
            if not isinstance(self._settings.get("suffix"), str):
                raise ValueError("Suffix must be a string")
            self._suffix = self._settings.get("suffix")

    def parse(self) -> None:
        """Evaluate all options."""
        self._parse_indicator()
        self._parse_unit()
        self._parse_prefix()
        self._parse_suffix()
