import numpy as np
from ultralytics import YOLO
import json
import os
import time
from waggle.plugin import Plugin
from waggle.data.vision import Camera

def detect_objects(image, model):
    results = model(image)
    
    detections = []
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                cls = int(box.cls.item())
                cls_name = model.names[cls]
                conf = box.conf.item()
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                detections.append({
                    "class": cls_name,
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2]
                })
    
    return detections

def should_upload_image(timestamp, last_upload_time, upload_interval=60):
    if last_upload_time is None:
        return True
    
    time_diff = timestamp - last_upload_time
    return time_diff >= upload_interval

def main():
    print("=== Combined Object Detection + Image Upload Plugin ===")
    print("Object detection: every run (~10 seconds)")
    print("Image upload: every 60 seconds")
    
    os.environ['YOLO_CONFIG_DIR'] = '/tmp'
    
    print("Loading YOLO model...")
    model = YOLO("yolov8n.pt")
    print("YOLO model loaded successfully")
    
    last_upload_time = None
    run_count = 0
    
    with Plugin() as plugin:
        print("Plugin initialized")
        
        print("Taking snapshot from bottom_camera...")
        with Camera("bottom_camera") as camera:
            snapshot = camera.snapshot()
        
        timestamp = snapshot.timestamp
        run_count += 1
        
        print(f"Snapshot taken - Run #{run_count}")
        print(f"Image shape: {snapshot.data.shape}")
        print(f"Timestamp: {timestamp}")
        
        print("Running object detection...")
        detections = detect_objects(snapshot.data, model)
        print(f"Found {len(detections)} objects")
        
        class_counts = {}
        for det in detections:
            class_name = det["class"]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        print(f"Object counts: {class_counts}")
        
        detection_data = {
            "detections": detections,
            "counts": class_counts,
            "total_objects": len(detections),
            "run_number": run_count
        }
        
        print("Publishing object detection results...")
        plugin.publish("object.count", len(detections), timestamp=timestamp)
        plugin.publish("object.detections", json.dumps(detection_data), timestamp=timestamp)
        plugin.publish("plugin.run_count", run_count, timestamp=timestamp)
        
        for class_name, count in class_counts.items():
            plugin.publish(f"object.count.{class_name}", count, timestamp=timestamp)
        
        if should_upload_image(timestamp, last_upload_time, upload_interval=60):
            print("📸 Time to upload image (60+ seconds since last upload)")
            
            snapshot.save("snapshot.jpg")
            plugin.upload_file("snapshot.jpg", timestamp=timestamp)
            
            last_upload_time = timestamp
            plugin.publish("image.uploaded", "true", timestamp=timestamp)
            plugin.publish("image.upload_interval", 60, timestamp=timestamp)
            
            print("Image uploaded successfully")
        else:
            time_since_last = timestamp - last_upload_time if last_upload_time else 0
            print(f"Skipping image upload (only {time_since_last:.1f}s since last upload)")
            plugin.publish("image.uploaded", "false", timestamp=timestamp)
            plugin.publish("time_since_last_upload", time_since_last, timestamp=timestamp)
        
        print(f"Plugin run #{run_count} completed successfully")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Plugin failed: {e}")
        import traceback
        traceback.print_exc()