DIALOG = {}

def get_state(user_id):
    return DIALOG.get(user_id, {"phase": "NEW", "missing": []})

def set_state(user_id, phase, missing=None):
    DIALOG[user_id] = {
        "phase": phase,
        "missing": missing or []
    }

def clear_state(user_id):
    DIALOG.pop(user_id, None)
