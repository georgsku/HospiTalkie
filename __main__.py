from hospi_talkie import HospiTalkie 
from login_gui import LoginGui
from stm_hospi_talkie import transitions, states
from stmpy import Driver, Machine


driver = Driver()

login_gui = LoginGui(driver)

hospiTalkie = HospiTalkie()
machine  = Machine(transitions=transitions, obj=hospiTalkie, name="HospiTalkie", states=states)
driver.add_machine(machine)
#hospiTalkie.stm = machine

driver.start()
hospiTalkie.start(driver, login_gui)

login_gui.app.go()