from django.shortcuts import render
from datetime import datetime


def campaigns(request):
    # TODO Remove this when data is available
    mock_campaigns = [
        {
            'index': 1,
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'name': 'Summer Adventure Campaign',
            'account_uuid': '456e7890-e89b-12d3-a456-426614174001',
            'start_date': datetime(2024, 6, 1, 16, 20),
            'end_date': datetime(2024, 8, 31, 16, 20),
            'last_updated': datetime(2024, 8, 31, 16, 20),
            'created_date': datetime(2024, 5, 15, 9, 0),
            'deleted': False
        },
        {
            'index': 2,
            'uuid': '987f6543-e89b-12d3-a456-426614174002',
            'name': 'Winter Mystery Campaign',
            'account_uuid': '456e7890-e89b-12d3-a456-426614174001',
            'start_date': datetime(2024, 12, 1, 16, 20),
            'end_date': datetime(2025, 2, 28, 16, 20),
            'last_updated': datetime(2025, 2, 28, 16, 20),
            'created_date': datetime(2024, 10, 1, 11, 15),
            'deleted': False
        },
        {
            'index': 3,
            'uuid': '456a7890-e89b-12d3-a456-426614174003',
            'name': 'Dragon Quest Campaign',
            'account_uuid': '789b0123-e89b-12d3-a456-426614174004',
            'start_date': datetime(2024, 3, 15, 16, 20),
            'end_date': None,
            'last_updated': datetime(2024, 7, 3, 16, 20),
            'created_date': datetime(2024, 2, 28, 13, 30),
            'deleted': False
        }
    ]
    
    return render(request, 'campaigns/campaigns.html', {'campaigns': mock_campaigns})