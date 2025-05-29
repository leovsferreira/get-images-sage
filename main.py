from waggle.plugin import Plugin
from waggle.data.vision import Camera

def main():
    with Plugin() as plugin:
        try:
            available_cameras = Camera.list_cameras()
            print(f"Available cameras: {available_cameras}")
        except Exception as e:
            print(f"Error listing cameras: {e}")
        
        try:
            with Camera() as camera:
                snapshot = camera.snapshot()
                timestamp = snapshot.timestamp
                print("snapshot taken")
                snapshot.save("snapshot.jpg")
                plugin.upload_file("snapshot.jpg", timestamp=timestamp)
        except Exception as e:
            print(f"Camera error: {e}")

if __name__ == "__main__":
    main()