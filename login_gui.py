from appJar import gui
from gui_manager import GuiManager

class LoginGui:
  

  def __init__(self, stm_driver):
    self.stm_driver = stm_driver
    print("init LoginGui")
    self.app = gui("Login Window", "400x200")
    self.app.setBg("lightGrey")
    self.app.setFont(16)

    self.app.addLabel("title", "Welcome to HospiTalkie")
    self.app.setLabelBg("title", "blue")
    self.app.setLabelFg("title", "orange")

    self.app.addLabelEntry("Username")
    self.app.addLabelSecretEntry("Password")
    self.app.addButtons(["Submit", "Cancel"], self.press)
    self.app.setFocus("Username")
    

  def switch_gui(self):

    def extract_button(label):
        label = label.lower()
        if 'go' in label: return 'goBtnPressed'
        if 'back' in label: return 'backBtnPressed'
        if 'scroll' in label: return 'scrollBtnScrolled'
        if 'mute' in label: return 'muteBtnPressed'
        return None

    "logic in stm"
    def on_button_pressed(title):
        button = extract_button(title)
        print("btn pressed")

        "send which button is pressed to the state machine"
        self.stm_driver.send(button, "HospiTalkie")

    "implement function in hospietalkie and call when incoming message arrives" 

    self.app.setTitle("Idle")
    self.app.setLabel("title", " HospiTalkie ")
    self.app.removeLabel("Username")
    self.app.removeLabel("Password")
    self.app.removeButton("Submit")
    self.app.removeButton("Cancel")
    
    self.app.setSize("300x500")
    self.app.setInPadding([10, 10])
    self.app.addButton('Go', on_button_pressed)
    self.app.addButton('Back', on_button_pressed)
    self.app.addButton('Scroll', on_button_pressed)
    self.app.addButton('Mute', on_button_pressed)

    #self.app.addHorizontalSeparator(4, 0, 4, colour="white")
    self.app.addMessage("mess", "Welcome!")
    self.app.setMessageWidth("mess", "300")

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

  def message_received(self, message):
    print("hei og ho")
    self.app.yesNoBox("messread", "Du har en melding. Vil du lese?", parent=None)
    self.app.setMessage("mess", ""+message+"")

  def login_success(self):
    print("loginSucess")
    self.app.stop()
    self.myGUi = GuiManager()
    self.myGUi.stm_driver = self.stm_driver

      
