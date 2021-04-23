from stmpy import Machine, Driver

##########################################
#    Transitions
##########################################
transitions = []


#Transaction naming convention: t_FROM_TO

#Transitions - Initial

t_initial_authorize = {'source': 'initial',
                       'target': 'authorize'}
transitions.append(t_initial_authorize)

t_authorize_authorize = {'trigger': 't',
                         'source': 'authorize',
                         'target': 'authorize'}

t_authorize_idle = {'trigger': 'authorized',
                    'source': 'authorize',
                    'target': 'idle',
                    'effect':'getPhoneBook'}

#Transitions - Do Not Disturb

t_idle_dontDisturb = {'trigger':'goBtnHold',
                      'source':'idle',
                      'target':'dontDisturb'}

t_dontDisturb_idle = {'trigger':'backBtnPressed',
                      'source':'dontDisturb',
                      'target':'idle'}

#Transitions - Send Message

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

#Transitions - Message Received
states = []

t_idle_showMessages = {'trigger':'messageReceived',
                       'source':'idle',
                       'target':'showMessages'}
states.append(t_idle_showMessages)

t_showMessages_idle = {'trigger':'backBtnPressed',
                       'source':'showMessages',
                       'target':'idle',
                       'effect': 'storeMessages()'}

t_showMessages_playMessages = {'trigger':'goBtnPressed',
                               'source':'showMessages',
                               'target':'playMessages'}

t_playMessages_reply
t_reply_idle

#Transitions - Saved Message

t_idle_savedMessages
t_savedMessages_savedMessages
t_savedMessages_playMessages

##########################################
#    States
##########################################

#States naming convention: s_name

authorize = {'name': 'authorize',
             'entry': 'authenticate(); start_timer("t", 1000)',
             'exit': 'stop_timer("t")'}

idle = {'name': 'idle',
        'entry': 'display(main_screen)'}

dontDisturb = {'name': 'dontDisturb',
               'entry': 'mute()',
               'exit': 'unmute()'}

chooseRecipient = {'name': 'chooseRecipient',
                   'entry': 'display(Contacts)'}

startRecording = {'name': 'startRecording',
                   'entry': 'display("press btn to record a message to", "chosenReciever")'}
# TODO: Need to check startRecording entry point - specially with display function parameters

recording = {'name': 'recording',
             'entry': 'startRecording; display("Recording")'}

sendMessage = {'name': 'sendMessage',
               'entry': 'sendMessage(); start_timer("t", 1000)',
               'exit': 'stop_timer("t")'}
transitions.append(sendMessage)



savedMessage = 
showMessage = 
playMessage = 
reply = 




