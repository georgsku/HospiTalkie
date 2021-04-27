from appJar import gui

class LoginGui:

  def __init__(self, stm_driver):
    self.stm_driver = stm_driver
    print("init LoginGui")
    self.app = gui("Login Window", "400x200")
    self.app.setBg("orange")
    self.app.setFont(18)

    self.app.addLabel("title", "Welcome to HospiTalkie")
    self.app.setLabelBg("title", "blue")
    self.app.setLabelFg("title", "orange")

    self.app.addLabelEntry("Username")
    self.app.addLabelSecretEntry("Password")
    self.app.addButtons(["Submit", "Cancel"], self.press)
    self.app.setFocus("Username")
    self.app.go()

  def press(self, button):
      if button == "Cancel":
          self.app.stop()
      else:
          usr = self.app.getEntry("Username")
          pwd = self.app.getEntry("Password")
          self.stm_driver.send("submit", "HospiTalkie" ,args=[usr, pwd])


  def login_error(self):
    print("login error")
    self.app.infoBox("Wrong Username or Password", "Please type your username or password again ", parent=None)

  def login_success(self):
    print("loginSucess")
    self.myGUi = GuiManager()
    self.myGUi.stm_driver = self.stm_driver
    self.app.stop()

