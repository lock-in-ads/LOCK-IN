from django.shortcuts import render

def quick_assignment(request):
    return render(request, 'quick-assignment.html')

def register_card(request):
    return render(request, 'register-card.html')