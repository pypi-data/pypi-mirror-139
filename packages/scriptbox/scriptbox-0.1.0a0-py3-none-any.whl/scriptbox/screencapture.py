"""Take a screenshot of the current screen."""

__program__: str = "screencapture"
__author__: str = "Niklas Larsson"
__license__: str = "MIT"
__credits__: list = ["Niklas Larsson"]
__maintainer__: str = "Niklas Larsson"

import os
import datetime
import subprocess
import pathlib
import time


class Screenshot:
    """For capturing screenshots."""

    def __init__(self, language: str, fmt: str) -> None:
        self._lng: str = language
        self._fmt: str = fmt
        self._dst: str = self._save(self._lng)
        self._id: str = self._identifier(self._lng)

    @property
    def photo_fmt(self) -> str:
        """Get format screenshots are saved as."""
        return self._fmt

    @photo_fmt.setter
    def photo_fmt(self, value: str) -> None:
        """Set new photo format."""
        raise NotImplementedError("Method not implemented yet")

    @property
    def save_to(self) -> str:
        """Get where to save screenshots."""
        return self._dst

    @save_to.setter
    def save_to(self, value: str) -> None:
        """Set where to save screenshots."""
        raise NotImplementedError("Method not implemented yet")

    @property
    def photo_id(self) -> str:
        """Get what identifier to use in screenshot name."""
        return self._id

    @photo_id.setter
    def photo_id(self, value: str) -> None:
        """Set new identifier."""
        raise NotImplementedError("Method not implemented yet")

    def _save(self, language: str) -> str:
        """Determine where to save screenshots."""

        dst: dict[str, str] = {
            "fi_FI.UTF-8": str(pathlib.Path.home()) + "/Kuvat/Näytönkaappaukset",
            "en_US.UTF-8": str(pathlib.Path.home()) + "/Pictures/Screenshots",
        }

        return dst.get(language, dst.get("en_US.UTF-8"))

    def _identifier(self, language: str) -> str:
        """Determine identifier to use in photo name."""

        identifier: dict[str, str] = {
            "fi_FI.UTF-8": "näytönkaappaus",
            "en_US.UTF-8": "screenshot",
        }

        return identifier.get(language, identifier.get("en_US.UTF-8"))

    def _name(self) -> str:
        """Name a screenshot."""
        pathlib.Path(self._dst).mkdir(parents=True, exist_ok=True)
        date: str = datetime.datetime.now().strftime("[%H:%M:%S] [%-d-%-m-%Y]")
        filename: str = f"{date} {self._id}.{self._fmt}"
        path: str = str(pathlib.PurePath(self._dst, filename))
        return path

    def capture(self) -> None:
        """Take a screenshot."""
        cmd: list = ["import", "-window", "root", self._name()]
        try:
            subprocess.run(cmd)
        except FileNotFoundError:
            pass


class ScreenshotNotification:
    """Notification shown after taking screenshot."""

    def __init__(self, language: str) -> None:
        self._lng: str = language
        self._sub: str = self._subject(self._lng)
        self._bdy: str = self._body(self._lng)
        self._cmd: list = ["notify-send", self._sub, self._bdy]

    @property
    def subject(self) -> str:
        """Get notification subject / heading."""
        return self._sub

    @subject.setter
    def subject(self, value: str) -> None:
        """Set new subject / heading."""
        raise NotImplementedError("Method not implemented yet")

    @property
    def body(self) -> str:
        """Get notification body."""
        return self._bdy

    @body.setter
    def body(self, value: str) -> None:
        """Set new body."""
        raise NotImplementedError("Method not implemented yet")

    def _subject(self, language: str) -> str:
        """Determine notification subject."""

        subject: dict[str, str] = {
            "fi_FI.UTF-8": "Näytönkaappaus",
            "en_US.UTF-8": "Screenshot",
        }

        return subject.get(language, subject.get("en_US.UTF-8"))

    def _body(self, language: str) -> str:
        """Determine notification body."""

        body: dict[str, str] = {
            "fi_FI.UTF-8": "Näytönkaappaus otettu 📸 ",
            "en_US.UTF-8": "Screenshot taken 📸 ",
        }

        return body.get(language, body.get("en_US.UTF-8"))

    def show(self) -> None:
        """Display notification after taking screenshot."""
        try:
            subprocess.run(self._cmd)
        except FileNotFoundError:
            pass


def main() -> None:
    """Main function."""

    # Settings
    fmt: str = "png"
    language: str = os.environ["LANG"]
    notifications: bool = True

    # TODO: read config

    # Set up screenshot & notification devices
    screenshot: Screenshot = Screenshot(language, fmt)
    notification: ScreenshotNotification = ScreenshotNotification(language)

    # Take screenshot
    screenshot.capture()
    if notifications:
        notification.show()


if __name__ == "__main__":
    main()
