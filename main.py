import glob
import os
import librosa
import numpy as np
import soundfile
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from pydub import AudioSegment


def extract_feature(file_name, mfcc, chroma, mel):
    # SoundFile can read and write sound files
    with soundfile.SoundFile(file_name) as sound_file:
        x = sound_file.read(dtype="float64")
        sample_rate = sound_file.samplerate
        if chroma:
            # analyse voice pattern
            # Calculate the absolute value element-wise np.abs
            # Short-time Fourier transform represents a signal in the time-frequency
            # domain by computing discrete Fourier transforms (DFT) over short overlapping windows
            stft = np.abs(librosa.stft(x))
            result = np.array([])
        # Mel Frequency Cepstral Coefficient, represents the short-term power spectrum of a sound
        if mfcc:
            # Sampling rate or sampling frequency defines the number of samples per second (or per other unit)
            # taken from a continuous signal to make a discrete or digital signal
            mfccs = np.mean(librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=40).T, axis=0)
            # hstack() stacks arrays in sequence horizontally (in a columnar fashion)
            result = np.hstack((result, mfccs))
        # Pertains to the 12 different pitch classes
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        # Mel Spectrogram Frequency
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(x, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
    return result


# Emotions in the RAVDESS dataset
emotions = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

# Emotions to observe
# observed_emotions = ['angry']


# Load the data and extract features for each sound file
# def load_data(test_size=0.2):
#     #feature describe the vioce recording честота
#     x, y = [], []
#     # The glob module finds all the pathnames matching a specified pattern
#     for file in glob.glob("C:\\University\\3rd year\\3rd Year Project\\SpeechEmotionRec\\speech-emotion-recognition-ravdess-dataset\Actor_*\\*.wav"):
#         # To read or write files see open(), and for accessing the filesystem see the os module
#         file_name = os.path.basename(file)
#         # .split(String) will take a single string and split it into an array based on a value supplied as a parameter.
#         # The number in the square braces [0] is requesting an item location in the array
#         emotion = emotions[file_name.split("-")[2]]
#         if emotion not in observed_emotions:
#             continue
#         feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
#         # x holds the features
#         x.append(feature)
#         # y holds the emotions
#         y.append(emotion)
#     return train_test_split(np.array(x), y, test_size=test_size, random_state=9)

def load_train_data():
    x, y = [], []
    # The glob module finds all the path names matching a specified pattern
    for file in glob.glob(
            "C:\\University\\3rd year\\3rd Year Project\\SpeechEmotionRec\\speech-emotion-recognition-ravdess-dataset"
            "\Actor_*\\*.wav"):
        # To read or write files see open(), and for accessing the filesystem see the os module
        file_name = os.path.basename(file)
        emotion = emotions[file_name.split("-")[2]]
        if emotion not in emotions.values():
            continue
        feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    return np.array(x), y


def load_test_data():
    x, y = [], []
    for file in glob.glob(
            "C:\\University\\3rd year\\3rd Year Project\\SpeechEmotionRec\\interview_recordings\\Actor_*\\*.wav"):
        emotion_basename = os.path.basename(file)
        emotion = emotions[os.path.splitext(emotion_basename)[0]]

        # Convert WAV file from stereo to mono(i.e. fix problem with file encoding)
        sound = AudioSegment.from_wav(os.path.abspath(file))
        sound = sound.set_channels(1)
        sound.export(os.path.abspath(file), format="wav")

        feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    return np.array(x), y


# def load_interview_data(test_size=0.2):
#     x, y = [], []
#     # The glob module finds all the pathnames matching a specified pattern
#     for file in glob.glob("C:\\Users\\Irina\\OneDrive - University of Southampton\\Documents\\Sound recordings")
#         file_name = os.path.basename(file)

# formats_to_convert = ['.m4a']
# dirPath = 'C:\\Users\\Irina\\OneDrive - University of Southampton\\Documents\\Sound recordings'
#
# for (dirPath, dirNames, filenames) in os.walk("M4a_files/"):
#     for filename in filenames:
#         if filename.endswith(tuple(formats_to_convert)):
#
#             filepath = dirPath + '/' + filename
#             (path, file_extension) = os.path.splitext(filepath)
#             file_extension_final = file_extension.replace('.', '')
#             try:
#                 track = AudioSegment.from_file(filepath, file_extension_final)
#                 wav_filename = filename.replace(file_extension_final, 'wav')
#                 wav_path = dirPath + '/' + wav_filename
#                 print('CONVERTING: ' + str(filepath))
#                 file_handle = track.export(wav_path, format='wav')
#                 os.remove(filepath)
#             except:
#                 print("ERROR CONVERTING " + str(filepath))


def main():
    x_train, y_train = load_train_data()
    x_test, y_test = load_test_data()

    # Initialize the Multi Layer Perceptron Classifier
    model = MLPClassifier(alpha=0.0001, batch_size=100, epsilon=1e-08, hidden_layer_sizes=15,
                          solver='adam', max_iter=500, activation='logistic')

    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print(y_pred)

    # Setting parameters for Grid Search
    # parameters = {'solver': ['adam'],
    #               'max_iter': [500],
    #               'hidden_layer_sizes': [15],
    #               'activation': ['logistic', 'tanh', 'relu'],
    #               'alpha': [0.0001],
    #               'batch_size': [100]
    #               }

    # Train the model
    model.fit(x_train, y_train)
    # Predict for the test set
    y_pred = model.predict(x_test)

    # clf = GridSearchCV(MLPClassifier(), parameters, n_jobs=-1)
    # clf.fit(x_train, y_train)
    # print(clf.score(x_train, y_train))
    # print(clf.best_params_)

    # Calculate the accuracy of our model
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)

    # Print the accuracy
    print("Accuracy: {:.2f}%".format(accuracy * 100))


if __name__ == '__main__':
    main()
