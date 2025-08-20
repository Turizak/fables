from django.shortcuts import render

from .forms import CreateAccountForm


def create_account(request):
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = CreateAccountForm()

    return render(request, "create_account.html", {"form": form})
