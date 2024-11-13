import threading

# Global variable to store the current data
current_data = None

# Lock to control access to the current_data
data_lock = threading.Lock()
