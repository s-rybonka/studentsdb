import rules
from rules import predicate


@predicate
def is_manager(account):
    return account.is_manager


rules.add_perm('manager', is_manager)
