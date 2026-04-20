import os
import sys

# Redirect stdout and stderr to error.log
# This is more robust than the logging module for catching import-time crashes.
log_file = os.path.join(os.path.dirname(__file__), 'error.log')
sys.stdout = sys.stderr = open(log_file, 'a', buffering=1, encoding='utf-8')


print("\n--- Passenger WSGI Start ---")

sys.path.insert(0, os.path.dirname(__file__))

try:
    from server import app as application
    print("App imported successfully")
except Exception as e:
    import traceback
    traceback.print_exc()
    raise e

