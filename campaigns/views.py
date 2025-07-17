from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from .models import Campaign, Account
import logging

logger = logging.getLogger(__name__)


def campaigns(request):
    # Get campaigns from database
    campaigns = Campaign.objects.filter(deleted=False).order_by("-created_date")
def campaigns(request):
    # Get campaigns from database
    campaigns = Campaign.objects.filter(deleted=False).order_by("-created_date")
    logger.info(f"Retrieved {campaigns.count()} campaigns for display")
    return render(request, "campaigns/campaigns.html", {"campaigns": campaigns})
    return render(request, "campaigns/campaigns.html", {"campaigns": campaigns})


def create_campaign(request):
    if request.method == "POST":
        name = request.POST.get("name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        logger.info(
            f"Campaign creation attempt - name: '{name}', start_date: '{start_date}', end_date: '{end_date}'"
        )

        if not name:
            logger.warning("Campaign creation failed: name is required")
            messages.error(request, "Campaign name is required.")
            return render(request, "campaigns/create_campaign.html")

        try:
            # Get or create a default account for now (until user auth is implemented)
            account, created = Account.objects.get_or_create(
                username="default_user", defaults={"username": "default_user"}
            )
            logger.debug(
                f"Account {'created' if created else 'retrieved'}: {account.username} (UUID: {account.uuid})"
            )

            # Convert date strings to date objects (if provided)
            start_date_obj = (
                datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
            )
            end_date_obj = (
                datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
            )

            logger.debug(
                f"Date conversion - start_date_obj: {start_date_obj}, end_date_obj: {end_date_obj}"
            )

            # Create the campaign
            campaign = Campaign.objects.create(
                name=name,
                account_uuid=account,
                start_date=start_date_obj,
                end_date=end_date_obj,
            )

            logger.info(
                f"Campaign '{name}' created successfully with UUID: {campaign.uuid} by {account.username} (UUID: {account.uuid})"
            )
            messages.success(request, f"Campaign '{name}' created successfully!")
            return redirect("campaigns")

        except Exception as e:
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
            return render(request, "campaigns/create_campaign.html")

    logger.debug("Rendering create campaign form (GET request)")
    return render(request, "campaigns/create_campaign.html")


def delete_campaign(request, uuid):
    logger.info(f"Campaign deletion attempt for UUID: {uuid}")
    campaign = get_object_or_404(Campaign, uuid=uuid, deleted=False)

    logger.debug(f"Found campaign to delete: '{campaign.name}' (UUID: {campaign.uuid})")

    try:
        # Soft delete by setting deleted=True
        campaign.deleted = True
        campaign.save()

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
     except Exception as e:
         logger.error(
             f"Error deleting campaign '{campaign.name}' (UUID: {campaign.uuid}): {str(e)}",
             exc_info=True,
         )
        messages.error(request, f"Error deleting campaign: {str(e)}")

    return redirect("campaigns")
