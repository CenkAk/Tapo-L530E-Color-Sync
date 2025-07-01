# Tapo L530E Renk Senkronizasyonu

Bu proje, Tapo L530E akıllı ampulün monitördeki baskın renklerle senkronize olmasını sağlayan bir Python scriptini içerir. Ampul, monitördeki renk değişimlerine göre dinamik olarak renk değiştirir ve yumuşak geçişler sunar.

## Gereksinimler
- **Python 3.12** veya daha yeni bir sürüm
- Aşağıdaki Python kütüphaneleri (komut istemi veya terminalde kurun):
  ```bash
  pip install tapo mss Pillow numpy opencv-python colorsys