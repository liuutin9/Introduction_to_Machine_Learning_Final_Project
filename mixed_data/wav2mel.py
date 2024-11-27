import os
import librosa
import numpy as np
import soundfile as sf
from alive_progress import alive_bar

# 路徑設定
src_mixed_dir = "./"
src_clean_dir = "./"
target_mixed_dir = "../test_data/"
target_clean_dir = "../nature/clean/"

# MelSpectrogram參數 (勿動)
n_mels = 128                # 保持 Mel 頻譜圖的解析度
n_fft = 1024                # 提高 FFT 窗口大小以適配更多信號頻率
hop_length = 512            # 保持 hop_length 為 n_fft 的一半
win_length = 1024           # 窗口大小與 n_fft 保持一致（或設為 None 使用默認值）
sample_rate = 16000         # 採樣率保持不變，適合語音處理
f_max = sample_rate // 2    # 預設為 Nyquist 頻率，即 8000 Hz
duration = 5                # 音頻時長為 5 秒

def save_spectrogram_as_npy(spectrogram, save_path):
    """Save mel spectrogram as a NumPy array."""
    # os.system('cls')
    # print(f"Saving spectrogram as .npy file to {save_path}...")
    np.save(save_path, spectrogram)  # Save as .npy file

def sound_to_spectrogram(mixed_dir, clean_dir, sample_rate, duration, n_mels):
    
    length = len(os.listdir(mixed_dir))
    filenames = sorted(os.listdir(mixed_dir))

    with alive_bar(length) as bar:
        for filename in filenames:
            try:
                # 使用完整路徑
                mixed_path = os.path.join(mixed_dir, filename)
                # clean_path = os.path.join(clean_dir, filename)
                
                # 使用 soundfile 替代 librosa.load
                mixed_waveform, sr = librosa.load(mixed_path)
                # clean_waveform, sr = librosa.load(clean_path)
                
                # 如果採樣率不匹配，進行重採樣
                if sr != sample_rate:
                    mixed_waveform = librosa.resample(mixed_waveform, orig_sr=sr, target_sr=sample_rate)
                    # clean_waveform = librosa.resample(clean_waveform, orig_sr=sr, target_sr=sample_rate)
                
                # 如果指定了持續時間，裁剪音頻
                # if duration:
                #     samples = int(duration * sample_rate)
                #     mixed_waveform = mixed_waveform[:samples]
                #     clean_waveform = clean_waveform[:samples]
                
                # 生成梅爾頻譜圖
                mixed_mel_spectrogram = librosa.feature.melspectrogram(
                    y=mixed_waveform,
                    sr=sample_rate,
                    n_fft=n_fft,
                    hop_length=hop_length,
                    n_mels=n_mels
                )
                # clean_mel_spectrogram = librosa.feature.melspectrogram(
                #     y=clean_waveform,
                #     sr=sample_rate,
                #     n_fft=n_fft,
                #     hop_length=hop_length,
                #     n_mels=n_mels
                # )

                # 轉換為分貝刻度
                mixed_mel_spectrogram_db = librosa.power_to_db(
                    mixed_mel_spectrogram, 
                    ref=np.max, 
                    amin=1e-10  # 避免log(0)
                )
                # clean_mel_spectrogram_db = librosa.power_to_db(
                #     clean_mel_spectrogram, 
                #     ref=np.max, 
                #     amin=1e-10
                # )
                
                # Save spectrograms as .npy files
                mixed_npy_path = os.path.join(target_mixed_dir, f"{filename[:-4]}.npy")
                # clean_npy_path = os.path.join(target_clean_dir, f"{filename[:-4]}.npy")

                save_spectrogram_as_npy(mixed_mel_spectrogram_db, mixed_npy_path)
                # save_spectrogram_as_npy(clean_mel_spectrogram_db, clean_npy_path)
                
                bar()
                
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")
                continue
            
sound_to_spectrogram(src_mixed_dir, src_clean_dir, sample_rate, duration, n_mels)
