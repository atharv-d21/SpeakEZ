import cv2
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading
import time

def record_video(frames, stop_event, camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        stop_event.set()
        return

    print("[Video] Recording started...")
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("[Video] Frame not captured.")
            break
        frames.append(frame)
        cv2.imshow('Video Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[Video] Recording stopped.")

def record_audio(audio_container, stop_event, fs=44100):
    print("[Audio] Recording started...")
    recorded_audio = []

    def callback(indata, frames, time_info, status):
        if stop_event.is_set():
            raise sd.CallbackStop()
        recorded_audio.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=2, callback=callback):
        while not stop_event.is_set():
            time.sleep(0.1) 

    audio_data = np.concatenate(recorded_audio, axis=0)
    audio_container.append(audio_data)
    print("[Audio] Recording stopped.")

def record_audio_video(duration=10, output_video='output.avi', output_audio='output.wav'):
    stop_event = threading.Event()
    video_frames = []
    audio_data_container = []
  
    video_thread = threading.Thread(target=record_video, args=(video_frames, stop_event))
    audio_thread = threading.Thread(target=record_audio, args=(audio_data_container, stop_event))

    video_thread.start()
    audio_thread.start()

    time.sleep(duration)
    stop_event.set()

    video_thread.join()
    audio_thread.join()

    if audio_data_container:
        fs = 44100
        write(output_audio, fs, audio_data_container[0])
        print(f"[Audio] Saved to {output_audio}")

    if video_frames:
        height, width, _ = video_frames[0].shape
        out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'XVID'), 20, (width, height))
        for frame in video_frames:
            out.write(frame)
        out.release()
        print(f"[Video] Saved to {output_video}")

    print("✅ Recording complete.")
