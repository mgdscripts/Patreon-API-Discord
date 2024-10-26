# Patreon Member Collector Bot

This bot interacts with the Patreon API to retrieve detailed information about members of a specific Patreon campaign, including their full names, emails, patron status, last charge dates, Discord IDs (if linked), and the tier they're currently entitled to. The collected data is saved to a text file for further analysis or integrations.

## Features

- **Pagination Support**: Collects member data across multiple pages with up to 1000 entries per page.
- **Tier and Discord Data**: Includes members' currently entitled tiers and linked Discord IDs.
- **File Management**: Clears and saves data to `patreonmembers.txt`, ensuring data is overwritten with each run.

## Setup Instructions

### Prerequisites

- Python 3.8+
- `requests` library for API requests
- A valid [Patreon API token](https://docs.patreon.com/#introduction) with permissions to access campaign data

### Installation

1. Clone the repository or download the source code.
2. Install the `requests` library:
   ```bash
   pip install requests
   ```

### Configuration

1. **Access Token**: Replace `access_token` with your Patreon API token.
2. **Campaign ID**: Replace `campaign_id` with your Patreon campaign ID.
3. **Campaign Name**: Set the `campaign_name` variable (used in the User-Agent header).

### Code Explanation

- **API Endpoint**: This bot uses the `/campaigns/{campaign_id}/members` endpoint to get member data, including their user information and currently entitled tiers.
- **Fields to Include**:
  - **Member Data**: Full name, email, patron status, last charge date, last charge status, pledge relationship start, and currently entitled amount.
  - **User Data**: First and last names, email, and social connections (for Discord ID collection).
  - **Tier Data**: Title and amount (for the currently entitled tier).
- **Pagination**: The bot fetches data in batches of up to 1000 members per request and automatically follows pagination links to retrieve additional pages of members.
- **File Handling**:
  - `clear_file`: Clears `patreonmembers.txt` at the beginning of each run.
  - `save_to_file`: Appends each member’s information to the text file.

### Usage

1. Run the bot:
   ```bash
   python main.py
   ```
2. The bot will request data from the Patreon API, process it, and save it to `patreonmembers.txt`.

### Example Workflow

1. **Data Fetching**: The bot sends a GET request to the Patreon API for the specified campaign’s members.
2. **Discord ID Collection**: For users with linked Discord accounts, it fetches and saves the Discord ID.
3. **Tier Information**: For each member, it retrieves and formats their entitled tier(s), including tier name and pledge amount.
4. **Data Storage**: Each member's information is saved in a formatted string in `patreonmembers.txt`.

### Example Data Entry

Each entry in `patreonmembers.txt` will look like this:
```plaintext
Name: John Doe, Email: johndoe@example.com, Patron Status: active, Last Charge Date: 2023-05-10, Discord ID: 1234567890, Tier: VIP Supporter ($10.00)
```

### Additional Notes

- **Permissions**: Ensure your API token has permission to read campaign and member data.
- **Patreon API**: This bot uses the v2 API; verify that the endpoint and fields match your API version.
- **Error Handling**: If the API request fails, the bot logs the status code and response text for debugging.

---

This bot was designed to streamline member data collection from Patreon campaigns.
```
