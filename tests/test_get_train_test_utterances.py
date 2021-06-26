from get_train_test_utterances import get_bookflight_utterances
import os


def test_is_file_frames_small():
    assert os.path.isfile("./P10_03_LuisModel/frames_small.json")

examples = get_bookflight_utterances("./P10_03_LuisModel/frames_small.json")

def test_size_bookflight_utterances():
    assert len(examples) == 10

def test_first_bookflight_utterance_text():
    assert examples[0]["text"] == "I want to go to san antonio from tijuana for 7 days"
