from django.shortcuts import render
import markdown
from django.utils.safestring import mark_safe
from .utils import ask_gemini
from .forms import UserInput
import re

def linkify(text):
    url_pattern = r'(http[s]?://[^\s]+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)

def chatbot(request):
    html_response = ''
    form = UserInput(request.GET)

    # Clear chat history on full page refresh (i.e., no 'user_input' param)
    if 'user_input' not in request.GET:
        request.session['chat_history'] = []

    if request.method == "GET" and 'user_input' in request.GET:
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            raw_response = ask_gemini(user_input)

            # Convert URLs to hyperlinks
            linked_response = linkify(raw_response)

            # Format with markdown (e.g., for line breaks)
            formatted_response = mark_safe(markdown.markdown(linked_response))

            # Append to session chat history
            chat = request.session.get('chat_history', [])
            chat.append({"sender": "You", "message": user_input})
            chat.append({"sender": "Kababayan", "message": formatted_response})
            request.session['chat_history'] = chat  # Save changes

            html_response = formatted_response

    context = {
        'form': form,
        'html_response': html_response,
        'chat_history': request.session.get('chat_history', []),
    }

    return render(request, 'home.html', context)
