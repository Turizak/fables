import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreateCampaignForm
from .models import Account, Campaign

logger = logging.getLogger(__name__)


def campaigns(request):
    # Get campaigns from database
    campaigns = Campaign.objects.filter(deleted=False).order_by("-created_date")
    logger.info(f"Retrieved {campaigns.count()} campaigns for display")
    return render(request, "campaigns.html", {"campaigns": campaigns})


def create_campaign(request):
    if request.method == "POST":
        form = CreateCampaignForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            logger.info(
                f"Campaign creation attempt - name: '{name}', start_date: '{start_date}', end_date: '{end_date}'"
            )

            try:
                # Get or create a default account for now (until user auth is implemented)
                account, created = Account.objects.get_or_create(
                    username="default_user", defaults={"username": "default_user"}
                )
                logger.debug(
                    f"Account {'created' if created else 'retrieved'}: {account.username} (UUID: {account.uuid})"
                )

                # Create the campaign
                campaign = Campaign.objects.create(
                    name=name,
                    account_uuid=account,
                    start_date=start_date,
                    end_date=end_date,
                )

                logger.info(
                    f"Campaign '{name}' created successfully with UUID: {campaign.uuid} by {account.username} (UUID: {account.uuid})"
                )
                messages.success(request, f"Campaign '{name}' created successfully!")
                return redirect("campaigns")

            except Exception as e:
                try:
                    account_info = f"{account.username} (UUID: {account.uuid})"
                except NameError:
                    account_info = "Unknown user"
                logger.error(
                    f"{account_info} encountered error creating campaign '{name}': {str(e)}",
                    exc_info=True,
                )
                messages.error(request, f"Error creating campaign: {str(e)}")
        else:
            logger.warning(f"Form validation failed: {form.errors}")
    else:
        form = CreateCampaignForm()
        logger.debug("Rendering create campaign form (GET request)")

    return render(request, "create_campaign.html", {"form": form})


def delete_campaign(request, uuid):
    logger.info(f"Campaign deletion attempt for UUID: {uuid}")
    campaign = get_object_or_404(Campaign, uuid=uuid, deleted=False)

    logger.debug(f"Found campaign to delete: '{campaign.name}' (UUID: {campaign.uuid})")

    try:
        # Soft delete by setting deleted=True
        campaign.deleted = True
        campaign.save()

        logger.info(
            f"Campaign '{campaign.name}' (UUID: {campaign.uuid}) successfully soft-deleted"
        )
        messages.success(
            request, f"Campaign '{campaign.name}' has been deleted successfully!"
        )
    except Exception as e:
        messages.error(request, f"Error deleting campaign: {str(e)}")
        logger.error(
            f"Error deleting campaign '{campaign.name}' (UUID: {campaign.uuid}): {str(e)}",
            exc_info=True,
        )

    return redirect("campaigns")
