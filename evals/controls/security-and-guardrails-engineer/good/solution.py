def can_refund(principal, charge):
    return isinstance(principal,dict) and isinstance(charge,dict) and principal.get('authenticated') is True and bool(principal.get('account_id')) and principal.get('account_id')==charge.get('owner')
