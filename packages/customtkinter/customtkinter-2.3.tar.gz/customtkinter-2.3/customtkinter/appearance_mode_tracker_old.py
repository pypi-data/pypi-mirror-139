from threading import Thread
import time
import sys
from distutils.version import StrictVersion as Version
import darkdetect

if Version(darkdetect.__version__) < Version("0.3.1"):
    sys.stderr.write("WARNING: You have to update the darkdetect library: pip3 install --upgrade darkdetect\n")
    if sys.platform != "darwin":
        exit()


class SystemAppearanceModeListener(Thread):
    """ This class checks for a system appearance change
        in a loop, and if a change is detected, than the
        callback function gets called. Either 'Light' or
        'Dark' is passed in the callback function. """

    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDaemon(True)

        self.appearance_mode = self.detect_appearance_mode()
        self.callback_function = callback

        self.activated = True

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def get_mode(self):
        return self.appearance_mode

    def set_mode(self, appearance_mode):
        self.appearance_mode = appearance_mode

    @staticmethod
    def detect_appearance_mode():
        try:
            if darkdetect.theme() == "Dark":
                return 1  # Dark
            else:
                return 0  # Light
        except NameError:
            return 0  # Light

    def run(self):
        while True:
            if self.activated:
                detected_mode = self.detect_appearance_mode()
                if detected_mode != self.appearance_mode:
                    self.appearance_mode = detected_mode

                    if self.appearance_mode == 0:
                        self.callback_function("Light", from_listener=True)
                    else:
                        self.callback_function("Dark", from_listener=True)
                time.sleep(0.5)
            else:
                while self.activated is False:
                    time.sleep(0.05)


class SystemAppearanceModeListenerNoThread:
    def __init__(self, callback):
        self.appearance_mode = self.detect_appearance_mode()
        self.callback_function = callback

        self.activated = True

    def get_mode(self):
        return self.appearance_mode

    @staticmethod
    def detect_appearance_mode():
        try:
            if darkdetect.theme() == "Dark":
                return 1  # Dark
            else:
                return 0  # Light
        except NameError:
            return 0  # Light

    def update(self):
        detected_mode = self.detect_appearance_mode()
        if detected_mode != self.appearance_mode:
            self.appearance_mode = detected_mode

            if self.appearance_mode == 0:
                self.callback_function("Light", from_listener=True)
            else:
                self.callback_function("Dark", from_listener=True)


class AppearanceModeTracker():
    """ This class holds a list with callback functions
        of every customtkinter object that gets created.
        And when either the SystemAppearanceModeListener
        or the user changes the appearance_mode, all
        callbacks in the list get called and the
        new appearance_mode is passed over to the
        customtkinter objects """

    callback_list = []
    appearance_mode = 0  # Light (standard)
    system_mode_listener = None

    @classmethod
    def init_listener_function(cls, no_thread=False):
        if isinstance(cls.system_mode_listener, SystemAppearanceModeListener):
            cls.system_mode_listener.deactivate()

        if no_thread is True:
            cls.system_mode_listener = SystemAppearanceModeListenerNoThread(cls.set_appearance_mode)
            cls.appearance_mode = cls.system_mode_listener.get_mode()
        else:
            cls.system_mode_listener = SystemAppearanceModeListener(cls.set_appearance_mode)
            cls.system_mode_listener.start()
            cls.appearance_mode = cls.system_mode_listener.get_mode()

    @classmethod
    def add(cls, callback):
        cls.callback_list.append(callback)

    @classmethod
    def remove(cls, callback):
        cls.callback_list.remove(callback)

    @classmethod
    def get_mode(cls):
        return cls.appearance_mode

    @classmethod
    def set_appearance_mode(cls, mode_string, from_listener=False):
        if mode_string.lower() == "dark":
            cls.appearance_mode = 1
            cls.system_mode_listener.set_mode(1)

            if not from_listener:
                cls.system_mode_listener.deactivate()

        elif mode_string.lower() == "light":
            cls.appearance_mode = 0
            cls.system_mode_listener.set_mode(0)

            if not from_listener:
                cls.system_mode_listener.deactivate()

        elif mode_string.lower() == "system":
            cls.system_mode_listener.activate()

        if cls.appearance_mode == 0:
            for callback in cls.callback_list:
                try:
                    callback("Light")
                except Exception:
                    print("error callback")
                    continue

        elif cls.appearance_mode == 1:
            for callback in cls.callback_list:
                try:
                    callback("Dark")
                except Exception:
                    print("error callback")
                    continue


AppearanceModeTracker.init_listener_function()
