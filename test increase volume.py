from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def increase_volume(step=0.1):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + step)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Volume increased to {new_volume * 100:.0f}%")

increase_volume()
