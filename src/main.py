import tkinter as tk
import requests


class TwoColumnApp:
    def __init__(self, root):

        url = "http://127.0.0.1:8000"
        alerts = requests.get(url)
        self.alerts = alerts.json()

        self.root = root
        self.root.title("Two-Column Layout with Listbox")

        #Grid layout
        self.root.rowconfigure(0, weight=0)  # Headline row
        self.root.rowconfigure(1, weight=1)  # Main content row
        self.root.columnconfigure(0, weight=1, uniform="equals")  # Left column
        self.root.columnconfigure(1, weight=2, uniform="equals")  # Right column

        self.create_headline()

        self.create_listbox()

        self.create_detail_view()

    def create_headline(self):
        headline_frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10)
        headline_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        headline_label = tk.Label(headline_frame, text="Ilmatieteenlaitoksen varoitukset", font=("Arial", 24), fg="white",
                                  bg="lightblue")
        headline_label.pack(expand=True)

    def create_listbox(self):
        self.listbox_frame = tk.Frame(self.root, padx=10, pady=10)
        self.listbox_frame.grid(row=1, column=0, sticky="nsew")

        #Listbox
        self.listbox = tk.Listbox(self.listbox_frame, font=("Arial", 12))
        self.listbox.pack(expand=True, fill="both")

        #Listing the alerts
        count = 0
        for alert in self.alerts:
            count += 1
            self.listbox.insert(tk.END, "{}. {}".format(count, alert["title"]))

        self.listbox.bind("<<ListboxSelect>>", self.on_item_select)

    def create_detail_view(self):
        self.detail_frame = tk.Frame(self.root, bg="lightgray", padx=10, pady=10)
        self.detail_frame.grid(row=1, column=1, sticky="nsew")
        self.detail_label = tk.Label(self.detail_frame, text="Select an item to view details.", bg="lightgray",
                                     font=("Arial", 12))
        self.detail_label.pack(expand=True, fill="both")

    def on_item_select(self, event):
        selected_index = self.listbox.curselection()  # Get the selected item index
        index = None
        for i in selected_index:
            index = i

        if selected_index:
            selected_item = self.alerts[index]

            self.update_detail_view(selected_item)

    def update_detail_view(self, alert):
        # Clear previous details
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        areas = ", ".join(alert["areas"])


        #Show alert info
        tk.Label(self.detail_frame, text=alert["event"], font=("Arial", 14), bg="lightgray", wraplength=1000, justify="left").pack(anchor="w")
        tk.Label(self.detail_frame, text=f"Kuvaus: {alert['description']}", font=("Arial", 12), bg="lightgray", wraplength=1000, justify="left").pack(anchor="w")
        tk.Label(self.detail_frame, text=f"Paikat: {areas}", font=("Arial", 12), bg="lightgray", wraplength=1000, justify="left").pack(anchor="w")



#Main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = TwoColumnApp(root)
    root.mainloop()