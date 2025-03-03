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
            raise ValueError(f"Transition with name {self.name} can not be fired.")

        for place, count in self.inputs.items():
            place.remove_tokens(count)

        for place, count in self.outputs.items():
            place.add_tokens(count)

    def __str__(self):
        return f"Transition({self.name})"
