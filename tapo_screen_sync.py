import os
import asyncio
import sys
from tapo import ApiClient
from mss import mss
from PIL import Image
import numpy as np
import cv2
import colorsys
import configparser

config = configparser.ConfigParser()
config.read('.\config.ini')
TAPO_USERNAME = config['TapoSettings']['username']
TAPO_PASSWORD = config['TapoSettings']['password']
IP_ADDRESS = config['TapoSettings']['ip_address']

try:
    MONITOR_INDEX = int(sys.argv[1]) if len(sys.argv) > 1 else 1  # Varsayılan: 1
except ValueError:
    print("Gecersiz giris, varsayilan monitör (1) kullaniliyor.")
    MONITOR_INDEX = 1

async def setup_device():
    print("Cihaz baglanti denemesi basliyor...")
    try:
        client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
        print(f"ApiClient olusturuldu. Mevcut metodlar: {dir(client)}")
        device = await client.l530(IP_ADDRESS)
        print("Cihaz baglandi.")
        await device.on()
        print("Cihaz acildi.")
        return device
    except Exception as e:
        print(f"Baglanti hatasi: {str(e)}".encode('utf-8').decode('utf-8'))
        exit(1)

def get_dominant_color(monitor_index):
    with mss() as sct:
        if monitor_index >= len(sct.monitors):
            print(f"Hata: Monitör indeksi {monitor_index} mevcut değil!")
            exit(1)
        monitor = sct.monitors[monitor_index]
        print(f"Secilen monitör: {monitor}")
        width, height = monitor['width'], monitor['height']
        left = monitor['left'] + width // 4
        top = monitor['top'] + height // 4
        region = {"left": left, "top": top, "width": width // 2, "height": height // 2}
        screenshot = sct.grab(region)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img = img.resize((150, 150))
        pixels = np.float32(img).reshape(-1, 3)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, 5, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        r, g, b = int(dominant[0]), int(dominant[1]), int(dominant[2])
        print(f"Algilanan renk (RGB): ({r}, {g}, {b})")
        return r, g, b

async def smooth_transition(device, current_hue, current_saturation, target_hue, target_saturation, steps=10):
    for i in range(steps + 1):
        interp_hue = current_hue + (target_hue - current_hue) * (i / steps)
        interp_saturation = current_saturation + (target_saturation - current_saturation) * (i / steps)
        if interp_saturation == 0:
            interp_saturation = 1
        await device.set_hue_saturation(int(interp_hue), int(interp_saturation))
        await asyncio.sleep(0.05)

async def main():
    print("Ana dongu basliyor...")
    device = await setup_device()
    print("Cihaz hazir, renk senkronizasyonu basliyor...")
    current_hue = 0
    current_saturation = 1
    while True:
        try:
            r, g, b = get_dominant_color(MONITOR_INDEX)
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            target_hue = int(h * 360)
            target_saturation = int(s * 100)
            if target_saturation == 0:
                target_saturation = 1

            if abs(target_hue - current_hue) > 5 or abs(target_saturation - current_saturation) > 5:
                print(f"Yumuşak geçiş: {current_hue}, {current_saturation} -> {target_hue}, {target_saturation}")
                await smooth_transition(device, current_hue, current_saturation, target_hue, target_saturation)
                current_hue = target_hue
                current_saturation = target_saturation
            else:
                print(f"Küçük değişim, atlanıyor: {target_hue}, {target_saturation}")

            print(f"Renk ayarlandi: Hue={current_hue}, Saturation={current_saturation}, Monitör={MONITOR_INDEX}")
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Hata: {str(e)}".encode('utf-8').decode('utf-8'))
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())