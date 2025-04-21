from django.shortcuts import render
import markdown
from django.utils.safestring import mark_safe
from .utils import ask_gemini
from .forms import UserInput


def home(request):
    html_response = ''
    form = UserInput(request.GET)

    if request.method == "GET":

        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            raw_response = ask_gemini(user_input)
            html_response = mark_safe(markdown.markdown(raw_response))
    
    else:
        form = UserInput()
    
    context = {
        'form': form,
        'html_response': html_response,
    }

    return render(request, 'home.html', context)