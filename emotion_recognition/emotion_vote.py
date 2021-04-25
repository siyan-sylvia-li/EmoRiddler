def emotion_voting(emo_list):
    emotion_dict = {"Happy": 0, "Neutral": 0, "Surpise": 0, "Angry": 0, "Sad": 0, "Disgust": 0, "Fear": 0}

    for item in emo_list:
        emotion_dict[item] = emotion_dict[item] + 1

    print(emotion_dict)

    my_keys = sorted(emotion_dict, key=emotion_dict.get, reverse=True)[:3]
    print(my_keys)
    print(type(my_keys))


if __name__ == "__main__":
    list_of_emotions = ['Happy', 'Fear', 'Disgust', 'Neutral', 'Sad', 'Happy', 'Sad', 'Happy']
    emotion_voting(list_of_emotions)