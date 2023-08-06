"""class for the settings"""


from PySide6.QtWidgets import QTabWidget, QMainWindow

import meshtastic.serial_interface

from meshtastic_flasher.admin_form import AdminForm
from meshtastic_flasher.wifi_and_mqtt_form import Wifi_and_MQTT_Form
from meshtastic_flasher.user_form import UserForm
from meshtastic_flasher.position_form import PositionForm
from meshtastic_flasher.power_form import PowerForm
from meshtastic_flasher.radio_form import RadioForm
#from meshtastic_flasher.channels_form import ChannelsForm


class Settings(QMainWindow):
    """settings"""

    def __init__(self):
        """constructor"""
        super(Settings, self).__init__()

        self.port = None
        self.interface = None

        width = 800
        height = 600
        self.setMinimumSize(width, height)
        self.setWindowTitle("Settings")

        self.admin_form = AdminForm(self)
        self.wifi_and_mqtt_form = Wifi_and_MQTT_Form(self)
        self.user_form = UserForm(self)
        self.position_form = PositionForm(self)
        self.power_form = PowerForm(self)
        self.radio_form = RadioForm(self)
        #self.channels_form = ChannelsForm(self)

        self.tabs = QTabWidget()

        self.setStyleSheet("""
QTabWidget::pane { position: absolute; top: -0.5em; }
QTabWidget::tab-bar { alignment: center; }
QTabBar::tab:selected {
    /* expand/overlap to the left and right by 4px */
    margin-left: -4px;
    margin-right: -4px;
}
QTabBar::tab:first:selected {
    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
}
QTabBar::tab:last:selected {
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
}
QTabBar::tab:only-one {
    margin: 0; /* if there is only one tab, we don't want overlapping margins */
}
""")
        self.tabs.blockSignals(True) # just for not showing initial message
        self.tabs.currentChanged.connect(self.on_change_tabs)

        #tabs.setTabPosition(QTabWidget.West)
        self.tabs.setTabPosition(QTabWidget.North)

        self.tabs.addTab(self.wifi_and_mqtt_form, "Wifi/MQTT")
        self.tabs.addTab(self.position_form, "Position")
        self.tabs.addTab(self.user_form, "User")
        self.tabs.addTab(self.power_form, "Power")
        self.tabs.addTab(self.radio_form, "Radio")
        self.tabs.addTab(self.admin_form, "ADMIN")
        #self.tabs.addTab(self.channels_form, "Channels")

        self.setCentralWidget(self.tabs)

        self.tabs.blockSignals(False) # now listen the currentChanged signal


    def on_change_tabs(self, i):
        """On change of each tab """
        print(f'on_change_tabs:{i}')
        if i == 0:
            print('wifi_and_mqtt_form run()')
            self.wifi_and_mqtt_form.run(port=self.port, interface=self.interface)
        elif i == 1:
            print('position run()')
            self.position_form.run(port=self.port, interface=self.interface)
        elif i == 2:
            print('user run()')
            self.user_form.run(port=self.port, interface=self.interface)
        elif i == 3:
            print('power run()')
            self.power_form.run(port=self.port, interface=self.interface)
        elif i == 4:
            print('radio run()')
            self.radio_form.run(port=self.port, interface=self.interface)
        elif i == 5:
            print('admin form run()')
            self.admin_form.run(port=self.port, interface=self.interface)
#        elif i == 5:
#            print('channels run()')
#            self.channels_form.run(port=self.port, interface=self.interface)


    def my_close(self):
        """Close this window"""
        self.port = None
        self.interface.close()
        self.interface = None # so any saved values are re-read upon next form use
        self.close()


    # pylint: disable=unused-argument
    def closeEvent(self, event):
        """On close of the Settings window"""
        print('closed Settings')
        self.close()


    def run(self, port=None):
        """load the form"""
        print(f'in settings run() port:{port}:')
        self.show()
        if port and port != '':
            self.port = port
        print(f'self.port:{self.port}:')
        if self.interface is None:
            try:
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
                self.port = self.interface.devPath
                print(f'self.port:{self.port}:')
            except Exception as e:
                print(f'Exception:{e}')
        self.wifi_and_mqtt_form.run(port=self.port, interface=self.interface)
