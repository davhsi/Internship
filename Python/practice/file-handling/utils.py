from datetime import datetime

def write_output(filepath, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filepath, "a") as f: 
        f.write(f"\n===== Run at {timestamp} =====\n")
        f.write(content)
        f.write("\n" + "="*40 + "\n")