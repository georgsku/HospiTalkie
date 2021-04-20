# State Machine for the HospiTalkie

from stmpy import Machine, Driver

import ipywidgets as widgets
from IPython.display import display


#All the Functions can be here
class HospiTalkie:
    def __init__(self):
        #Do something
        
        
    def getPhoneBook(self):
        #Do something
        
    def loadPhoneBook(self):
        #Do something
        
hospitalkie = HospiTalkie()


##########################################
#    Transactions
##########################################

#Transaction naming convention: t_FROM_TO

#Transactions - Initial

t_initial_authorize = {'source': 'initial',
                       'target': 'authorize'}

t_authorize_authorize = {'trigger': 't',
                         'source': 'authorize',
                         'target': 'authorize'}

t_authorize_idle = {'trigger': 'authorized',
                    'source': 'authorize',
                    'target': 'idle'
                    'effect':'getPhoneBook'}

#Transactions - Do Not Disturb

t_idle_dontDisturb = {'trigger':'goBtnHold',
                      'source':'idle',
                      'target':'dontDisturb'}

t_dontDisturb_idle = {'trigger':'backBtnPressed',
                      'source':'dontDisturb',
                      'target':'idle'}

#Transactions - Send Message

t_idle_chooseRecipient = {'trigger':'goBtnPressed',
                          'source':'idle',
                          'target':'chooseRecipient',
                          'effect': 'loadPhoneBook'}

t_chooseRecipient_idle = {'trigger':'backBtnPressed',
                          'source':'chooseRecipient',
                          'target':'idle'}

t_chooseRecipient_chooseRecipient = {'trigger':'scrollBtnScrolled',
                                     'source':'chooseRecipient',
                                     'target':'chooseRecipient',
                                     'effect': 'display(nextContact)'}

t_chooseRecipient_startRecording = {'trigger':'goBtnPressed',
                                    'source':'chooseRecipient',
                                    'target':'startRecording',
                                    'effect': 'setRecipient'}

t_startRecording_recording = {'trigger':'goBtnPressed',
                              'source':'startRecording',
                              'target':'recording'}

t_recording_sendMessage = {'trigger':'goBtnReleased',
                           'source':'recording',
                           'target':'sendMessage',
                           'effect':'stopRecording'} #May be we can change it to exit?

t_recording_idle = {'trigger':'messagePublished',
                      'source':'recording',
                      'target':'idle',
                      'effect': 'display("Message sent")'}

t_recording_idle_t = {'trigger':'t',
                      'source':'recording',
                      'target':'idle',
                      'effect': 'display("Message not sent")'}

#Transactions - Message Received

#Transactions - Saved Message


##########################################
#    States
##########################################

#States naming convention: s_name

authorize = {'name': 'authorize',
             'entry': 'authenticate(); start_timer("t", 1000)',
             'exit': 'stop_timer("t")'}
idle = 
dontDisturb = 
chooseRecipient = 
startRecording = 
recording = 
sendMessage = 

savedMessage = 
showMessage = 
playMessage = 
reply = 

##########################################
#    State machine initialization
##########################################


#State Machine declaration
stm_hospiTalke = Machine(name='stm_hospitalkie',transactions=[], obj=hospitalkie, states=[])
hospitalkie.stm = stm_hospiTalke

driver = Driver()
driver.add_machine(stm_hospiTalke)
driver.start()