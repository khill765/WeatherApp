# File: main.py
# Author: Kobe Hillman
# Date: 12/10/2023
# Description: This program allows a user to enter a city name
# and the program displays the current weather conditions in the city that they entered.

import tkinter as tk
import PIL.ImageTk
import requests
from PIL import Image, ImageTk


# Class that stores the base window of the application
# Including every frame, button, label, and entry on the app.
# This class also includes every function related to the app.
class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Function that clears text from the entry box
        def clear_text():
            city_entry.delete(0, 'end')

        # Function that removes the app image that displays app name, version, and icon
        def delete_app_label_image():
            app_image_label.destroy()

        # Function that resets the application to default
        def reset():
            city_entry.delete(0, 'end')
            results_label.config(text='')
            app_image_label.config(image=app_image)

        # Function that closes the application
        def exit_app():
            tk.Tk.destroy(self)

        # Function that gets the weather information from open weather map
        # And finds the proper weather icon
        def get_weather(city):
            weather_key = '991ce89b7a14c2c6286501cf13f00146'
            url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
            response = requests.get(url, params=params)
            weather = response.json()
            results_label['text'] = show_results(weather)

            icon_file_name = weather['weather'][0]['icon']
            open_icon(icon_file_name)

        # Opens the weather icon that was found by the get_weather function
        def open_icon(icon):
            size = int(results_frame.winfo_height() * 0.25)
            img = ImageTk.PhotoImage(Image.open('./img/' + icon + '.png').resize((size, size)))
            weather_icon.delete("all")
            weather_icon.create_image(0, 0, anchor='nw', image=img)
            weather_icon.image = img

        # Function to pull specific weather information from the OpenWeatherMap weather data.
        # Validates input by making sure it's the correct data type
        # as well as an actual city name. If not, it tells the user that it could not find that location.
        def show_results(weather):
            try:
                city_name = weather["name"]
                current_condition = weather["weather"][0]["description"]
                current_temp = weather["main"]["temp"]
                feels_like = weather["main"]["feels_like"]
                temp_max = weather["main"]["temp_max"]
                temp_min = weather["main"]["temp_min"]
                final_results = ('City: %s \nConditions: %s \nTemperature °F: %s \nFeels Like °F: %s \nHigh °F: %s '
                                 '\nLow °F: %s') % (city_name, current_condition.title(),
                                                    int(current_temp), int(feels_like), int(temp_max), int(temp_min))
            except:
                final_results = 'Could not find that location!'
            return final_results

        # Function that opens a "Thank you" window and is triggered when the "More Info" button is clicked.
        def open_app_info():
            window2 = tk.Toplevel()
            window2.title("Thank you!")
            window2.geometry("400x200")
            window2.iconbitmap("WeatherAppIcon.ico")
            window2.resizable(height=False, width=False)
            window2_label = tk.Label(window2, text="Thank you for using Ordinary Weather!\n"
                                                   "Please refer to the User Manual for instructions on how to use "
                                                   "this app.\nThank You!\n  - Kobe Hillman",
                                     font="Georgia, 9", bg="#ffffcc")
            window2_label.pack()
            x = window2.winfo_x()
            y = window2.winfo_y()
            window2.geometry("+%d+%d" % (x + 800, y + 200))
            window2.config(bg="#ffffcc")

        # Variables that store the height and width of the base window.
        h = 600
        w = 500
        # Creates the base canvas or window for the application
        window = tk.Canvas(self, height=h, width=w, bg='#ffeecc')
        window.pack()

        # Loads background image and resizes it
        image_path = PIL.Image.open('app_bg.png')
        image = PIL.ImageTk.PhotoImage(image_path.resize((500, 600)))

        # Creates a 'background' label and attaches the image to the label
        bg_label = tk.Label(image=image)
        bg_label.image = image
        bg_label.place(relwidth=1, relheight=1)

        # Changes title shown at the top of the application
        self.title("Ordinary Weather")
        # Adds custom icon at the top left of the application
        self.iconbitmap("WeatherAppIcon.ico")
        # Allows the application window to be resized/ allows user to resize the window
        self.resizable(False, False)

        # Creates the entry frame
        entry_frame = tk.Frame(self, bg='#ffffcc', bd=15)
        entry_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

        # Creates the color frame that holds the results_label
        results_frame = tk.Frame(self, bg='#ffffcc', bd=10)
        results_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

        # Button that clears text from the entry box
        clear = tk.Button(entry_frame, text="Clear", command=clear_text)
        clear.place(x=245, y=9, relheight=.50, relwidth=0.3)

        # Button that resets the application to default
        reset = tk.Button(entry_frame, text="Reset", bg='#ff9999', command=reset)
        reset.place(x=245, y=25, relheight=.50, relwidth=0.3)

        # Button that opens a second window and displays more information about the application
        more_info_button = tk.Button(bg_label, text="More Info", bg='#ffffcc', command=open_app_info)
        more_info_button.place(x=225, y=20)

        # Button that exits the application
        exit_button = tk.Button(bg_label, text="Exit", bg='#ffffcc', command=exit_app)
        exit_button.place(x=126, y=535, relwidth=.5)

        # Creates the "Go" button and triggers the "get_weather" function to get the weather data
        search_button = tk.Button(entry_frame, text="Search", command=lambda: get_weather(city_entry.get()))
        search_button.place(x=245, y=-7, relheight=.50, relwidth=0.3)

        # Creates the entry box and receives user input of the city name
        city_entry = tk.Entry(entry_frame, font=('Georgia', 20))
        city_entry.place(relwidth=0.65, relheight=1)

        # Prompts the user to enter a city name
        city_name_label = tk.Label(entry_frame, text="Enter a city:", bg='#ffffcc')
        city_name_label.place(x=-39, y=-14, relheight=0.4, relwidth=0.4)

        # Label that displays the weather information
        results_label = tk.Label(results_frame, font=('Georgia', 15), bg='#ffeecc')
        results_label.place(relwidth=1, relheight=1)

        # Label that displays the app name, version, and icon
        # Loads image that is shown in the results label (app name, version, icon)
        app_image_path = PIL.Image.open('app_label_image.png')
        app_image = PIL.ImageTk.PhotoImage(app_image_path)
        app_image_label = tk.Label(results_label, image=app_image, bg='#ffeecc')
        app_image_label.image = app_image
        app_image_label.place(relwidth=1, relheight=1)

        # Canvas that holds the weather condition specific icon
        weather_icon = tk.Canvas(results_label, bd=0, highlightthickness=0, bg='#ffeecc')
        weather_icon.place(relx=.38, rely=0, relwidth=1, relheight=0.5)


# Main Function
def main():
    WeatherApp().mainloop()


if __name__ == '__main__':
    main()
