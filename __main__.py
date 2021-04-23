import HospiTalkie
import GuiManager
import mqttCommunication
from stm_hospi_talkie import transitions, states

# broker, port = 'iot.eclipse.org', 1883
broker, port = "localhost", 1883

hospiTalkie = HospiTalkie()
ted  = Machine(transitions=transitions, obj=self, name="HospiTalkie", states=states)
hospiTalkie.stm = tick_tock_machine

driver = Driver()
driver.add_machine(tick_tock_machine)


myclient.stm_driver = driver

myGUi = GuiManager()
myGUi.stm_driver = driver

driver.start()
myclient.start(broker, port)