# PhishGrid - Offline Phishing Simulation Tool

PhishGrid is a self-contained phishing simulation tool designed for Nigerian SMEs. It runs entirely offline and helps organizations test their employees' awareness of phishing attacks through simulated campaigns.

## Features

- 🚀 **Offline-First**: Works without internet or cloud services
- 📧 **Local Templates**: Uses HTML templates for phishing pages
- 📊 **Event Tracking**: Logs opens, clicks, and form submissions
- 📈 **Results Viewer**: Simple frontend to display campaign results
- 🎯 **Multiple Kits**: Includes various phishing templates (GTBank, NEPA, etc.)

## Project Structure

```
phishgrid-local/
├── backend/ (FastAPI)
│   ├── main.py             ← Simple API for tracking
│   └── logs/               ← Tracks events per campaign
├── frontend/
│   ├── index.html          ← Campaign builder (static)
│   ├── viewer.html         ← See results (uses fetch API)
│   └── remediation.html    ← Fake remediation page
├── kits/
│   ├── gtb-alert/
│   │   ├── email.html
│   │   └── index.html      ← Landing page with JS tracker
└── run_local.sh            ← Bash script to launch server
```

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/phishgrid-local.git
cd phishgrid-local
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
chmod +x run_local.sh
./run_local.sh
```

The application will be available at `http://localhost:8000`

## Usage

1. **Create a Campaign**:
   - Open `http://localhost:8000` in your browser
   - Fill in campaign details (name, target emails, phishing kit)
   - Preview the phishing template
   - Create the campaign

2. **View Results**:
   - Click "View Results" on any campaign
   - See statistics for opens, clicks, and submissions
   - View detailed event logs

3. **Test the Campaign**:
   - Open the phishing email template
   - Click the link to simulate a user interaction
   - Fill out the form to simulate a submission
   - View the results in real-time

## Security Notice

This tool is designed for educational and testing purposes only. Always:
- Obtain proper authorization before running phishing simulations
- Follow ethical guidelines and local laws
- Use only on systems you own or have permission to test
- Never collect real credentials or sensitive data

## License

MIT License - See LICENSE file for details 