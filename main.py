from waggle.plugin import Plugin
from waggle.data.vision import Camera

def main():
    with Plugin() as plugin:
        with Camera() as camera:
            snapshot = camera.snapshot("bottom_camera")
            timestamp = snapshot.timestamp
            print("snapshot taken")
            snapshot.save("snapshot.jpg")
            plugin.upload_file("snapshot.jpg", timestamp=timestamp)

if __name__ == "__main__":
    main()