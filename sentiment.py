import tkinter as tk
from tkinter import messagebox

from textblob import TextBlob


# Function to perform sentiment analysis
def analyze_sentiment():
    # Get the input text
    input_text = text_input.get("1.0", tk.END).strip()

    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text for analysis.")
        return

    # Perform sentiment analysis using TextBlob
    blob = TextBlob(input_text)
    sentiment_score = blob.sentiment.polarity  # Sentiment polarity (-1 to 1)
    
    if sentiment_score > 0:
        sentiment = "Positive"
    elif sentiment_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Display the result
    result_label.config(text=f"Sentiment: {sentiment}")
    confidence_label.config(text=f"Confidence: {abs(sentiment_score) * 100:.2f}%")

# Set up the main window
root = tk.Tk()
root.title("Sentiment Analysis")
root.geometry("500x400")
root.config(bg="#f0f4f8")

# Header Label
header_label = tk.Label(root, text="Sentiment Analysis", font=("Arial", 20, "bold"), bg="#4A90E2", fg="white", pady=10)
header_label.pack(fill="x")

# Instructions
instructions_label = tk.Label(root, text="Enter text below and click 'Analyze Sentiment'", font=("Arial", 12), bg="#f0f4f8")
instructions_label.pack(pady=10)

# Textbox for input
text_input = tk.Text(root, height=5, wrap="word", font=("Arial", 12), padx=10, pady=10)
text_input.pack(pady=10, padx=20, fill="x")

# Analyze Button
analyze_button = tk.Button(root, text="Analyze Sentiment", font=("Arial", 14), bg="#4A90E2", fg="white", command=analyze_sentiment)
analyze_button.pack(pady=20)

# Result Section
result_label = tk.Label(root, text="Sentiment: ", font=("Arial", 14), bg="#f0f4f8")
result_label.pack(pady=5)

confidence_label = tk.Label(root, text="Confidence: ", font=("Arial", 14), bg="#f0f4f8")
confidence_label.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
