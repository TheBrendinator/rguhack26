import numpy as np
import sounddevice as sd
import time
import cv2

# CODE USED IS FROM https://github.com/rubenmak/raspberry-pi-sense-hat-audio-spectrum-analyzer
# AI ASSISTANCE WAS USED

# -------------------------------
# SETTINGS
# -------------------------------

latest_levels = None
chunk = 4096
samplerate = 44100
channels = 1
update_interval = 0.03  # seconds


# LED matrix colors (RGB tuples)
yellow = (255, 255, 0)
red    = (255, 0, 0)
green  = (0, 204, 0)
e      = (0, 0, 0)  # empty
spectrum = [green, green, green, yellow, yellow, yellow, red, red]
matrix = [0]*8
weighting = [2, 8, 8, 16, 16, 32, 32, 64]

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def piff(val):
    return int(2 * chunk * val / samplerate)

def volume_frequency_range(power, freq_low, freq_high):
    try:
        volume = int(np.mean(power[piff(freq_low):piff(freq_high)]))
        return volume
    except:
        return 0

def calculate_levels(data):
    global matrix
    if channels > 1:
        data = data.mean(axis=1)
    if data.dtype == np.float32:
        data = (data * 32768).astype(np.int16)

    fourier = np.fft.rfft(data)
    fourier = np.delete(fourier, len(fourier)-1)
    power = np.abs(fourier)

    matrix[0] = volume_frequency_range(power, 0, 156)
    matrix[1] = volume_frequency_range(power, 156, 313)
    matrix[2] = volume_frequency_range(power, 313, 625)
    matrix[3] = volume_frequency_range(power, 625, 1250)
    matrix[4] = volume_frequency_range(power, 1250, 2500)
    matrix[5] = volume_frequency_range(power, 2500, 2750)
    matrix[6] = volume_frequency_range(power, 2750, 5000)
    matrix[7] = volume_frequency_range(power, 5000, 10000)

    # Scale for visible output
    matrix_scaled = np.divide(np.multiply(matrix, weighting), 50000)
    matrix_scaled = matrix_scaled.clip(0, 8)
    return matrix_scaled

# -------------------------------
# DISPLAY FUNCTIONS
# -------------------------------
def show_fullscreen(levels, scale=40):
    base_size = 8

    # Create 8x8 RGB image
    img = np.zeros((base_size, base_size, 3), dtype=np.uint8)

    for y in range(base_size):
        for x in range(int(levels[y])):
            img[y, x] = spectrum[x]

    # Scale image (pixel-perfect enlargement)
    img = cv2.resize(
        img,
        (base_size * scale, base_size * scale),
        interpolation=cv2.INTER_NEAREST
    )

    cv2.imshow("Spectrum", img)
    cv2.waitKey(1)

# -------------------------------
# SELECT MIC DEVICE
# -------------------------------
devices = sd.query_devices()

mic_device = 1

print(f"Using device: {devices[mic_device]['name']}")

# -------------------------------
# CALLBACK
# -------------------------------
def audio_callback(indata, frames, time_info, status):
    global latest_levels
    if status:
        print("Status:", status)
    latest_levels = calculate_levels(indata.copy())

# -------------------------------
# MAIN LOOP
# -------------------------------
with sd.InputStream(
    device=mic_device,
    channels=channels,
    samplerate=samplerate,
    blocksize=chunk,
    callback=audio_callback
):
    cv2.namedWindow("Spectrum", cv2.WND_PROP_FULLSCREEN)
    

    print("Listening... Press Ctrl+C to stop.")

    try:
        while True:
            if latest_levels is not None:
                show_fullscreen(latest_levels, scale=60)

            time.sleep(update_interval)

    except KeyboardInterrupt:
        print("Stopped.")
        cv2.destroyAllWindows()