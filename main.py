import requests
import json

# Patreon API credentials
access_token = ''
campaign_id = ''  # Replace with your actual campaign ID
campaign_name = ''
# Patreon API v2 base URL
base_url = 'https://www.patreon.com/api/oauth2/v2/'

# Endpoint for campaign members and including user data and currently entitled tiers
endpoint = f'campaigns/{campaign_id}/members?include=user,currently_entitled_tiers'

# Fields to include in the response
fields = (
    'fields[member]='
    'full_name,email,patron_status,lifetime_support_cents,last_charge_date,last_charge_status,'
    'pledge_relationship_start,currently_entitled_amount_cents'
    '&fields[user]=first_name,last_name,email,social_connections'
    '&fields[tier]=title,amount_cents'  # Include tier fields (title and amount)
)

# Increase page size to get 1000 members per request
page_size = 1000  # Set the page size to 1000
url = f'{base_url}{endpoint}&{fields}&page[size]={page_size}'

# Headers for the request
headers = {
    'Authorization': f'Bearer {access_token}',
    'User-Agent': '{campaign_name}',
    'Content-Type': 'application/json'
}

# Function to clear file contents
def clear_file(filename):
    with open(filename, 'w', encoding='utf-8') as file:  # Using utf-8 encoding
        file.write('')  # Overwrite with empty content

# Function to save information to file
def save_to_file(filename, content):
    with open(filename, 'a', encoding='utf-8') as file:  # Using utf-8 encoding
        file.write(content + '\n')

# Function to get Patreon members with pagination
def get_patreon_members():
    next_url = url  # Start with the initial URL
    members_collected = 0
    filename = 'patreonmembers.txt'

    # Clear the file before saving new data
    clear_file(filename)

    while next_url:
        response = requests.get(next_url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            members_info = response.json()
            
            # Create a dictionary to map user ids to their social connections
            user_social_connections = {}
            
            # Populate the dictionary from 'included' data
            if 'included' in members_info:
                for included_user in members_info['included']:
                    user_id = included_user['id']  # This is the user ID from 'included'
                    social_connections = included_user['attributes'].get('social_connections', None)
                    
                    # Ensure 'social_connections' exists and 'discord' is not None
                    if social_connections and social_connections.get('discord'):
                        discord_id = social_connections['discord'].get('user_id', 'N/A')
                        user_social_connections[user_id] = discord_id
            
            # Process the members in this batch
            if 'data' in members_info:
                for member in members_info['data']:
                    full_name = member['attributes']['full_name']
                    email = member['attributes'].get('email', 'N/A')  # Handle missing email
                    patron_status = member['attributes']['patron_status']
                    last_charge_date = member['attributes'].get('last_charge_date', 'N/A')  # Handle missing last_charge_date
                    
                    # Get the correct user ID from the member relationship
                    user_id = member['relationships']['user']['data']['id']
                    
                    # Look up the corresponding Discord ID for this user, if available
                    discord_id = user_social_connections.get(user_id, 'N/A')

                    # Get tier information (currently entitled tiers)
                    tier_titles = []
                    if 'currently_entitled_tiers' in member['relationships']:
                        tiers = member['relationships']['currently_entitled_tiers']['data']
                        for tier in tiers:
                            tier_id = tier['id']
                            # Find tier in 'included' section
                            for included_tier in members_info['included']:
                                if included_tier['id'] == tier_id and included_tier['type'] == 'tier':
                                    tier_title = included_tier['attributes']['title']
                                    tier_amount = included_tier['attributes']['amount_cents'] / 100  # Convert to dollars
                                    tier_titles.append(f"{tier_title} (${tier_amount})")
                    
                    tier_info = ', '.join(tier_titles) if tier_titles else 'No tier'

                    # Prepare the information string
                    info = (f"Name: {full_name}, Email: {email}, Patron Status: {patron_status}, "
                            f"Last Charge Date: {last_charge_date}, Discord ID: {discord_id}, Tier: {tier_info}")
                    
                    # Save the information to the file
                    save_to_file(filename, info)

                    # Output the information (optional)
                    print(info)
                    members_collected += 1
            
            # Check for next page link
            next_url = members_info.get('links', {}).get('next', None)
            
        else:
            print(f"Failed to fetch members info. Status Code: {response.status_code}")
            print("Response:", response.text)
            break
    
    print(f"Total members collected: {members_collected}")

# Run the function
get_patreon_members()
