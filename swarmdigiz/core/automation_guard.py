# -*- coding: utf-8 -*-

"""
SwarmDigiz Automation Guard

Prevents duplicate automated actions such as:
- duplicate campaigns
- duplicate SMS
- duplicate emails
- duplicate follow-ups
"""

from datetime import datetime, timedelta

# memory guard (per run)
_guard_cache = {}


def _key(action_type, identifier):
    return f"{action_type}:{identifier}"


def allow(action_type, identifier, cooldown_minutes=10):

    k = _key(action_type, identifier)

    now = datetime.utcnow()

    if k not in _guard_cache:
        _guard_cache[k] = now
        return True

    last_run = _guard_cache[k]

    if now - last_run > timedelta(minutes=cooldown_minutes):
        _guard_cache[k] = now
        return True

    return False