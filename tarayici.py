import asyncio
from bleak import BleakScanner

async def identify_my_phone():
    print("Telefonunu alıcıya çok yaklaştır ve bekle...")
    devices = await BleakScanner.discover() #
    
    # Cihazları sinyal gücüne (RSSI) göre sıralayalım
    sorted_devices = sorted(devices, key=lambda d: d.rssi, reverse=True) #[cite: 2]
    
    print("\n--- Tespit Edilen Cihazlar (En Yakından En Uzağa) ---") #[cite: 2]
    for d in sorted_devices: #[cite: 2]
        name = d.name if d.name else "Bilinmeyen Cihaz" #[cite: 2]
        print(f"Adres: {d.address} | RSSI: {d.rssi} | İsim: {name}") #[cite: 2]

# Sadece bu dosyayı çalıştırdığımızda devreye girsin
if __name__ == "__main__":
    asyncio.run(identify_my_phone()) #[cite: 2]