def select_passages(documents, tenant):
    return [d['id'] for d in documents if d['tenant']==tenant and d['current'] and not d['deleted']]
