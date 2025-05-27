import os
from waggle.plugin import Plugin
from waggle.data.vision import Camera


def main():
    shared_image_dir = "/app/shared_images"
    shared_image_path = os.path.join(shared_image_dir, "latest_snapshot.jpg")
    
    os.makedirs(shared_image_dir, exist_ok=True)
    
    with Plugin() as plugin:
        with Camera("bottom_camera") as camera:
            snapshot = camera.snapshot()
        
        timestamp = snapshot.timestamp
        
        snapshot.save(shared_image_path)
        
        plugin.upload_file(shared_image_path, timestamp=timestamp)


if __name__ == "__main__":
    main()