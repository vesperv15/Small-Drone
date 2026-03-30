import asyncio
import cv2
import numpy as np
import threading
import json
from bleak import BleakScanner
from milo_beyin import PID

class MiloMaster:
    def __init__(self, target_mac):
        self.target_mac = target_mac
        self.is_running = True
        
        # PID Kontrolcüleri
        self.x_pid = PID(kp=0.4, ki=0.01, kd=0.05)
        self.y_pid = PID(kp=0.4, ki=0.01, kd=0.05)
        self.z_pid = PID(kp=0.5, ki=0.01, kd=0.1)
        
        self.current_rssi = -70
        self.target_rssi = -55
        self.milo_x, self.milo_y, self.milo_z = 0, 0, 0

    def ble_callback(self, device, advertisement_data):
        if device.address == self.target_mac:
            self.current_rssi = advertisement_data.rssi

    async def bluetooth_dongusu(self):
        """Bluetooth taramasını bağımsız bir görev olarak çalıştırır[cite: 7, 8]"""
        print(f"Milo: Bluetooth radarı aktif... Hedef: {self.target_mac}")
        try:
            async with BleakScanner(self.ble_callback) as scanner:
                while self.is_running:
                    # Z ekseni (Mesafe) hesabını burada yapıyoruz
                    error_z = self.target_rssi - self.current_rssi
                    self.milo_z = self.z_pid.calculate(error_z)
                    await asyncio.sleep(0.1) # İşlemciyi yormayalım
        except Exception as e:
            print(f"Bluetooth Hatası: {e}")

    async def kamera_dongusu(self):
        """Kamera ve görüntü işlemeyi yönetir"""
        cap = cv2.VideoCapture(0)
        print("Milo: Gözler açıldı!")

        while self.is_running:
            ret, frame = cap.read()
            if not ret: break

            h, w, _ = frame.shape
            mx, my = w // 2, h // 2
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            maske = cv2.inRange(hsv, np.array([100, 150, 50]), np.array([140, 255, 255]))
            M = cv2.moments(maske)

            if M["m00"] != 0:
                hx, hy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
                self.milo_x = self.x_pid.calculate(hx - mx)
                self.milo_y = self.y_pid.calculate(hy - my)
                cv2.circle(frame, (hx, hy), 15, (0, 255, 0), -1)

            # Ekrana verileri yazdır
            self.ekran_arayuzu(frame, self.milo_x, self.milo_y, self.milo_z, mx, my)
            cv2.imshow("Milo Master Kontrol Paneli", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.is_running = False
            
            await asyncio.sleep(0.01)

        cap.release()
        cv2.destroyAllWindows()

    def ekran_arayuzu(self, frame, x, y, z, mx, my):
        cv2.drawMarker(frame, (mx, my), (255, 0, 0), cv2.MARKER_CROSS, 20, 2)
        cv2.putText(frame, f"MILO 3D STATUS", (10, 30), 1, 1.5, (255, 255, 255), 2)
        cv2.putText(frame, f"X (Roll): {int(x)} | Y (Pitch): {int(y)}", (10, 70), 1, 1.2, (0, 255, 0), 2)
        cv2.putText(frame, f"Z (Throttle): {int(z)} | RSSI: {self.current_rssi}", (10, 110), 1, 1.2, (0, 255, 0), 2)

    async def baslat(self):
        # İki görevi aynı anda başlatıyoruz
        await asyncio.gather(
            self.bluetooth_dongusu(),
            self.kamera_dongusu()
        )

if __name__ == "__main__":
    # ÖNEMLİ: Windows'ta Bluetooth sorunlarını aşmak için bu ayar kalmalı
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    with open ("config.json") as f:
        config= json.load(f)
    ADRES = config["TARGET_ADDRESS"]
    milo = MiloMaster(ADRES)
    asyncio.run(milo.baslat())