import asyncio
from bleak import BleakScanner

class AidanDroneController:
    def __init__(self, target_mac): #[cite: 2]
        self.target_mac = target_mac #[cite: 2]
        self.alpha = 0.2  # Filtre katsayısı[cite: 2]
        self.filtered_rssi = -70.0 #[cite: 2]
        self.is_running = True #[cite: 2]
        self.current_mode = "FOLLOW" # Manuel, Takip, İniş vb.[cite: 2]

    def apply_filter(self, raw_rssi): #[cite: 2]
        # Üstel Hareketli Ortalama Filtresi[cite: 2]
        self.filtered_rssi = (self.alpha * raw_rssi) + (1 - self.alpha) * self.filtered_rssi #[cite: 2]
        return self.filtered_rssi #[cite: 2]

    async def handle_voice_commands(self): #[cite: 2]
        """AI Komut merkezi (Placeholder)""" #[cite: 2]
        while self.is_running: #[cite: 2]
            # Burada ileride mikrofon girişi olacak[cite: 2]
            await asyncio.sleep(5) #[cite: 2]

    def get_movement_command(self, rssi): #[cite: 2]
        """Sinyal gücüne göre hareket kararı""" #[cite: 2]
        if rssi > -50: #[cite: 2]
            return "DUR / GERİ GİT (Çok yakın!)" #[cite: 2]
        elif -65 < rssi <= -50: #[cite: 2]
            return "SABİT KAL (İdeal mesafe)" #[cite: 2]
        elif rssi <= -65: #[cite: 2]
            return "YAKLAŞ (Mesafe açılıyor)" #[cite: 2]
        return "BEKLE" #[cite: 2]

    async def detection_callback(self, device, advertisement_data): #[cite: 2]
        if device.address == self.target_mac: #[cite: 2]
            raw_rssi = advertisement_data.rssi #[cite: 2]
            smooth_rssi = self.apply_filter(raw_rssi) #[cite: 2]
            
            action = self.get_movement_command(smooth_rssi) #[cite: 2]
            print(f"Ham: {raw_rssi} | Filtreli: {smooth_rssi:.2f} | Karar: {action}") #[cite: 2]

    async def run(self): #[cite: 2]
        scanner = BleakScanner(self.detection_callback) #[cite: 2]
        print(f"Aslı, {self.target_mac} adresi için takip başladı...") #[cite: 2]
        
        await scanner.start() #[cite: 2]
        # Ses komutları ve tarama eşzamanlı çalışacak[cite: 2]
        await asyncio.gather( #[cite: 2]
            self.handle_voice_commands(), #[cite: 2]
            asyncio.sleep(30) # Şimdilik 30 saniye boyunca çalışsın[cite: 2]
        )
        await scanner.stop() #[cite: 2]

if __name__ == "__main__":
    # Çip adresi buraya gelecek[cite: 2]
    TARGET_ADDRESS = "TARAYICIDAN_BULDUGUN_ADRESI_BURAYA_YAZ" 
    drone = AidanDroneController(TARGET_ADDRESS) #[cite: 2]
    asyncio.run(drone.run()) #[cite: 2]