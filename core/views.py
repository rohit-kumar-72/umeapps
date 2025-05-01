import os
import google.genai as genai
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import AnalysisLog
import json
# Create your views here.

TONE_LIST = [
    "Happy", "Sad", "Angry", "Frustrated", "Excited", "Calm",
    "Bored", "Anxious", "Confused", "Curious", "Motivated", "Tired"
]
TONE_TO_INTENT_MAP = {
    "Bored": "Entertainment",
    "Happy": "Celebrate",
    "Sad": "Seek Support",
    "Angry": "Complaint",
    "Frustrated": "Ask Question",
    "Excited": "Order Food",
    "Calm": "Casual Inquiry",
    "Anxious": "Seek Support",
    "Confused": "Ask Question",
    "Curious": "Learn Something",
    "Motivated": "Plan Goals",
    "Tired": "Health Advice",
    "Unknown":"Ask Question"
}

ACTION_MAP = {
    "Entertainment": [
        {"action_code": "WATCH_VIDEO", "display_text": "Watch a trending video"},
        {"action_code": "PLAY_GAME", "display_text": "Play an online game"},
        {"action_code": "LISTEN_MUSIC", "display_text": "Listen to music"}
    ],
    "Celebrate": [
        {"action_code": "ORDER_CAKE", "display_text": "Order a celebration cake"},
        {"action_code": "BOOK_RESTAURANT", "display_text": "Book a restaurant"},
        {"action_code": "SEND_GIFT", "display_text": "Send a gift to someone"}
    ],
    "Seek Support": [
        {"action_code": "CONTACT_SUPPORT", "display_text": "Contact support"},
        {"action_code": "CHAT_THERAPIST", "display_text": "Chat with a therapist"},
        {"action_code": "JOIN_COMMUNITY", "display_text": "Join a support community"}
    ],
    "Complaint": [
        {"action_code": "FILE_COMPLAINT", "display_text": "File a complaint"},
        {"action_code": "ESCALATE_ISSUE", "display_text": "Escalate to management"},
        {"action_code": "LEAVE_FEEDBACK", "display_text": "Leave negative feedback"}
    ],
    "Ask Question": [
        {"action_code": "SEARCH_FAQ", "display_text": "Search FAQ"},
        {"action_code": "ASK_AGENT", "display_text": "Talk to a support agent"},
        {"action_code": "POST_FORUM", "display_text": "Post a question on community forum"}
    ],
    "Order Food": [
        {"action_code": "ORDER_PIZZA", "display_text": "Order a pizza"},
        {"action_code": "FIND_NEARBY_FOOD", "display_text": "Find nearby food options"},
        {"action_code": "VIEW_MENU", "display_text": "Browse restaurant menus"}
    ],
    "Casual Inquiry": [
        {"action_code": "DAILY_FACT", "display_text": "Get a daily fact"},
        {"action_code": "NEWS_HEADLINES", "display_text": "View news headlines"},
        {"action_code": "CHECK_WEATHER", "display_text": "Check today's weather"}
    ],
    "Learn Something": [
        {"action_code": "WATCH_TUTORIAL", "display_text": "Watch a tutorial"},
        {"action_code": "READ_ARTICLE", "display_text": "Read an article"},
        {"action_code": "ENROLL_COURSE", "display_text": "Enroll in a free course"}
    ],
    "Plan Goals": [
        {"action_code": "SET_REMINDER", "display_text": "Set a reminder"},
        {"action_code": "CREATE_TODO", "display_text": "Create a to-do list"},
        {"action_code": "SCHEDULE_EVENT", "display_text": "Schedule an event"}
    ],
    "Health Advice": [
        {"action_code": "SLEEP_TIPS", "display_text": "Tips for better sleep"},
        {"action_code": "EXERCISE_ROUTINE", "display_text": "Start a light exercise routine"},
        {"action_code": "MENTAL_HEALTH_TIPS", "display_text": "Mental health guidance"}
    ]
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
        "Analyze the following user message. Choose the tone from this list:\n"
        f"{TONE_LIST}\n"
        "Then choose an appropriate intent category based on the tone using the following mapping:\n"
        f"{json.dumps(TONE_TO_INTENT_MAP)}\n"
        "Return a JSON object with fields 'tone', 'intent', and 'actions' (brief description).\n"
        "Only return the JSON.\n"
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