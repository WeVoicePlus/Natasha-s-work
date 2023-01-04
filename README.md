## Following resources are included in this repo:
1. [Pipeline](https://github.com/WeVoicePlus/Natasha-s-work/blob/master/data/data.py) to upload annotated datasets to Azure CustomVision.
2. [iCrawler script](https://github.com/WeVoicePlus/Natasha-s-work/blob/master/img_crawler/icr.py) to webcrawl images to make datasets.
3. [Predict](https://github.com/WeVoicePlus/Natasha-s-work/blob/master/predict.py) a whole folder of images, instead of one by one in the portal.
4. [Masterlist](https://github.com/WeVoicePlus/Natasha-s-work/blob/master/CustomVision_observations.md) of all our observations/conclusions regarding CustomVisions AutoML parameters.
5. [Download](https://github.com/WeVoicePlus/Natasha-s-work/blob/master/download.py) your datasets from CustomVision.
6. [Helper functions for TFLite](https://github.com/WeVoicePlus/Natasha-s-work/blob/master/tflite_odml_dataprep.py) has functions for adding the metadata to the `.tflite` file and converting the [downloaded](https://github.com/WeVoicePlus/Natasha-s-work/blob/master/download.py) CustomVision data to csv for [TFLite model maker training.](https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/models/modify/model_maker/object_detection.ipynb)

Let me know if there's some other functionality you'd need, or just open an issue.
