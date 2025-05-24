import time

log_file = "logs/app.log"

with open(log_file, 'w') as f:
    f.write("2025-05-24 08:00:01 INFO Application started\n")
    f.write("2025-05-24 08:00:02 ERROR NullPointerException at line 56\n")
    f.write("2025-05-24 08:00:03 ERROR NumberFormatException at line 103\n")

time.sleep(2)
with open(log_file, 'a') as f:
    f.write("2025-05-24 08:00:05 INFO User logged in\n")
    f.write("2025-05-24 08:00:06 ERROR NullPointerException at line 72\n")