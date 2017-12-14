import subprocess
from keycode import ANDROID_KEYCODE
from robot import Robot
import os
import re

PATH = lambda p: os.path.abspath(p)

KEYCODE = ANDROID_KEYCODE
subp = os.path.join(os.environ["Android_HOME"], "platform-tools", "adb")


class ADBRobot(Robot):
    def open_app(self, appName):
        # subprocess.check_output([subp, "shell", "am", "start", "-n", appName ], shell=True)
        command = "adb shell am start -n " + appName
        subprocess.check_output(command, shell=True)

    def close_app(self, appName):
        # subprocess.check_output([subp, "shell", "am", "force-stop", appName], shell=True)
        command = "adb shell am force-stop " + appName
        subprocess.check_output(command, shell=True)

    def get_devices(self):
        dList = subprocess.getoutput('adb devices')
        dNames = dList.splitlines()[1]
        return dNames.split('\t')[0]

    def send_keys(self, keys):
        for key in keys:
            self.send_key(KEYCODE[key])

    def send_key(self, keycode):
        # return subprocess.call([subp, "shell", "input", "keyevent", str(keycode)], shell=True)
        command = "adb shell input keyevent " + str(keycode)
        return subprocess.call(command, shell=True)

    def drag_and_drop(self, start_x, start_y, end_x, end_y):
        # subprocess.call([subp, "shell", "input", "swipe", str(start_x), str(start_y), str(end_x), str(end_y) ], shell=True)
        command = " ".join(["adb shell input swipe", str(start_x), str(start_y), str(end_x), str(end_y)])
        subprocess.call(command, shell=True)

    def screenshot(self):
        path = "./screenshot_pic"
        wait = "adb wait-for-device"
        subprocess.call(wait, shell=True)
        fileName = "tmp.png"
        capture = "adb shell screencap -p ./data/local/tmp/" + fileName
        subprocess.call(capture, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        pull = "adb pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull ,shell=True)
        print("success")
        return path + "/" + fileName

    def before_screenshot(self):
        path = "./screenshot_pic"

        # subprocess.call([subp, "wait-for-device"], shell=True)
        wait = "adb wait-for-device"
        subprocess.call(wait, shell=True)

        # subprocess.call([subp, "shell", "screencap", "-p", "/data/local/tmp/before.png"], shell=True)
        fileName = "before.png"
        capture = "adb shell screencap -p ./data/local/tmp/" + fileName
        subprocess.call(capture, shell=True)

        if not os.path.isdir(path):
            os.makedirs(path)

        # subprocess.call([subp, "pull", "/data/local/tmp/before.png", str(PATH(path + "/before.png"))], shell=True)
        pull = "adb pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull, shell=True)
        print("success")
        return path + "/" + fileName

    def after_screenshot(self):
        path = "./screenshot_pic"

        # subprocess.call([subp, "wait-for-device"], shell=True)
        wait = "adb wait-for-device"
        subprocess.call(wait, shell=True)
        # subprocess.call([subp, "shell", "screencap", "-p", "/data/local/tmp/after.png"], shell=True)
        fileName = "after.png"
        capture = "adb shell screencap -p ./data/local/tmp/" + fileName
        subprocess.call(capture, shell=True)

        if not os.path.isdir(path):
            os.makedirs(path)

        # subprocess.call([subp, "pull", "/data/local/tmp/after.png", str(PATH(path + "/after.png"))], shell=True)
        pull = "adb pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull, shell=True)
        print("success")
        return path + "/after.png"

    def tap(self, x, y, duration=None):
        if duration:
            # subprocess.call(
            #     [subp, "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(3000)],
            #     shell=True)
            command = " ".join(["adb shell input swipe", str(x), str(y), str(x), str(y), str(3000)])
        else:
            # subprocess.call(
            #     [subp, "shell", "input", "tap", str(x), str(y)],
            #     shell=True)
            command = " ".join(["adb shell input tap", str(x), str(y)])

        subprocess.call(command, shell=True)

    def input_text(self, text):
        #print("text =" + str(text))
        try:
            text = text.replace(' ', '%s')
            command = 'adb shell input text ' + text
            subprocess.call(command, shell=True)

            return "Success"
        except:
            print("Input Text Error", text)
            return "Error"

    def get_uiautomator_dump(self):
        # path = PATH(os.getcwd() + "/dumpXML")
        path = "./dumpXML"

        # subprocess.call([subp, "wait-for-device"], shell=True)
        wait = "adb wait-for-device"
        subprocess.call(wait, shell=True)
        # subprocess.call([subp, "shell", "uiautomator", "dump", "/data/local/tmp/uidump.xml"], shell=True)
        fileName = "uidump.xml"
        dump = "adb shell uiautomator dump ./data/local/tmp/" + fileName
        subprocess.call(dump, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        # subprocess.call([subp, "pull", "/data/local/tmp/uidump.xml", path + "/uidump.xml"], shell=True)
        pull = "adb pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull, shell=True)
        print(path + "/uidump.xml")
        return path + "/uidump.xml"

    def get_display(self):
        real_size_pattern = r"real (\d+) x (\d+),"
        result = subprocess.check_output('adb shell dumpsys display | grep mBaseDisplayInfo', shell=True).__str__()
        match = re.search(real_size_pattern, result)
        return (match.group(1), match.group(2))

    # @property
    # def windows_size(self):
    #     """
    #     adb shell dumpsys display | grep mBaseDisplayInfo
    #
    #     :return:
    #     """
    #     #real 1080 X 1920
    #     real_size_pattern = r"real (\d+) x (\d+),"
    #
    #     #density 480 (480.0 x 480.0) dpi,
    #     #density_pattern = re.compile(r"density (\d+) \((\d+.\d+ x \d+.\d+)\) dpi,")
    #
    #     result = grep(adb("shell", "dumpsys", "display"), "mBaseDisplayInfo").__str__()
    #     match = re.search(real_size_pattern, result)
    #     if match:
    #         size = (int(match.group(1)), int(match.group(2)))
    #     else:
    #         size = None
    #
    #     return size