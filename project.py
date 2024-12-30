import sys
import os
from transformers import pipeline
import re
from rich.console import Console

# allows use of rich to add colour and style to text :)
console = Console()

# This stops a warning coming up in the terminal when using the NLP models
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    # Welcome message and a few instructions
    console.print("─•~❉᯽ No Nonsense Nuance ᯽❉~•─", style="Cyan bold underline", justify="center")
    console.print("\nWelcome to N3: your reading comprehension assistant.\nN3 will read and analyse the semantics of your text for you. Simply upload your text file and N3 will tell you the overall tone of the text, the top emotions within the text, and more information if you wish.\n", justify="center")
    print("Rules and requirements:\n✅Ensure your file is in .txt format\n✅Ensure your text file is in the same folder as this program\n✅Maximum passage length is 500 words\n")

    # prompt the user for their file
    file = get_file(input("Paste your .txt file name: "))

    # if the file has passed all checks, use distilBERT model to get the semantics (positive, negative, neutral)
    semantics = get_semantics(file)

    # same as above, but now using roBERTa model to get the emotions (anger, disgust, joy, fear, sadness, neutral, surprise)
    feeling, more_data = get_feeling(file)

    # print the semantics and the number 1 feeling expressed in the text
    console.print(
        f"\nYour text is overall {semantics}, with it's top emotional hit being {feeling}.\n", style="cyan")

    # ask the user if they want more insights into the emotions of the text before quitting the program
    # infinite loop till the user types in a prompt that is either Y (yes) or N (no), case insensitively
    while True:

        option = input("Want more specifics? (Y/N): ").capitalize().strip()

        if option == "Y":
            break
        elif option == "N":
            sys.exit("Thank you for using N3 <3")
            break
        else:
            pass

    detail = get_detail(more_data)
    console.print(f"\nHere is a breakdown of the emotions in your text: \n", style="cyan")

    print("╔════════ ≪ °❈° ≫ ════════╗")
    for line in detail:
        print(f"{line}")
    print("╚════════ ≪ °❈° ≫ ════════╝\n")

    sys.exit("Thank you for using N3 <3\n")


def get_file(file: str) -> str:
    """Checks the user's file is a text file and less than 500 words.

    :param file: User's inputted file
    :type file: str
    :raise SystemExit: If file does not fulfil length or type requirements, or if it doesn't exist
    :return: The name of the user's file proivided it has passed the checks
    :rtype: str
    """

    # using os to split on the file extension
    filetype = os.path.splitext(file)

    try:
        if filetype[1] == ".txt":
            # to ensure that it isn't too long to be processed by the NLP models (both with 512 max word length)
            word_count = get_word_count(file)
            if word_count <= 500:
                return file
            else:
                sys.exit(":( Passage is too long: Max length of 500 words. Please reload the program.")
        else:
            sys.exit(":( Not a .txt file. Please reload the program.")

    except (FileNotFoundError):
        sys.exit(":( File does not exist in this folder. Please reload the program.")


def get_word_count(c: str) -> int:
    """Counts the number of words in the user's file

    :param c: The user's file name
    :type c: str
    :return: The number of words in the text (i.e. the length of the list of words extracted from the file)
    :rtype: int
    """

    # all non word characters
    pattern = r"[^\w]"

    with open(c, "r") as text:
        # get a list of just the words in the text, spaces seperating them all. this gets around words with cotractions like didn't --> didnt so it's counted as one word not two
        cleaned_file = re.sub(pattern, " ", text.read())

    # counts all the individual words
    return len(cleaned_file.split())


def get_semantics(s: str) -> str:
    """Classifies the semantics of the user's text

    :param s: The user's file name
    :type s: str
    :return: The best semantic match (i.e. the first key in the dictionary produced when using pipeline, the dictionary is contained in a list)
    :rtype: str
    """
    # loading the NLP model
    sentiment_pipeline = pipeline(
        "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    with open(s, "r") as text:
        # processing the file using distilBERT
        sentiment = sentiment_pipeline(text.read())

    # enter the list, access the value of the best semantic match (positive, negative, neutral)
    return sentiment[0]["label"].lower()


def get_feeling(f: str) -> tuple[str, list]:
    """Classifies emotions in the user's text into Ekman's 6 basic emotions and a neutral emotion.

    :param f: The user's file name
    :type f: str
    :return: The top-ranked emotion within the user's text and the entire list of dictionaries produced when using pipeline
    :rtype: tuple containing str and list
    """
    # loading the NLP model
    classifier = pipeline("text-classification",
                          model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

    with open(f, "r") as text:
        # processing the file using distilROBERTA
        feeling = classifier(text.read())

    # returns the strongest emotional match in the text, then returns the entire list of dictionaries for all 7 emotions and their relative presence in the text
    return feeling[0][0]["label"].lower(), feeling


def get_detail(d: list) -> list:
    """Format the emotion data in a user-friendly string.

    :param d: The list of dictionaries generated in get_feeling
    :type d: list
    :return: A list of strings with an emoji to reflect the emotion, the emotion, and the percentage representation
    :rtype: list
    """
    # list of dictionaries
    detailed_feelings = d[0]
    ranked = []
    emoji = {
        "Anger": "😡",
        "Disgust": "🤢",
        "Joy": "😁",
        "Fear": "😨",
        "Sadness": "😭",
        "Surprise": "😯",
        "Neutral": "😐"
    }

    for emotion in detailed_feelings:
        # store each emotion to be used as a key for the 'emoji' dictionary
        emotion_hit = emotion["label"].capitalize()
        # appends the matching emoji, the name of the emotion, and the percentage represntation. In ranked order thanks to the 'get_feeling' function
        ranked.append(
            f"{emoji[emotion_hit]}{emotion_hit} contributes {round(emotion["score"]*100)}%")

    return ranked


if __name__ == "__main__":
    main()
