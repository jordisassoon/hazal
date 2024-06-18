HAZAL

```
python src/train.py experiment=tt_thumos data=thumos model.video_path=data/ model.split=10 model.setting=50 data.nsplit=10 exp_name=exp_0

python utils/false_positive_analysis.py --ground_truth_filename data/annotations/thumos14.json --prediction_filename data/annotations/full_t3al.json --output_folder out/ --is_thumos14

python adapt.py --origin_path data/out/full_predicted.csv --destination_path data/annotations/full_t3al.json

python analyze.py --annotations_path data/annotations/thumos_anno_action.json --predictions_path data/out/full_predicted.csv

python analyze.py --annotations_path data/annotations/thumos_anno_action.json --predictions_path data/out/full_predicted.csv --confusion_path out/confusion.csv
```