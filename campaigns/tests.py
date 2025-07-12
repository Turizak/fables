from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import date
from uuid import uuid4

from .models import Campaign
from accounts.models import Account


class CampaignModelTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(username="test_user")

    def test_campaign_creation(self):
        campaign = Campaign.objects.create(
            name="Test Campaign",
            account_uuid=self.account,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        )

        self.assertEqual(campaign.name, "Test Campaign")
        self.assertEqual(campaign.account_uuid, self.account)
        self.assertEqual(campaign.start_date, date(2024, 1, 1))
        self.assertEqual(campaign.end_date, date(2024, 12, 31))
        self.assertFalse(campaign.deleted)
        self.assertIsNotNone(campaign.uuid)
        self.assertIsNotNone(campaign.created_date)
        self.assertIsNotNone(campaign.last_updated)

    def test_campaign_str_method(self):
        campaign = Campaign.objects.create(
            name="Test Campaign", account_uuid=self.account
        )
        self.assertEqual(str(campaign), "Test Campaign")

    def test_campaign_uuid_uniqueness(self):
        campaign1 = Campaign.objects.create(
            name="Campaign 1", account_uuid=self.account
        )
        campaign2 = Campaign.objects.create(
            name="Campaign 2", account_uuid=self.account
        )
        self.assertNotEqual(campaign1.uuid, campaign2.uuid)

    def test_campaign_optional_dates(self):
        campaign = Campaign.objects.create(
            name="Campaign No Dates", account_uuid=self.account
        )
        self.assertIsNone(campaign.start_date)
        self.assertIsNone(campaign.end_date)

    def test_campaign_soft_delete(self):
        campaign = Campaign.objects.create(name="To Delete", account_uuid=self.account)
        campaign.deleted = True
        campaign.save()
        self.assertTrue(campaign.deleted)


class CampaignViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(username="test_user")

    def test_campaigns_view_get(self):
        Campaign.objects.create(
            name="Active Campaign", account_uuid=self.account, deleted=False
        )
        Campaign.objects.create(
            name="Deleted Campaign", account_uuid=self.account, deleted=True
        )

        response = self.client.get(reverse("campaigns"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active Campaign")
        self.assertNotContains(response, "Deleted Campaign")

    def test_create_campaign_get(self):
        response = self.client.get(reverse("create_campaign"))
        self.assertEqual(response.status_code, 200)

    def test_create_campaign_post_valid(self):
        response = self.client.post(
            reverse("create_campaign"),
            {
                "name": "New Campaign",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Campaign.objects.filter(name="New Campaign").exists())

        campaign = Campaign.objects.get(name="New Campaign")
        self.assertEqual(campaign.start_date, date(2024, 1, 1))
        self.assertEqual(campaign.end_date, date(2024, 12, 31))

    def test_create_campaign_post_no_name(self):
        response = self.client.post(
            reverse("create_campaign"), {"name": "", "start_date": "2024-01-01"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Campaign.objects.filter(name="").exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Campaign name is required" in str(m) for m in messages))

    def test_create_campaign_post_no_dates(self):
        response = self.client.post(
            reverse("create_campaign"), {"name": "Campaign No Dates"}
        )

        self.assertEqual(response.status_code, 302)
        campaign = Campaign.objects.get(name="Campaign No Dates")
        self.assertIsNone(campaign.start_date)
        self.assertIsNone(campaign.end_date)

    def test_create_campaign_creates_default_account(self):
        response = self.client.post(
            reverse("create_campaign"), {"name": "Test Campaign"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Account.objects.filter(username="default_user").exists())

    def test_delete_campaign_valid_uuid(self):
        campaign = Campaign.objects.create(name="To Delete", account_uuid=self.account)

        response = self.client.post(reverse("delete_campaign", args=[campaign.uuid]))

        self.assertEqual(response.status_code, 302)
        campaign.refresh_from_db()
        self.assertTrue(campaign.deleted)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("deleted successfully" in str(m) for m in messages))

    def test_delete_campaign_invalid_uuid(self):
        invalid_uuid = uuid4()
        response = self.client.post(reverse("delete_campaign", args=[invalid_uuid]))
        self.assertEqual(response.status_code, 404)

    def test_delete_already_deleted_campaign(self):
        campaign = Campaign.objects.create(
            name="Already Deleted", account_uuid=self.account, deleted=True
        )

        response = self.client.post(reverse("delete_campaign", args=[campaign.uuid]))
        self.assertEqual(response.status_code, 404)
