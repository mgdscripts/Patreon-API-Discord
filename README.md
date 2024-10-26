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
