# Public Transport Monitoring with YOLOv5

Computer vision system for monitoring passenger occupancy and mask compliance
on public transport, publishing detection results to a cloud dashboard.

**Built on [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5) (GPL-3.0).**
This repository contains custom-trained models and application code layered on the
upstream YOLOv5 training and inference framework.

## What I built

- **Custom model training** — trained YOLOv5 detection models on a labelled dataset
  of [N images] for [passenger / mask] detection, reaching [X% mAP].
- **Telemetry pipeline** (`thingspeak_upload.py`) — publishes detection counts to a
  ThingSpeak endpoint over HTTP for time-series logging and remote monitoring.
- **Sensor integration** (`SensorReading.py`) — reads [sensor type] and combines it
  with vision output.
- **Evaluation** (`testing.py`) — runs inference over recorded video and reports results.

## Results

| Metric | Value |
|---|---|
| mAP@0.5 | [x] |
| Inference speed | [x] FPS on [hardware] |
| Dataset | [N] images, [N] classes |

Sample output: `result.mp4`

## Running it

```bash
pip install -r requirements.txt
python detect.py --weights best.pt --source test.mp4
python thingspeak_upload.py
```

## Limitations

- trained on a limited dataset; accuracy drops in low light
-  counting assumes a fixed camera angle

## Attribution

Training and inference scripts (`train.py`, `detect.py`, `val.py`, `export.py`,
`hubconf.py`) are from Ultralytics YOLOv5 and remain under GPL-3.0. Custom
application code, trained weights and integration work are my own.
