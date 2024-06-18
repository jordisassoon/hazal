def conform_to_detad(predictions):
    _dict = {
        "version": "VERSION 1.3",
        "external_data": {},
        'results': {}
    }
    for _, row in predictions.iterrows():
        video_id = row['video_id']
        if video_id not in _dict['results']:
            _dict['results'][video_id] = []
        _dict['results'][video_id].append({
            'score': row['score'],
            'segment': [row['start'], row['end']],
            'label': row['label']
        })
    return _dict