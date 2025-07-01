from mss import mss

# Monitörleri listele
with mss() as sct:
    for i, monitor in enumerate(sct.monitors):
        print(f"Monitör {i}: {monitor}")