class TokenManager:
    @staticmethod
    def can_fire(transition):
        """Ελέγχει αν μια μετάβαση μπορεί να εκτελεστεί"""
        if not transition.inputs:  # Αν δεν υπάρχουν input places, μπορεί να εκτελεστεί άμεσα
            return True

        for place, tokens in transition.inputs.items():
            if place.tokens < tokens:
                return False  # Δεν μπορεί να εκτελεστεί γιατί ένα place δεν έχει αρκετά tokens
        return True

    @staticmethod
    def fire_transition(transition):
        """Εκτελεί μια μετάβαση αν είναι εφικτό και μεταφέρει τα tokens."""
        if not TokenManager.can_fire(transition):
            print(f"❌ Η μετάβαση {transition.name} δεν μπορεί να εκτελεστεί λόγω έλλειψης tokens.")
            return False

        # Αφαιρούμε tokens από τα input places ΜΟΝΟ αν όλα έχουν αρκετά
        for place, tokens in transition.inputs.items():
            place.tokens -= tokens

        # Αν δεν υπάρχουν output places, τα tokens χάνονται
        if not transition.outputs:
            print(f"🔥 Η μετάβαση {transition.name} εκτελέστηκε και κατανάλωσε tokens χωρίς έξοδο.")
            return True

        # Προσθέτουμε tokens στα output places
        for place, tokens in transition.outputs.items():
            place.tokens += tokens

        print(f"✔ Η μετάβαση {transition.name} εκτελέστηκε επιτυχώς.")
        return True
