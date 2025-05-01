import os
import google.genai as genai
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import AnalysisLog
import json
# Create your views here.


ACTION_MAP = {
    "Order Food": [
        {"action_code": "FIND_NEARBY_PIZZERIA", "display_text": "Find nearby pizza restaurants"},
        {"action_code": "PLACE_ONLINE_ORDER", "display_text": "Place an online pizza order"},
        {"action_code": "FIND_RECIPE", "display_text": "Find pizza recipes"}
    ],
    "Ask Question": [
        {"action_code": "ASK_HELP", "display_text": "Ask for help"},
        {"action_code": "SEARCH_FAQ", "display_text": "Search FAQ"},
        {"action_code": "CONTACT_SUPPORT", "display_text": "Contact support"}
    ],
    # Add more intents as needed
}


@api_view(['POST'])
def analyze(request):
    apikey=os.environ.get("API_KEY")
    user_text = request.data.get("query")
    # print(user_text)
    if not user_text:
        return Response({"success": False, "error": "No Query provided"}, status=400)
    

    client=genai.Client(api_key=apikey)
    chat = client.chats.create(model="gemini-2.0-flash")

    prompt = (
        "Analyze the following user message. "
        "Return a JSON object with fields 'tone' (e.g., Happy, Urgent), 'intent' (e.g., Order Food, Ask Question) and 'actions' (e.g., buy online, this is not a good option). "
        "Respond ONLY with the JSON object. "
        f"Message: {user_text}"
    )

    try:
        response = chat.send_message(prompt)
        # print("*************************************")
        # print(response.text)
        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.strip("```").strip()
            response_text=response_text[4:]
        analysis = json.loads(response_text)
        tone = analysis.get("tone", "Unknown")
        intent = analysis.get("intent", "Unknown")
        ai_suggestion=analysis.get("actions")
    except Exception as e:
        return Response({"error": "Gemini API call or parsing failed", "details": str(e)}, status=500)

    suggested_actions = ACTION_MAP.get(intent, [
        {"action_code": "ASK_HELP", "display_text": "Ask for help"}
    ])
    
    AnalysisLog.objects.create(
        query=user_text,
        tone=tone,
        intent = intent,
        suggestions = suggested_actions
    )

    return Response({
        "query": user_text,
        "AI suggestion":ai_suggestion,
        "analysis": {"tone": tone, "intent": intent},
        "suggested_actions": suggested_actions
    })