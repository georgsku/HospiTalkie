from appJar import gui
from strings import get_string
class LoginGui:
  

  def __init__(self, stm_driver):
    import threading
    print("thread gui: ")
    print(threading.current_thread())

    self.stm_driver = stm_driver
    print("init LoginGui")
    self.app = gui("Login Window", "400x200")
    self.app.setBg("#d8e0bb")
    self.app.setFont(16)

    self.app.startFrame("header", row=0, column=0, rowspan=1, colspan=2)
    self.app.addLabel("title", "Welcome to HospiTalkie")
    self.app.setLabelFg("title", "#6b3074")
    self.app.getLabelWidget("title").config(font=("Sans Serif", "24", "bold"))
    self.app.stopFrame()

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
        print("btn pressed" + title)

        "send which button is pressed to the state machine"
        self.stm_driver.send(button, get_string("hospi_talkie"))

    "implement function in hospietalkie and call when incoming message arrives" 

    
    
    self.app.removeLabel("Username")
    self.app.removeLabel("Password")
    self.app.removeButton("Submit")
    self.app.removeButton("Cancel")
    self.app.removeLabel("title")

    self.app.setSize("300x300")
    self.app.setStretch("both")
    self.app.setSticky("")

    self.app.addLabel("title", "Welcome to HospiTalkie", 0, 0, 2, 1)
    self.app.setLabelFg("title", "#6b3074")
    self.app.getLabelWidget("title").config(font=("Sans Serif", "24", "bold"))

    self.app.addMessage("mess", "", 1, 0, 2, 1)
    self.app.getMessageWidget("mess").config(font=("Sans Serif", "16", "italic"))
    self.app.setMessageFg("mess", "#6b3074")
    self.app.setMessageWidth("mess", "300")

    self.app.addButton('Go', on_button_pressed, 2, 0)
    self.app.setButtonWidth("Go", "12")
    self.app.setButtonBg("Go", "#6b3074")

    self.app.addButton('Back', on_button_pressed, 2, 1)
    self.app.setButtonWidth("Back", "12")
    self.app.setButtonBg("Back", "#6b3074")

    self.app.addButton('Scroll', on_button_pressed, 3, 0)
    self.app.setButtonWidth("Scroll", "12")
    self.app.setButtonBg("Scroll", "#6b3074")
    
    self.app.addButton('Mute', on_button_pressed, 3, 1)
    self.app.setButtonWidth("Mute", "12")
    self.app.setButtonBg("Mute", "#6b3074")

  def press(self, button):
      if button == "Cancel":
          self.app.stop()
      else:
          usr = self.app.getEntry("Username")
          pwd = self.app.getEntry("Password")
          self.stm_driver.send("submit", "HospiTalkie" ,args=[usr, pwd])


  def login_error(self):
    print("login error")
    self.app.infoBox(get_string("wrong_user_pass"), get_string("retype_user_pass"), parent=None)

  def message_received(self, message):
    print("hei og ho")
    self.app.yesNoBox("messread", get_string("new_message"), parent=None)
    self.app.setMessage("mess", str(message))

  def login_success(self):
    print("loginSucess")
    self.app.stop()
    self.myGUi = GuiManager()
    self.myGUi.stm_driver = self.stm_driver
