from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from .models import Campaign, Account


def campaigns(request):
    # Get campaigns from database
    campaigns = Campaign.objects.filter(deleted=False).order_by("-created_date")
    return render(request, "campaigns/campaigns.html", {"campaigns": campaigns})


def create_campaign(request):
    if request.method == "POST":
        name = request.POST.get("name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if not name:
            messages.error(request, "Campaign name is required.")
            return render(request, "campaigns/create_campaign.html")

        try:
            # Get or create a default account for now (until user auth is implemented)
            account, _ = Account.objects.get_or_create(
                username="default_user", defaults={"username": "default_user"}
            )

            # Convert date strings to date objects (if provided)
            start_date_obj = (
                datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
            )
            end_date_obj = (
                datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
            )

            # Create the campaign
            Campaign.objects.create(
                name=name,
                account_uuid=account,
                start_date=start_date_obj,
                end_date=end_date_obj,
            )

            messages.success(request, f"Campaign '{name}' created successfully!")
            return redirect("campaigns")

        except Exception as e:
            messages.error(request, f"Error creating campaign: {str(e)}")
            return render(request, "campaigns/create_campaign.html")

    return render(request, "campaigns/create_campaign.html")


def delete_campaign(request, uuid):
    campaign = get_object_or_404(Campaign, uuid=uuid, deleted=False)

    try:
        # Soft delete by setting deleted=True
        campaign.deleted = True
        campaign.save()

        messages.success(
            request, f"Campaign '{campaign.name}' has been deleted successfully!"
        )
    except Exception as e:
        messages.error(request, f"Error deleting campaign: {str(e)}")

    return redirect("campaigns")
