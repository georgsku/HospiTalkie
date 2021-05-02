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

t_login_authorize = {'trigger': 'loginError',
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

t_idle_dontDisturb = {'trigger':'muteBtnPressed', 
                      'source':'idle',
                      'target':'dontDisturb'}
transitions.append(t_idle_dontDisturb)

t_dontDisturb_idle = {'trigger':'muteBtnPressed',
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
                                     'effect': 'display("next_contact")'}
transitions.append(t_chooseRecipient_chooseRecipient)

t_chooseRecipient_startRecording = {'trigger':'goBtnPressed',
                                    'source':'chooseRecipient',
                                    'target':'startRecording',
                                    'effect': 'setRecipient()'}
transitions.append(t_chooseRecipient_startRecording)

t_startRecording_recording = {'trigger':'goBtnPressed',
                              'source':'startRecording',
                              'target':'recording'}
transitions.append(t_startRecording_recording)

t_startRecording_idle = {'trigger':'backBtnPressed',
                         'source':'startRecording',
                         'target':'idle'}
transitions.append(t_startRecording_idle)

t_recording_doneRecording = {'trigger':'goBtnPressed',
                            'source':'recording',
                            'target':'doneRecording',
                            'effect':'stopRecording'} 
transitions.append(t_recording_doneRecording)

t_recording_sendMessage = {'trigger':'recordingFinished',
                           'source':'doneRecording',
                           'target':'sendMessage',
                           'effect': 'sendMessage(*)'}
transitions.append(t_recording_sendMessage)

t_recording_idle = {'trigger':'messagePublished',
                    'source':'sendMessage',
                    'target':'idle',
                    'effect': 'display("Message sent")'}
transitions.append(t_recording_idle)

t_recording_idle_t = {'trigger':'t',
                      'source':'sendMessage',
                      'target':'idle',
                      'effect': 'display("Message not sent")'}
transitions.append(t_recording_idle_t)

#Transitions - Message Received
t_idle_newMessage = {'trigger':'messageReceived',
                     'source':'idle',
                     'target':'newMessage',
                     'effect': 'getMessage(*)'}
transitions.append(t_idle_newMessage)

#TODO: stop playing in the player state machine by setting variable

t_newMessage_playOrStore = {'trigger':'playingFinished',
                            'source':'newMessage',
                            'target':'playOrStore'}
transitions.append(t_newMessage_playOrStore)

t_playOrStore_idle = {'trigger':'backBtnPressed',
                      'source':'playOrStore',
                      'target':'idle',
                      'effect': 'storeMessages()'}
transitions.append(t_playOrStore_idle)

t_playOrStore_playMessage = {'trigger':'goBtnPressed',
                             'source':'playOrStore',
                             'target':'playMessage'}
transitions.append(t_playOrStore_playMessage)

# TODO: Compound transition
t_playMessage_reply = {'trigger':'playingFinished',
                       'source':'playMessage',
                       'target':'reply'}
transitions.append(t_playMessage_reply)

t_reply_idle = {'trigger':'backBtnPressed',
                'source':'reply',
                'target':'idle'}
transitions.append(t_reply_idle)                   

t_reply_recording = {'trigger':'goBtnPressed',
                     'source':'reply',
                     'target':'recording'}
transitions.append(t_reply_recording)

#Transitions - Saved Message
t_idle_savedMessages = {'trigger':'backBtnPressed',
                        'source':'idle',
                        'target':'savedMessages'}
transitions.append(t_idle_savedMessages)


t_savedMessages_savedMessages = {'trigger':'scrollBtnScrolled',
                                 'source':'savedMessages',
                                 'target':'savedMessages',
                                 'effect': 'highlightNextMessage()'}
transitions.append(t_savedMessages_savedMessages)

t_savedMessages_playMessage = {'trigger':'goBtnPressed',
                               'source':'savedMessages',
                               'target':'playMessage'}
transitions.append(t_savedMessages_playMessage)


t_savedMessages_playMessage = {'trigger':'backBtnPressed',
                               'source':'savedMessages',
                               'target':'idle'}
transitions.append(t_savedMessages_playMessage)


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
               'messageReceived': 'defer',
               'exit': 'unmute()'}
states.append(dontDisturb)

chooseRecipient = {'name': 'chooseRecipient',
                   'entry': 'display("Contacts")',
                   'messageReceived': 'defer'}
states.append(chooseRecipient)

startRecording = {'name': 'startRecording',
                  'entry': 'display("btn_record")',
                  'messageReceived': 'defer'}
states.append(startRecording)

# TODO: Need to check startRecording entry point - specially with may function parameters

recording = {'name': 'recording',
             'entry': 'startRecording; display("recording")',
             'messageReceived': 'defer'}
states.append(recording)

doneRecording = {'name': 'doneRecording',
                 'entry': 'stopRecording; display("done_recording")',
                 'messageReceived': 'defer'}
states.append(doneRecording)

sendMessage = {'name': 'sendMessage',
       #        'entry': 'start_timer("t", 10000)',
               'messageReceived': 'defer',
               'exit': 'stop_timer("t")'}
states.append(sendMessage)

#States - Saved Messages
savedMessages = {'name': 'savedMessages',
                 'entry': 'display("saved_messages")',
                 'messageReceived': 'defer'}
states.append(savedMessages)

newMessage = {'name': 'newMessage',
              'entry': 'display("new_message")',
              'entry': 'playNotification()',
              'messageReceived': 'defer'}
states.append(newMessage)

playOrStore = {'name': 'playOrStore',
               'entry': 'display("play_or_store")',
               'messageReceived': 'defer'}
states.append(playOrStore)

playMessage = {'name': 'playMessage',
               'entry': 'playMessage; display("playing")',
               'messageReceived': 'defer'}
states.append(playMessage)

reply = {'name': 'reply',
         'entry': 'display("reply_message")',
         'messageReceived': 'defer'}
states.append(reply)
