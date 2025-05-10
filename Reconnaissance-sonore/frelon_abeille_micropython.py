# micropython_detect_frelon.py
import uos
import math
from ulab import numpy as np
from ulab import fft

# --- Lecture d'un WAV 16-bit mono minimal ---
def read_wav(path):
    """
    Lit un petit WAV 16-bit PCM mono stocké en LittleFS/SPIFFS.
    Renvoie (samplerate, samples_array).
    """
    with open(path, "rb") as f:
        # En-tête RIFF minimal
        riff = f.read(12)            # "RIFF" + size + "WAVE"
        fmt  = f.read(24)            # "fmt " + subchunk1Size + rest
        # extra subchunks parameters
        # On récupère sample rate (octets 24-28) et bits per sample (octets 34-36)
        sr = int.from_bytes(fmt[4:8], 'little')
        bits = int.from_bytes(fmt[14:16], 'little')
        if bits != 16:
            raise ValueError("Seuls les WAV 16-bit sont supportés")
        # On saute le reste jusqu'à "data" (non-robuste mais souvent ok)
        header = f.read(8)           # "data" + chunkSize
        data_size = int.from_bytes(header[4:8], 'little')
        # Lecture des échantillons
        raw = f.read(data_size)
    # Conversion en tableau int16
    n = data_size // 2
    samples = np.zeros(n, dtype=np.int16)
    for i in range(n):
        lo = raw[2*i]
        hi = raw[2*i+1]
        val = (hi << 8) | lo
        # convertir en signed
        if val & 0x8000:
            val = val - 0x10000
        samples[i] = val
    return sr, samples

# --- Fonction de détection de fréquence dominante simplifiée ---
def detecter_frelon(path_wav, frelon_band=(100, 300), amp_threshold=1000):
    """
    Retourne True si on détecte un pic d'amplitude > amp_threshold
    dans la bande frelon_band (Hz) pour le WAV donné.
    """
    sr, x = read_wav(path_wav)
    # Fenêtrage si très long : on peut réduire la taille
    N = len(x)
    # Convertir en float
    xf = x.astype(np.float32)
    # FFT
    X = fft.fft(xf)
    # Fréquences positives
    freqs = np.linspace(0, sr, N)
    half = N // 2
    X_abs = np.abs(X[:half]) * 2 / N
    freqs = freqs[:half]
    # Recherche dans la bande
    for i in range(half):
        f = freqs[i]
        if frelon_band[0] <= f <= frelon_band[1] and X_abs[i] >= amp_threshold:
            return True
    return False

# --- Exemple d'utilisation ---  
# stocke echantillons/abeille.wav et frelon.wav sur le filesystem
tests = {
    "abeille.wav": False,
    "frelon.wav": True,
}

for fname, attendu in tests.items():
    res = detecter_frelon("/echantillons/" + fname,
                         frelon_band=(150, 250),
                         amp_threshold=2000)
    print(fname, ":", res, "(attendu", attendu, ")")
