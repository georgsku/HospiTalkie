from stmpy import Machine, Driver

##########################################
#    Transitions
##########################################
transitions = []


#Transaction naming convention: t_FROM_TO

#Transitions - Initial

t_initial_login = {'source': 'initial',
                       'target': 'login',}
transitions.append(t_initial_login)

t_login_authorize = {'trigger': 'error',
                         'source': 'login',
                         'target': 'login',
                         'effect': 'loginError'}
transitions.append(t_login_authorize)

t_login_idle = {'trigger': 'loginSuccess',
                    'source': 'login',
                    'target': 'idle',
                    'effect':'loginSuccess',}
transitions.append(t_login_idle)


#Transitions - Do Not Disturb

t_idle_dontDisturb = {'trigger':'goBtnHold',
                      'source':'idle',
                      'target':'dontDisturb'}
transitions.append(t_idle_dontDisturb)

t_dontDisturb_idle = {'trigger':'backBtnPressed',
                      'source':'dontDisturb',
                      'target':'idle'}
transitions.append(t_dontDisturb_idle)


#Transitions - Send Message

t_idle_chooseRecipient = {'trigger':'goBtnPressed',
                          'source':'idle',
                          'target':'chooseRecipient',
                          'effect': 'loadPhoneBook'}
transitions.append(t_idle_chooseRecipient)

t_chooseRecipient_idle = {'trigger':'backBtnPressed',
                          'source':'chooseRecipient',
                          'target':'idle'}
transitions.append(t_chooseRecipient_idle)

t_chooseRecipient_chooseRecipient = {'trigger':'scrollBtnScrolled',
                                     'source':'chooseRecipient',
                                     'target':'chooseRecipient',
                                     'effect': 'display("nextContact")'}
transitions.append(t_chooseRecipient_chooseRecipient)

t_chooseRecipient_startRecording = {'trigger':'goBtnPressed',
                                    'source':'chooseRecipient',
                                    'target':'startRecording',
                                    'effect': 'setRecipient'}
transitions.append(t_chooseRecipient_startRecording)

t_startRecording_recording = {'trigger':'goBtnPressed',
                              'source':'startRecording',
                              'target':'recording'}
transitions.append(t_startRecording_recording)

t_recording_sendMessage = {'trigger':'goBtnReleased',
                           'source':'recording',
                           'target':'sendMessage',
                           'effect':'stopRecording'} #May be we can change it to exit?
transitions.append(t_recording_sendMessage)

t_recording_idle = {'trigger':'messagePublished',
                      'source':'recording',
                      'target':'idle',
                      'effect': 'display("Message sent")'}
transitions.append(t_recording_idle)

t_recording_idle_t = {'trigger':'t',
                      'source':'recording',
                      'target':'idle',
                      'effect': 'display("Message not sent")'}
transitions.append(t_recording_idle_t)

#Transitions - Message Received


t_idle_showMessages = {'trigger':'messageReceived',
                       'source':'idle',
                       'target':'showMessages'}
transitions.append(t_idle_showMessages)

t_showMessages_idle = {'trigger':'backBtnPressed',
                       'source':'showMessages',
                       'target':'idle',
                       'effect': 'storeMessages()'}
transitions.append(t_showMessages_idle)

t_showMessages_playMessages = {'trigger':'goBtnPressed',
                               'source':'showMessages',
                               'target':'playMessages'}
transitions.append(t_showMessages_playMessages)

""" t_playMessages_reply
t_reply_idle

#Transitions - Saved Message

t_idle_savedMessages
t_savedMessages_savedMessages
t_savedMessages_playMessages
 """
##########################################
#    States
##########################################

#States naming convention: s_name
states= []
login = {'name': 'login',
             'submit': 'authenticate(*)',}
states.append(login)

idle = {'name': 'idle',
        'entry': 'display("main_screen")'}
states.append(idle)

dontDisturb = {'name': 'dontDisturb',
               'entry': 'mute()',
               'exit': 'unmute()'}
states.append(dontDisturb)

chooseRecipient = {'name': 'chooseRecipient',
                   'entry': 'display("Contacts")'}
states.append(chooseRecipient)

startRecording = {'name': 'startRecording',
                   'entry': 'display("press btn to record a message to", "chosenReciever")'}
states.append(startRecording)
# TODO: Need to check startRecording entry point - specially with display function parameters

recording = {'name': 'recording',
             'entry': 'startRecording; display("Recording")'}
states.append(recording)

sendMessage = {'name': 'sendMessage',
               'entry': 'sendMessage(); start_timer("t", 1000)',
               'exit': 'stop_timer("t")'}
states.append(sendMessage)



savedMessage = {}
showMessage = {}
playMessage = {}
reply = {}




