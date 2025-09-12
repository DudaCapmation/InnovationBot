import json
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .slack_utils import send_message
from .slack_listeners import handler

@csrf_exempt
def slack_events_handler(request):
    return handler.handle(request)

@csrf_exempt
def send_message_api(request):
    # API endpoint for message sending

    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON.")

    channel = payload.get("channel")
    text = payload.get("text")

    if not channel or not text:
        return  HttpResponseBadRequest("Missing channel or text.")

    try:
        response = send_message(channel=channel, text=text)
        return JsonResponse({"ok": True, "slack": response})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)