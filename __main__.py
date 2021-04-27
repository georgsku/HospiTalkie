from hospi_talkie import HospiTalkie 
from login_gui import LoginGui
from stm_hospi_talkie import transitions, states
from stmpy import Driver, Machine

driver = Driver()
hospiTalkie = HospiTalkie()
machine  = Machine(transitions=transitions, obj=hospiTalkie, name="HospiTalkie", states=states)
driver.add_machine(machine)
#hospiTalkie.stm = machine

driver.start()
hospiTalkie.start(driver)