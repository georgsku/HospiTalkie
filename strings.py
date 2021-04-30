strings = dict(
    hospi_talkie = "HospiTalkie",
    contacts="{}",
    btn_record = "Press Go to record a message",
    new_messages = "New Messages",
    new_messages_description = "You got a new message, would you like to read/hear?",
    main_screen = "Welcome, press go btn to enter contacts, or back btn to enter messages",
    saved_messages = "Saved Messages",
    reply_message = "Press go btn to reply back to idle",
    new_message = "Du har en melding. Vil du lese?",
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
    done_recording = "Done recording",
    choose_reciever = "Choose Reciever",
)

def get_string(string, *args):
    return strings.get(string).format(*args)
