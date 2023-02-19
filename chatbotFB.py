import tkinter as tk


import fbchat
from fbchat.models import *


class FacebookMessengerApp:
    
    def __init__(self, master):
        
        
        self.error_label = None
        self.check_buttons = {}

        # Set up the GUI
        self.master = master
        master.title("Facebook Messenger")
        
        self.label1 = tk.Label(master, text="Enter your Facebook email:")
        self.label1.pack()
        
        self.entry1 = tk.Entry(master, width=50)
        self.entry1.pack()
        
        self.label2 = tk.Label(master, text="Enter your Facebook password:")
        self.label2.pack()
        
        self.entry2 = tk.Entry(master, show="*", width=50)
        self.entry2.pack()

        self.button1 = tk.Button(master, text="Login", command=self.login)
        self.button1.pack()
        
        
        self.label3 = tk.Label(master, text="Enter the message:")
        self.label3.pack()
        
        self.entry3 = tk.Entry(master, width=50)
        self.entry3.pack()
        
        self.label4 = tk.Label(master, text="Select recipients:")
        self.label4.pack()
        # please write all the names in the names.txt file of the people you want to send message
        # Note::::1)The same should be same as fb user name 
        # 2) If there is two or more same names then also only one random will be selected
        #3) Uid can be used to remove this.......
        with open("G:/fb chat bot/names.txt") as f:
            names = [line.strip() for line in f]
        for i, name in enumerate(names):
            check_var = tk.IntVar()
            check_button = tk.Checkbutton(master, text=name, variable=check_var)
            check_button.pack()
            self.check_buttons[f"check{i+1}"] = (check_button, check_var)
        
        self.button2 = tk.Button(master, text="Send", command=self.send_message, state=tk.DISABLED)
        self.button2.pack()
        
        # Hide the message-related widgets
        self.label3.pack_forget()
        self.entry3.pack_forget()
        self.label4.pack_forget()
        for check_button, _ in self.check_buttons.values():
            check_button.pack_forget()
        self.button2.pack_forget()
        
    def login(self):
        email = self.entry1.get()
        password = self.entry2.get()
        
        # Initialize the client
        try:
            self.client = fbchat.Client(email, password)
            success_label = tk.Label(self.master, text="Login successful!")
            success_label.pack()
            self.button2.config(state=tk.NORMAL)
            if self.error_label is not None:  # Check if error label exists
                self.error_label.destroy() 
            
            # Hide the login-related widgets
            self.label1.pack_forget()
            self.entry1.pack_forget()
            self.label2.pack_forget()
            self.entry2.pack_forget()
            self.button1.pack_forget()
            
            # Show the message-related widgets
            self.label3.pack()
            self.entry3.pack()
            self.label4.pack()
            for check_button, _ in self.check_buttons.values():
                check_button.pack()

            self.button2.pack()
            
        except fbchat.FBchatUserError:
            if self.error_label is None:  # Check if error label does not exist
                self.error_label = tk.Label(self.master, text="Login failed. Please try again.")
                self.error_label.pack()  # Create and display error label if it doesn't exist
           
        
        
    def send_message(self):
    # Delete previous success message, if it exists
        if hasattr(self, "success_label"):
            self.success_label.destroy()

        # Get the message text and recipients
        message_text = self.entry3.get()
        recipients = []

        # Loop through the check buttons to get the selected recipients
        for check_button, check_var in self.check_buttons.values():
            if check_var.get() == 1:
                # Get the name of the recipient from the check button text
                name = check_button.cget("text")
                # Find the user ID of the recipient
                user = self.client.searchForUsers(name)[0]
                recipients.append(user.uid)

        # Send the message to each recipient
        for recipient in recipients:
            self.client.send(Message(text=message_text), thread_id=recipient, thread_type=ThreadType.USER)

        # Display a success message
        if len(recipients) == 0:
            self.success_label = tk.Label(self.master, text="Please select at least one recipient.")
        elif len(recipients) == 1:
            self.success_label = tk.Label(self.master, text="Message sent to 1 recipient!")
        else:
            self.success_label = tk.Label(self.master, text="Message sent to {} recipients!".format(len(recipients)))

        self.success_label.pack()
root = tk.Tk()
root.geometry("300x200")
icon = tk.PhotoImage(file="g:fb chat bot\iconmonstr-facebook-messenger-1 (Custom).png")
iconsmall =  tk.PhotoImage(file="g:fb chat bot\iconmonstr-facebook-messenger-1 (Custom) (1).png")

root.iconphoto(False, icon, iconsmall)



root.configure(background='#ADD8E6')


app = FacebookMessengerApp(root)


root.mainloop()



