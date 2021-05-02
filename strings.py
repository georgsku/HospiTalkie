strings = dict(
    hospi_talkie = "HospiTalkie",
    contacts="{}",
    btn_record = "Press Go to record a message",
    new_message = "New Message",
    new_messages = "New Messages",
    new_messages_description = "You got a new message, would you like to read/hear?",
    play_or_store = "You got a new message, would you like to hear?",
    main_screen = "Welcome, press go btn to enter contacts, or back btn to enter messages",
    saved_messages = "Saved Messages",
    reply = "Reply",
    reply_message = "Press Go btn to reply to {}, or Back to idle",
    wrong_user_pass = "Wrong Username or Password",
    retype_user_pass = "Please type your username or password again",
    btn_go = "Go",
    btn_back = "Back",
    btn_scroll = "Scroll",
    btn_mute = "Mute",
    mute = "Mute",
    unmute = "Unmute",
    dont_disturb = "Do Not Disturb",
    not_disturbed = "You will not be disturbed!",
    record_message = "Record Message",
    idle = "Idle",
    recording = "Recording message... Press Go to stop.",
    done_recording = "Done recording",
    playing = "Playing",
    playing_from = "Playing {}'s message",
    choose_reciever = "Choose Reciever",
    next_message = "Messages"
)

def get_string(string, *args):
    return strings.get(string).format(*args)
