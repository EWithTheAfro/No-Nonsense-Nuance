import pytest
from project import get_file, get_word_count, get_semantics, get_feeling, get_detail


def test_get_file():
    # this text file meets all of the program requirements
    assert get_file("prideandprejudice.txt") == "prideandprejudice.txt"
    with pytest.raises(SystemExit):
        # file doesn't exist
        get_file("no.txt")
        # file is too long
        get_file("lifeofpiBAD.txt")
        # not a text file
        get_file("hello")


def test_get_word_count():
    # checking the counter works
    assert get_word_count("wordsample.txt") == 4
    assert get_word_count("loremipsum.txt") == 500


def test_get_semantics():
    # example of two semantics tests
    assert get_semantics("wordsample.txt") == "negative"
    assert get_semantics("prideandprejudice.txt") == "positive"


def test_get_feeling():
    # example of inference
    assert get_feeling("wordsample.txt") == ("neutral", [[{'label': 'neutral', 'score': 0.8933568000793457}, {'label': 'disgust', 'score': 0.03130398318171501}, {'label': 'anger', 'score': 0.02235930599272251}, {
        'label': 'fear', 'score': 0.022121353074908257}, {'label': 'surprise', 'score': 0.020261215046048164}, {'label': 'sadness', 'score': 0.005417149513959885}, {'label': 'joy', 'score': 0.005180109292268753}]])


def test_get_detail():
    # example of reformatted inference data
    assert get_detail([[{'label': 'neutral', 'score': 0.8933568000793457}, {'label': 'disgust', 'score': 0.03130398318171501}, {'label': 'anger', 'score': 0.02235930599272251}, {'label': 'fear', 'score': 0.022121353074908257}, {'label': 'surprise', 'score': 0.020261215046048164}, {'label': 'sadness', 'score': 0.005417149513959885}, {'label': 'joy', 'score': 0.005180109292268753}]]) == ([
        "😐Neutral contributes 89%",
        "🤢Disgust contributes 3%",
        "😡Anger contributes 2%",
        "😨Fear contributes 2%",
        "😯Surprise contributes 2%",
        "😭Sadness contributes 1%",
        "😁Joy contributes 1%"
    ])
