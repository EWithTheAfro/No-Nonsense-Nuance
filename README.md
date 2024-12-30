# No Nonsense Nuance: emotional inference reading comprehension assistant
## Description
**No Nonsense Nuance (N3)** is a program that analyses the overall emotion of a piece of text; be it a single sentence or a whole paragraph. It runs in the terminal window with some simple styling using the rich library. N3 tells the user the top emotion associated with the text then offers a more detailed breakdown with percentages per category (Ekman’s 6 basic emotions: anger, joy, sadness, disgust, fear, surprise and an added neutral emotion), making use of natural language processing to do so. N3 was designed for use by those with additional learning needs as an aid for reading comprehension and writing about the moods within a text.

**Project structure:**
* project.py (The main script for the program; contains plenty of comments and doctrings to explain functionality)
* test_project.py (Unit tests for the 5 functions in project.py)
* README.md
* requirements.txt

## Rationale
In my work as a private tutor, I have worked with students of all ages and abilities. Yet, when writing about literature, one common challenge all students face is effectively analysing the mood of a text. Very often the difficulty lies in simply getting started: when faced with a block of text, how do you go about determining the semantics? I have observed that this problem is exacerbated when students have additional learning needs like ASD which affects their ability to process emotions and read social cues. They certainly have the ability to write about these deeper inferences, but struggle with finding that starting point. Thus the idea for N3 was born.

When I teach my students how to begin commenting on moods within text, I start by simply discussing the extract. I first have them determine whether the text is conveying overall positive or negative feelings. Then once we have decided on the tone, I will show them various adjectives or abstract noun connotations they could use to describe the text or they come up with these themselves. This then gives them a foundation to start their writing as we’ve done the hard work together.

N3 works in a similar way. It takes a text file uploaded by the user and prints the tone of the text, the top emotion associated with it, and then leaving it up to the user if they'd like a more detailed breakdown with the percentage representation of each of Ekman's 6 basic emotions and the neutral category. Please see the *'Functions'* section for a more deailed explaination of N3's functionality.
## Packages, libraries, and modules
N3 makes use of 6 packages/libraries and 1 additional framework to work with the NLP. 3 libraries are now built-in to python (**os, sys, and re**); **pytest** is only used for unit tests in test_project.py. The three remaining are as follows:
* **rich:** Used to style the terminal window with colours, align the text, and make the title bold. Read more about it here: https://rich.readthedocs.io/en/stable/ (Module)
* **transformers:** From Hugging Face. This allows N3 to make use of pretrained ML models to get the semantics and emotions of the text. Read more about it here: https://huggingface.co/docs/transformers/en/index (Module)
* **pytorch:** This is only installed so that the NLP models can function (Framework)

All packages can be installed using:
```
pip install -r requirements.txt
```
## Functions
The following details the functions found within the project.py file.
### main()
The main function acts as the hub for printing text to the terminal. The program starts by printing a brief welcome message and reminders about the file users upload. It calls the *get_file* function, and if that passes then it calls the *get_semantics* and *get_feeling* functions to allow it to print to the user the overall tone and the top emotion as an f-string. It then conatins a while loop to ask the user if they'd like more information or to end the program; if they don't input y or n (case-insensitively) then the user is reprompted. At this stage, the program will either end with sys.exit or if the user does want more details, main will call the *get_detail* function, and lastly print out the ranked emotions with some fancy terminal styling.
### get_file(_str_)
The get_file fuction runs checks on the file submitted by the user. This file is passed to the function as an argument. The file must be a .txt file and it must be less than 500 words in length. In order to check the length, get_file will call *get_word_count*. If it doesn’t meet those requirements (or the file does not exist in the same folder) then it exits the program with the appropriate message using sys.exit()
### get_word_count(_str_)
The get_word_count function counts the words in the file. This file is passed to the function as an argument. It first cleans the data, i.e. opens the file and uses re.sub to remove all of the punctuation marks; this avoids the bug of counting words such as didn’t or mustn’t as two separate words (separated by the apostrophe). Then with the cleaned data it calls str.split to create a list with all the words, no spaces or punctuation. Finally, it returns the length of the list which is equal to all the words in the text file.
### get_semantics(_str_)
The get_semantics function uses Hugging Face transformers’ pipeline function to analyse the semantics of the text in the supplied text file (passed to the function as an argument), using the distilBERT pre-trained model. Returns the overall semantic positive/negative/neutral which is the first key in the dictionary produced by the pipeline classifier.
### get_feeling(_str_)
The get_feeling function works very similarly to get_semantics, instead using Jochen Hartmann’s pre-trained distilRoBERTa model (Jochen Hartmann, "Emotion English DistilRoBERTa-base". https://huggingface.co/j-hartmann/emotion-english-distilroberta-base/, 2022.) This function returns the entire list of dictionaries produced by the classifier (key/value pairs of the emotion and it’s confidence score) and the top hit as its own returned value for ease of use in main().
### get_detail(_list_)
The get_detail function processes the list of dictionaries returned in the get_feeling function to make it more user-friendly. The list of dictionaries is passed as an argument for this function. It contains a dictionary ‘emoji’ of which the keys match the 7 emotions classified by the distilRoBERTa model. The function uses the key “label” from the emotions dictionaries to access the emoji value. Then it appends f-strings with: the emoji, the emotion itself and the percentage representation in the text presented in a simple sentence such as “😁 Joy contributes 75%”. Returns the aforementioned list of strings. I chose to add the emoji along with the emotion itself to help with accessibility for users who struggle with additional learning needs such as dyslexia as seeing the pictoral representation can help in understanding the writtten words.
## Other files
* **test_project.py**: contains the unit tests for project.py and needs pytest to execute the tests. There is one test per function in project.py: each test has the same name as its project.py counterpart, just with test_ in front of it.
    * *test_get_file* first tests a value that should pass all checks, hence returning True. Then it uses pytest.raises() menthod to ensure that our project.py code correctly exits the program if the file doesn't exit, if it isn't a text file, and if it is over the maximum word count.
    * *test_get_word_count* tests two sample texts, one very short and the other a 500 word lorem ipsum file. This check actually detected a bug in my code when I was first implementing get_word_count where it had accidentally been counting spaces that were substituted in place of the punctuation- very handy!
    * *test_get_semantics* tests two different extracts which are obviously very negative and very positive to ensure the code is classifying them correctly
    * *test_get_feeling* tests one sample text and compares the tuple that should be returned with what is actually generated.
    * *test_get_detail* works similarly to the above but this time takes the list of dictionaries from get_feeling (in project.py) and compares the list of strings that should be returned with what is actually generated.
* **requirements.txt**: contains a list of the libraries needed for N3 to run, please see the section *'Packages, libraries, and modules'* for more information
* A selection of text files to trial the code with
* This **README.md** file :)
## Design Choices, Project Limitations, and Future Iterations
Due to time constraints and my relative lack of experience, I had to stick with producing an MVP of what I’d like N3 to become in time.

**Natural Language Processing using Hugging Face transformers**
* Limitation: the distilBERT and distilRoBERTa models I used were pre-trained as I don’t have the knowledge of training NLP models myself. They are trained on shorter, opinion-based texts like tweets, reviews, films, etc but they accurate enough for my current purposes. A downside of these models is they only allow up to 512 words for accuracy, so i had to limit user text input to 500 words.
* Future iteration: I would like to train a model on 19th and 20th century literature that I commonly teach so that it’s semantics comments are specific to this context. I would also like to allow users to upload longer text files, like whole chapters of books.

**User interface design**
* Limitation: N3 currently runs in the terminal. I had researched how to implement a GUI, but again with my current skills this was a challenge! In order to focus on the more important NLP side of my project, I decided to stick to simply styling the terminal with the rich library so that it still looked appealing for users.
* Future iteration: I would like to design N3 as a full web app.

**Other ideas**
* Display the words that contributed to the top emotional hit for the text
* Option to display the percentages visually, potentially using a pie chart as learners with dyscalculia may find working with just the percentage too abstract
* Suggest most impactful quotes from the whole text submitted by the user
## References
Jochen Hartmann, "Emotion English DistilRoBERTa-base". https://huggingface.co/j-hartmann/emotion-english-distilroberta-base/, 2022.



