### Because CustomVision is a black box AutoML method, there's no documentation as to what loss, augmentations, sampling strategy is considered as parameters.
### Feel free to contribute your observations, and discuss possible conclusions and solutions

| Observation | Conclusion | Solution |
| ----------- | ---------- | -------- |
| Not annotating Every Instance -> poor performance | Hard negative sampling is used | Annotate every instance|
| Large amount of partial objects -> one object detected as many of the same object | ? | Higher IoU threshold or including more complete objects, depending on the dataset |