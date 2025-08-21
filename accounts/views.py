import logging

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CreateAccountForm
from .models import Account

logger = logging.getLogger(__name__)


def create_account(request):
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            logger.info(f"Account creation attempt - username: '{username}'")

            try:
                account = Account.objects.create_user(
                    username=username, email=email, password=password
                )

                logger.info(
                    f"Account '{username}' created successfully with UUID {account.uuid}"
                )
                messages.success(request, f"Account '{username}' created successfully!")
                return redirect("home")

            except Exception as e:
                logger.error(
                    f"Account creation failed: {str(e)}",
                    exc_info=True,
                )
                messages.error(request, f"Error creating account: {str(e)}")
        else:
            logger.warning(f"Form validation failed: {form.errors}")
    else:
        form = CreateAccountForm()
        logger.debug("Rendering create account form (GET request)")

    return render(request, "create_account.html", {"form": form})
