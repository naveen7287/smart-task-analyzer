from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .scoring import calculate_task_score

@csrf_exempt
def analyze(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Use POST with a JSON list of tasks.')
    try:
        payload = json.loads(request.body)
        strategy = request.GET.get('strategy','balanced')
        processed = []
        for t in payload:
            t = dict(t)  # copy to avoid mutating input
            if 'importance' not in t:
                t['importance'] = 5
            if 'estimated_hours' not in t:
                t['estimated_hours'] = 1
            try:
                score, breakdown = calculate_task_score(t, strategy=strategy)
            except Exception as e:
                score, breakdown = 0, {'error': str(e)}
            t['score'] = score
            t['breakdown'] = breakdown
            processed.append(t)
        processed = sorted(processed, key=lambda x: x.get('score',0), reverse=True)
        return JsonResponse(processed, safe=False)
    except Exception as e:
        return HttpResponseBadRequest('Invalid JSON or error: '+str(e))

@csrf_exempt
def suggest(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Use POST.')
    try:
        payload = json.loads(request.body)
        strategy = request.GET.get('strategy','balanced')
        scored = []
        for t in payload:
            try:
                score, breakdown = calculate_task_score(t, strategy=strategy)
            except Exception as e:
                score, breakdown = 0, {'error': str(e)}
            scored.append((score, t, breakdown))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = []
        for score, t, breakdown in scored[:3]:
            top.append({'task': t, 'score': score, 'breakdown': breakdown})
        explanation = f"Top {len(top)} tasks chosen by strategy '{strategy}'."
        return JsonResponse({'top': top, 'explanation': explanation}, safe=False)
    except Exception as e:
        return HttpResponseBadRequest('Invalid JSON or error: '+str(e))