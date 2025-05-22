# PhishGrid - Offline Phishing Simulation Tool

A powerful, offline-only phishing simulation tool designed specifically for Nigerian SMEs. PhishGrid helps organizations test their employees' security awareness without requiring internet connectivity.

## 🌟 Features

- 🚀 **100% Offline**: Works without internet connection
- 📧 **Realistic Phishing Kits**: Pre-built templates for common Nigerian phishing scenarios
- 📊 **Detailed Analytics**: Track click rates, form submissions, and response times
- 🔒 **Secure**: All data stored locally in JSON files
- 🎯 **Customizable**: Create and modify phishing campaigns
- 💻 **Cross-Platform**: Works on Windows, macOS, and Linux

## 📁 Project Structure

```
phishgrid/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application code
│   └── logs/         # Campaign logs
├── frontend/         # Static HTML files
│   ├── index.html    # Campaign builder
│   ├── viewer.html   # Results viewer
│   └── remediation.html  # Training materials
├── kits/             # Phishing kits
│   └── gtb-alert/    # GTB alert template
├── run_local.sh      # Unix/Linux/macOS startup script
├── run_local.bat     # Windows startup script
└── requirements.txt  # Python dependencies
```

## 🛠️ Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/T3chfalcon/phishgrid-v1.git
   cd phishgrid-v1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Windows
1. Double-click `run_local.bat` or run it from Command Prompt:
   ```cmd
   run_local.bat
   ```

### Unix/Linux/macOS
1. Make the script executable:
   ```bash
   chmod +x run_local.sh
   ```
2. Run the script:
   ```bash
   ./run_local.sh
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## 🔧 Creating a Campaign

1. Click "Create New Campaign"
2. Select a phishing kit template
3. Configure campaign settings:
   - Target email addresses
   - Campaign duration
   - Success criteria
4. Click "Launch Campaign"

## 📊 Viewing Results

1. Go to the Results page
2. Select your campaign
3. View detailed analytics:
   - Click rates
   - Form submissions
   - Response times
   - User behavior

## ⚠️ Security Notice

This tool is designed for legitimate security awareness training. Always:
- Obtain proper authorization before running simulations
- Use only on your own network
- Follow local laws and regulations
- Respect employee privacy

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 