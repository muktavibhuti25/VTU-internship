import random

def predict_waste(image_path):
    classes = ["Plastic", "Organic", "Metal", "Paper"]
    return random.choice(classes)