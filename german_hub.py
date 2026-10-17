import json
import random
from pathlib import Path


WORDS_FILE = Path(__file__).with_name("german_words.json")


def load_words():
	if not WORDS_FILE.exists():
		return []

	try:
		with WORDS_FILE.open(encoding="utf-8") as file:
			words = json.load(file)
	except (json.JSONDecodeError, OSError):
		print("I couldn't read your saved words. Starting with an empty list.")
		return []

	if not isinstance(words, list):
		print("Your saved word list isn't in the expected format. Starting fresh.")
		return []
	return words


def save_words(words):
	with WORDS_FILE.open("w", encoding="utf-8") as file:
		json.dump(words, file, ensure_ascii=False, indent=2)


def enter_words(words):
	print("Enter a German word and its meaning. Leave the German word blank to finish.")
	while True:
		german = input("German word: ").strip()
		if not german:
			break

		meaning = input("Meaning: ").strip()
		if not meaning:
			print("The meaning can't be blank. Please enter that word again.")
			continue

		words.append({"german": german, "meaning": meaning})
		save_words(words)
		print(f"Saved: {german} = {meaning}")


def quiz(words):
	if not words:
		print("You haven't added any words yet. Choose 'enter words' first.")
		return

	questions = words[:]
	random.shuffle(questions)
	correct = 0

	for entry in questions:
		answer = input(f"German for '{entry['meaning']}': ").strip()
		if answer.casefold() == entry["german"].strip().casefold():
			print("Correct!")
			correct += 1
		else:
			print(f"Not quite. The German word is: {entry['german']}")

	print(f"You got {correct} out of {len(questions)} correct.")


def main():
	words = load_words()

	while True:
		choice = input("Would you like to 'quiz', 'enter words', or 'quit'? ").strip().casefold()
		if choice == "quiz":
			quiz(words)
		elif choice == "enter words":
			enter_words(words)
		elif choice == "quit":
			print("Viel Erfolg!")
			break
		else:
			print("Please type 'quiz', 'enter words', or 'quit'.")


if __name__ == "__main__":
	main()