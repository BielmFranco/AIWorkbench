def process_events(events):
    seen = set()
    result = []
    for event in events:
        if event['event_id'] not in seen:
            seen.add(event['event_id'])
            result.append(event['receipt'])
    return result
