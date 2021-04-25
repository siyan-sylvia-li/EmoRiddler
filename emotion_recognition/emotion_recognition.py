# Emotion Recognition System
import Algorithmia

API_key = "simQhlHNcBtEH+/5+PIeKYT3vv01"
client = Algorithmia.client(API_key)
count = 0
temp = {}


def emotion_recognition(image):
    input = {
        "image": image
    }

    algo = client.algo('util/SmartImageDownloader/0.2.20')
    algo.set_options(timeout=300)  # optional
    new_img_path = algo.pipe(input).result['savePath']

    input_emotion_recognition = {
        "image": new_img_path[0],
        "numResults": 1
    }

    algo = client.algo('deeplearning/EmotionRecognitionCNNMBP/1.0.1')
    result = algo.pipe(input_emotion_recognition).result

    # print(result)
    temp = result

    temp_1 = temp['results']
    temp_dict = temp_1[0]
    for x in temp_dict['emotions']:
        print(x['label'])


if __name__ == "__main__":
    emotion_recognition(
        image='https://www.pngfind.com/pngs/m/165-1659709_politically-incorrect-thread-happy-human-face-png.png')