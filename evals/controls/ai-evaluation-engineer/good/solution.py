def grade_ticket(output, expected):
    if not isinstance(output,dict) or set(output)!={'ticket_id','category'}: return False
    return all(isinstance(output[k],str) and bool(output[k]) and output[k]==expected[k] for k in ('ticket_id','category'))
