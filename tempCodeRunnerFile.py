def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("SkyNet")
    root.geometry("1280x720")

    # Load and resize the background image
    try:
        image = Image.open("SkyNetBG1.jpeg")
        photo = ImageTk.PhotoImage(image.resize((1280, 720)))
        root.photo = photo
        background = tk.Label(root, image=photo)
        background.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Background image not found. Using plain background.")
        background = tk.Label(root, bg="black")
        background.place(relwidth=1, relheight=1)

    # Add heading "SkyNet"
    heading_label = tk.Label(
        root,
        text="SkyNet",
        font=("Helvetica", 40, "bold"),
        bg="black",
        fg="white"
    )
    heading_label.place(relx=0.5, rely=0.1, anchor="center")

    # Chat box
    text_box = tk.Text(root, height=20, width=80, wrap=tk.WORD)
    text_box.place(relx=0.5, rely=0.5, anchor="center")
    text_box.insert(tk.END, "Click the mic to start speaking and click again to stop.\n")

    # Load and resize the microphone image
    try:
        mic_image = Image.open("mic2.png")
        mic_photo = ImageTk.PhotoImage(mic_image.resize((100, 100)))
        root.mic_photo = mic_photo
        microphone_button = tk.Button(
            root,
            image=mic_photo,
            command=lambda: on_microphone_click(text_box),
            borderwidth=0,
        )
        microphone_button.place(relx=0.3, rely=0.8, anchor="center")
    except FileNotFoundError:
        print("Microphone image not found. Using text button.")
        microphone_button = tk.Button(
            root,
            text="Mic",
            command=lambda: on_microphone_click(text_box),
            borderwidth=0,
        )
        microphone_button.place(relx=0.3, rely=0.8, anchor="center")

    # Load and resize the pause image
    try:
        pause_image = Image.open("pause_img.jpeg")
        pause_photo = ImageTk.PhotoImage(pause_image.resize((100, 100)))
        root.pause_photo = pause_photo
        pause_button = tk.Button(
            root,
            image=pause_photo,
            command=pause_func,
            borderwidth=0,
        )
        pause_button.place(relx=0.7, rely=0.8, anchor="center")
    except FileNotFoundError:
        print("Pause image not found. Using text button.")
        pause_button = tk.Button(
            root,
            text="Pause",
            command=pause_func,
            borderwidth=0,
        )
        pause_button.place(relx=0.7, rely=0.8, anchor="center")

    # Start the Tkinter event loop
    root.mainloop()

# Start the GUI