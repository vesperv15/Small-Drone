import asyncio
from bleak import BleakScanner
from milo_beyin import PID
import json

class MiloController:
    def __init__(self, target_mac):
        self.target_mac = target_mac
        self.is_running = True
        self.current_mode = "FOLLOW"
        self.z_pid = PID(kp=0.5, ki=0.01, kd=0.1)
        self.target_rssi = -55

    async def handle_voice_commands(self):
        """Milo'nun ileride sesini duyacağı kısım"""
        while self.is_running:
            await asyncio.sleep(5)

    def get_movement_command(self, pid_output):
        """PID çıktısına göre Milo'nun motor kararını belirle"""
        if pid_output > 5:
            return "YAKLAŞ (Mesafe çok açıldı)"
        elif pid_output < -5:
            return "GERİ GİT (Çok yaklaştın!)"
        else:
            return "MESAFEYİ KORU (İdeal konum)"

    def detection_callback(self, device, advertisement_data):
        """Bluetooth verisi geldiğinde çalışan fonksiyon"""
        if device.address == self.target_mac:
            raw_rssi = advertisement_data.rssi

            error = self.target_rssi - raw_rssi
            milo_z_output = self.z_pid.calculate(error)
            
            action = self.get_movement_command(milo_z_output)
            print(f"Ham RSSI: {raw_rssi} | Milo Z Kararı: {int(milo_z_output)} | Aksiyon: {action}")

    async def run(self):
        # Callback'i scanner'a bağlıyoruz
        scanner = BleakScanner(self.detection_callback)
        print(f"Milo: {self.target_mac} için takip görevi başlatıldı, Aslı!")
        
        await scanner.start()
        try:
            while self.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.is_running = False
        
        await scanner.stop()

if __name__ == "__main__":
    with open("config.json", "r") as dosya:
        ayarlar = json.load(dosya)

    TARGET_ADDRESS = ayarlar["TARGET_ADDRESS"]
    milo = MiloController(TARGET_ADDRESS)
    asyncio.run(milo.run())