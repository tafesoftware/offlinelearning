import socket
import os
import sys
from app import create_app
from seed import seed_data
from seed_ethiopian_curriculum import seed_grade_11_12_subject_catalog

def get_local_ip():
    """Attempts to find the host machine's local LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't actually send data, just connects to determine local routing interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    # Ensure the database is seeded with the curriculum
    seed_data()
    seed_grade_11_12_subject_catalog()
    
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    local_ip = get_local_ip()

    print("\n" + "=" * 65)
    print("   OFFLINE LMS - RURAL LEARNING MANAGEMENT SYSTEM")
    print("=" * 65)
    print(f" * Localhost access:        http://127.0.0.1:{port}")
    print(f" * Classroom Wi-Fi / Hotspot: http://{local_ip}:{port}")
    print("=" * 65)
    print(" [!] Tell students to connect to your Wi-Fi hotspot and")
    print(f"     open their phone/tablet browser to: http://{local_ip}:{port}")
    print(" [!] To install as an app on student devices: tap 'Install App' banner")
    print("     or 'Add to Home Screen' in Chrome/Edge/Safari.")
    print("=" * 65 + "\n")

    app.run(host="0.0.0.0", port=port, debug=False)
