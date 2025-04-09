from fastapi import APIRouter
import socket

router = APIRouter()


@router.get("/server-info/")
def get_server_info():
    """Returns the server's IP address and port information"""
    hostname = socket.gethostname()

    try:
        # Create a dummy connection to get the active IPv4 address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS (won't actually send data)
        ip_address = s.getsockname()[0]
        s.close()
    except Exception as e:
        ip_address = "Error getting IP: " + str(e)

    return {
        "server_hostname": hostname,
        "server_ip_address": ip_address,
        "server_port": 8000  # Adjust this if needed
    }