def emotion_voting(emo_list):
    emotion_dict = {"happy": 0, "neutral": 0, "surprise": 0, "angry": 0, "sad": 0, "disgust": 0, "fear": 0}

    for item in emo_list:
        emotion_dict[item] = emotion_dict[item] + 1

    print(emotion_dict)

    my_keys = sorted(emotion_dict, key=emotion_dict.get, reverse=True)[:3]
    print(my_keys)
    print(type(my_keys))
    return my_keys


if __name__ == "__main__":
    list_of_emotions = ['happy', 'fear', 'disgust', 'neutral', 'sad', 'happy', 'sad', 'happy']
    emotion_voting(list_of_emotions)