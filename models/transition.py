from models.place import Place

class Transition:
    def __init__(self, name: str, inputs: dict, outputs: dict):
        self.name = name
        self.inputs = inputs  # {Place: required tokens}
        self.outputs = outputs  # {Place: tokens to add}

    def is_enabled(self) -> bool:
        return all(place.tokens >= count for place, count in self.inputs.items())

    def fire(self):
        if not self.is_enabled():
            raise ValueError(f"Transition {self.name} cannot be fired.")

        print(f"🔥 Firing Transition: {self.name}")

        # Remove tokens from input places
        for place, count in self.inputs.items():
            print(f"🔴 Removing {count} tokens from {place.name} (Before: {place.tokens})")
            place.remove_tokens(count)
            print(f"✅ {place.name} now has {place.tokens} tokens")

        # Add tokens to output places (creating places if they do not exist)
        for place, count in self.outputs.items():
            if place.name not in self.inputs:  # Ensure the place exists
                place.tokens = 0  # Initialize place with zero tokens
            print(f"🟢 Adding {count} tokens to {place.name} (Before: {place.tokens})")
            place.add_tokens(count)
            print(f"✅ {place.name} now has {place.tokens} tokens")



    def __str__(self):
        return f"Transition({self.name})"
