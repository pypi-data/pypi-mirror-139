import PySimpleGUI as sg
from better_cryptography import Ciphers, Log, compare_hashes, hash_ 


# layouts goddamn
login_layout = [
    [sg.Text('Enter current Linux username. This will be used to access relevant directories/files.', font="Helvetica")],
    [sg.InputText(key='username', font="Helvetica", border_width=10)],
    [sg.Text("Enter password.", font="Helvetica")],
    [sg.InputText(key="password", password_char='*', font="Helvetica", border_width=10)],
    [sg.Button("Ok", font="Helvetica", border_width=10), sg.Button("Close Window", font="Helvetica", border_width=10)]
] # this layout is done
logged_layout = [
    [sg.Text('Password confirmed, user logged. What would you like to do?', font="Helvetica", border_width=10)],
    [sg.Button('Edit file configurations', key="file_hub", font="Helvetica", border_width=10),
    sg.Button('Change my password', key='password_change', font="Helvetica", border_width=10)],
    [sg.Button('Close Window', key='Close', font="Helvetica", border_width=10)]
] # this layout is done
change_pass_layout = [
    [sg.Text("Please enter your current password.", font="Helvetica")],
    [sg.InputText(key="old_password", password_char='*', font="Helvetica", border_width=10)],
    [sg.Text("Please enter your new password.", font="Helvetica")],
    [sg.InputText(key="new_password", password_char="*", font="Helvetica", border_width=10)],
    [sg.Button("Ok", key="OK_pass", font="Helvetica", border_width=10), sg.Button("Go back", key="back_pass", font="Helvetica", border_width=10)]
] # also done
file_hub_script_layout = [
    [sg.Text("Please select a command.", font="Helvetica")],
    [sg.Frame("External file commands",[
        [sg.Button("File encryption - encrypts a singular file, given the path.", key="file_encrypt", font="Helvetica"),
        sg.Button("File decryption - decrypts an already encrypted file, given the path.", key="file_decrypt", font="Helvetica")]],
        border_width=10, background_color="#626a80", element_justification="C")],
    [sg.Frame('External folder commands',[
        [sg.Button("Folder encryption - encrypts a singular folder, given the path.",key="folder_encrypt", font="Helvetica"),
        sg.Button("Folder decryption - decrypts an already encrypted folder, given the path.", key='folder_decrypt', font="Helvetica")]],
        border_width=10, background_color="#626a80", element_justification="C")],
    [sg.Frame('Vault commands',[
        [sg.Button("Encrypt Vault - encrypts every non-encrypted file in the Vault folder.", key="vault_encrypt", font="Helvetica"),
        sg.Button('Decrypt Vault - decrypts every encrypted file in the Vault folder.', key="vault_decrypt", font="Helvetica")]],
        border_width=10, background_color="#626a80", element_justification="C")],
    [sg.Button('Back - Go back to previous screen', key='back', font="Helvetica", border_width=10), sg.Button("Audit UserLog File", key="Intiate_audit", font="Helvetica", border_width=10)],
    [sg.Button("Logout - terminates application and logs user out.", key="logout", font="Helvetica", border_width=10)]
]# this layout is done
userLog_audit_layout = [
    [sg.Text("UserLog Audit Mode selected. What would you like to do?")],
    [sg.Button("Remove singular file Encryption/Decryption logs", key="single_file_log_audit", font="Helvetica", border_width=10),
    sg.Button("Remove Folder Encryption/Decryption Logs", key="folder_logs_audit", font="Helvetica", border_width=10)],
    [sg.Button("Remove Vault Encryption/Decryption Logs", key="vault_log_audit", font="Helvetica", border_width=10),
    sg.Button('Clear userlog.', key="Clear_userlog", font="Helvetica", border_width=10)],
    [sg.Button("Return to previous screen", key="audit_return", font="Helvetica", border_width=10),
    sg.Button("Close Window", key="Close_Audit", font="Helvetica", border_width=10)]
]
layout = [
    [sg.Column(login_layout, key="Login_Layout", element_justification="C"),
    sg.Column(logged_layout, visible=False, key="Logged_Layout", element_justification="C"),
    sg.Column(file_hub_script_layout, visible=False, key="File_hub_layout", element_justification="C"),
    sg.Column(change_pass_layout, visible=False, key='Change_pass_layout', element_justification="C"),
    sg.Column(userLog_audit_layout, visible=False, key="userLog_audit_layout", element_justification="C")
    ]
]




