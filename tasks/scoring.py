from datetime import date, datetime

def parse_date(d):
    if d is None:
        return None
    if isinstance(d, (date, datetime)):
        return d.date() if isinstance(d, datetime) else d
    # try common ISO formats
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y'):
        try:
            return datetime.strptime(d, fmt).date()
        except Exception:
            pass
    raise ValueError(f'Unrecognized date format: {d}')

def calculate_task_score(task_data, strategy='balanced'):
    """Return (score, breakdown_dict).
    Strategies: 'balanced', 'deadline', 'quickwins' - alter weights.
    """
    # defaults and safety
    importance = int(task_data.get('importance') or 5)
    estimated = float(task_data.get('estimated_hours') or 1)
    due_raw = task_data.get('due_date')
    deps = task_data.get('dependencies') or []
    try:
        due = parse_date(due_raw) if due_raw else None
    except Exception:
        due = None

    today = date.today()
    score = 0
    breakdown = {}

    # Strategy weights
    if strategy == 'deadline':
        w_urgency = 0.6
        w_importance = 0.3
        w_effort = 0.1
    elif strategy == 'quickwins':
        w_urgency = 0.2
        w_importance = 0.3
        w_effort = 0.5
    else:  # balanced
        w_urgency = 0.4
        w_importance = 0.4
        w_effort = 0.2

    # Urgency (0..100)
    if due:
        days_until = (due - today).days
        if days_until < 0:
            urgency = 100  # overdue highest urgency
        else:
            # map days to urgency: soon -> high
            if days_until <= 1:
                urgency = 90
            elif days_until <= 3:
                urgency = 75
            elif days_until <= 7:
                urgency = 55
            elif days_until <= 14:
                urgency = 35
            else:
                urgency = 10
    else:
        urgency = 20  # no due date -> low urgency
    breakdown['urgency'] = urgency

    # Importance (scale 1-10 mapped to 0..100)
    importance_score = max(0, min(10, importance)) * 10
    breakdown['importance'] = importance_score

    # Effort -> we prefer smaller tasks for higher priority (quick wins)
    # Map estimated hours to effort_score where small hours -> higher number
    if estimated <= 0:
        effort_score = 100
    elif estimated < 1:
        effort_score = 90
    elif estimated < 2:
        effort_score = 70
    elif estimated < 4:
        effort_score = 50
    elif estimated < 8:
        effort_score = 30
    else:
        effort_score = 10
    breakdown['effort'] = effort_score

    # Dependency penalty/boost: if dependencies exist, lower priority until dependencies done
    if deps:
        dep_penalty = -30  # arbitrary penalty
    else:
        dep_penalty = 0
    breakdown['dep_penalty'] = dep_penalty

    # Combine using weights, normalize to ~0..100
    raw = (urgency * w_urgency) + (importance_score * w_importance) + (effort_score * w_effort) + dep_penalty
    # ensure positive
    score = max(0, raw)

    breakdown['raw'] = raw
    breakdown['final'] = score
    return score, breakdown
