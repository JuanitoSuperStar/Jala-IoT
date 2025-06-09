import requests
import struct
from typing import List, Dict, Optional

def fetch_iot_data() -> List[Dict]:
    """Obtiene los datos del endpoint IoT"""
    url = "https://callback-iot.onrender.com/data"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return []

def decode_hex_data(hex_str: str) -> Optional[Dict[str, float]]:
    """Decodifica el string hexadecimal a valores de sensores"""
    try:
        # Convertir hex string a bytes
        byte_data = bytes.fromhex(hex_str)
        
        # Verificar que tenemos suficientes bytes (3 floats = 12 bytes)
        if len(byte_data) < 12:
            print(f"Datos insuficientes en hexData: {hex_str}")
            return None
        
        # Decodificar los 3 valores float (little-endian)
        temperatura, humedad, presion = struct.unpack('<fff', byte_data[:12])
        
        return {
            'temperature': temperatura,
            'humidity': humedad,
            'pressure': presion
        }
    except ValueError as e:
        print(f"Error decodificando hexData {hex_str}: {e}")
        return None

def process_iot_data():
    """Procesa y muestra los datos decodificados"""
    print("=== Decodificador de datos IoT ===")
    print("Obteniendo datos del endpoint...")
    
    data = fetch_iot_data()
    if not data:
        return
    
    print(f"\nSe encontraron {len(data)} registros")
    
    for idx, item in enumerate(data, 1):
        if 'hexData' not in item:
            continue
            
        print(f"\n--- Registro #{idx} ---")
        print(f"Dispositivo: {item.get('device', 'Desconocido')}")
        print(f"Timestamp: {item.get('timestamp', 'No disponible')}")
        print(f"hexData: {item['hexData']}")
        
        decoded = decode_hex_data(item['hexData'])
        if decoded:
            print("\nValores decodificados:")
            print(f"Temperatura: {decoded['temperature']:.2f} °C")
            print(f"Humedad: {decoded['humidity']:.2f} %")
            print(f"Presión: {decoded['pressure']:.2f} hPa")
        else:
            print("No se pudo decodificar hexData")

if __name__ == "__main__":
    process_iot_data()