import random
import json
import os
import time

# Files
WORDS_FILE = "words.json"
SCORES_FILE = "scores.json"

# Hangman ASCII
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\\  |
 / \\  |
     ===''']

# Load words
def load_words():
    with open(WORDS_FILE, "r") as f:
        return json.load(f)

# Load scores
def load_scores():
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "w") as f:
            json.dump({}, f)
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

# Save scores
def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

# Choose word based on difficulty
def choose_word(words, difficulty):
    return random.choice(words[difficulty]).upper()

# Display leaderboard
def display_leaderboard(scores):
    print("\n--- Leaderboard ---")
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for i, (user, score) in enumerate(sorted_scores[:10], 1):
        print(f"{i}. {user}: {score} points")
    print("-------------------\n")

# Provide hint (one random unguessed letter)
def provide_hint(word, guessed_letters):
    remaining = [c for c in word if c not in guessed_letters]
    if remaining:
        hint = random.choice(remaining)
        print(f"Hint: Try the letter '{hint}'")

def play_hangman():
    print("Welcome to Advanced Hangman!")
    username = input("Enter your name: ").strip()

    scores = load_scores()
    if username not in scores:
        scores[username] = 0

    words = load_words()

    while True:
        # Difficulty
        while True:
            difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
            if difficulty in words:
                break
            print("Invalid choice. Try again.")

        word = choose_word(words, difficulty)
        word_letters = set(word)
        guessed_letters = set()
        tries = 6
        round_score = 0

        print(f"\nYou have {tries} tries to guess the word.")

        start_time = time.time()

        while len(word_letters) > 0 and tries > 0:
            display_word = [letter if letter in guessed_letters else "_" for letter in word]
            print("\n" + " ".join(display_word))
            print(HANGMAN_PICS[6 - tries])
            print(f"Guessed letters: {' '.join(sorted(guessed_letters))}")

            # Offer hint if 3 tries left
            if tries == 3:
                use_hint = input("Do you want a hint? (y/n): ").lower()
                if use_hint == 'y':
                    provide_hint(word, guessed_letters)
                    tries -= 1  # Hint costs 1 try

            guess = input("Guess a letter: ").upper()
            if guess in guessed_letters:
                print("You already guessed that letter.")
            elif guess in word_letters:
                print("Good guess!")
                guessed_letters.add(guess)
                word_letters.remove(guess)
                round_score += 10
            else:
                print("Wrong guess!")
                guessed_letters.add(guess)
                tries -= 1

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        if tries == 0:
            print(HANGMAN_PICS[6])
            print(f"Game Over! The word was: {word}")
            round_score = max(round_score - 5, 0)
        else:
            print(f"Congratulations {username}! You guessed the word: {word}")

        print(f"Round score: {round_score}, Time taken: {duration} seconds")
        scores[username] += round_score
        save_scores(scores)
        display_leaderboard(scores)

        replay = input("Play again? (y/n): ").lower()
        if replay != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_hangman()
