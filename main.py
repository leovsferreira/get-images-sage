from waggle.plugin import Plugin
from waggle.data.vision import Camera
import json
import time
import pytz
from datetime import datetime

def get_chicago_time():
    chicago_tz = pytz.timezone('America/Chicago')
    return datetime.now(chicago_tz).isoformat()

def main():
    start_time = get_chicago_time()
    
    with Plugin() as plugin:
        with Camera("bottom_camera") as camera:
            snapshot = camera.snapshot()
            timestamp = snapshot.timestamp

            snapshot.save("snapshot.jpg")
            plugin.upload_file("snapshot.jpg", timestamp=timestamp)
            
            finish_time = get_chicago_time()
            
            snapshot_dt = datetime.fromtimestamp(timestamp / 1e9, tz=pytz.UTC)
            chicago_snapshot_time = snapshot_dt.astimezone(pytz.timezone('America/Chicago')).isoformat()
            
            timing_data = {
                "plugin_start_time_chicago": start_time,
                "plugin_finish_time_chicago": finish_time,
                "image_timestamp_chicago": chicago_snapshot_time,
                "image_timestamp_ns": timestamp
            }
            
            plugin.publish("plugin.timing", json.dumps(timing_data), timestamp=timestamp)

if __name__ == "__main__":
    main()