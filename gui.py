#import libraries
import tkinter as tk
from tkinter import Canvas, Button, Label, PhotoImage, messagebox  # Import messagebox module
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from keras.models import load_model

# Load the pre-trained model
model = load_model("model.h5")

# Define the GUI class
class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Digit Predictor")

        # Create the canvas to draw on
        self.canvas_width = 560
        self.canvas_height = 560
        self.canvas = Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Create a PIL Image object to draw on
        self.img = Image.new("L", (self.canvas_width, self.canvas_height), 255)
        self.draw = ImageDraw.Draw(self.img)

        # Bind mouse events to the canvas
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        self.canvas.bind("<ButtonRelease-1>", self.predict_digit)

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        # Create a clear button
        self.clear_button = Button(self.button_frame, text="Clear", command=self.clear_canvas, width=10)
        self.clear_button.pack(side="left")

        # Create a help button
        self.help_button = Button(self.button_frame, text="Help", command=self.show_help, width=10)
        self.help_button.pack(side="left")

        # Create a quit button
        self.quit_button = Button(self.button_frame, text="Quit", command=master.quit, width=10)
        self.quit_button.pack(side="left")

        # Create a label to display the predicted digit
        self.prediction_label = Label(master, text="")
        self.prediction_label.pack()

    # Draw on the canvas when the mouse is dragged
    def draw_on_canvas(self, event):
        x, y = event.x, event.y
        r = 20
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")
        self.draw.ellipse((x-r, y-r, x+r, y+r), fill=0)

    # Clear the canvas
    def clear_canvas(self):
        self.canvas.delete("all")
        self.img = Image.new("L", (self.canvas_width, self.canvas_height), 255)
        self.draw = ImageDraw.Draw(self.img)

    # Predict the digit when the mouse button is released
    def predict_digit(self, event):
        # Resize the image to 28x28 and invert the colors
        img_resized = self.img.resize((28, 28))
        img_inverted = ImageOps.invert(img_resized)

        # Convert the image to a numpy array
        img_array = np.array(img_inverted)
        img_array = img_array.astype("float32") / 255.0
        img_array = img_array.reshape((1, 28, 28, 1))

        # Make the prediction
        pred = model.predict(img_array)[0]
        digit = np.argmax(pred)
        accuracy = round(pred[digit]*100, 2)

        # Update the prediction label
        self.prediction_label.config(text="Predicted digit: {} with {}% accuracy".format(digit, accuracy))

    # Show the help information
    def show_help(self):
        help_text = "Draw a digit on the canvas and release the mouse button to predict the digit. Use the 'Clear' button to clear the canvas."
        messagebox.showinfo("Help", help_text)  # Use messagebox module


# Create the main window and start the GUI
root = tk.Tk()
gui = GUI(root)
root.geometry("800x700")  # Set the size of the window
root.mainloop()
