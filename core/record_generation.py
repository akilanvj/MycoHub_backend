import random
import json


# Function to generate random item names and descriptions
def generate_random_item():
    adjectives = ["Small", "Big", "Fast", "Slow", "Red", "Blue", "Green", "Yellow", "Bright", "Dark"]
    nouns = ["Widget", "Gadget", "Device", "Item", "Object", "Thing"]
    descriptions = [
        "This is a description for a random item.",
        "A unique and interesting item.",
        "An item of significant value.",
        "A commonly used item.",
        "An item with many features.",
        "A simple yet effective item.",
        "An item with a colorful design.",
        "A robust and durable item.",
        "An item that is easy to use.",
        "An item with high quality."
    ]

    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    description = random.choice(descriptions)
    return {"name": name, "description": description}


# Generate 25 random items
items = [generate_random_item() for _ in range(25)]

# Convert to JSON
items_json = json.dumps(items, indent=4)

# Print the JSON payload
print(items_json)