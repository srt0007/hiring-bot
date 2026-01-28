#!/bin/bash

# Deployment script for Hiring Automation SSO fix
# Usage: ./deploy.sh [server_user@server_ip]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Hiring Automation - Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"

# Configuration
PEM_FILE="$HOME/Downloads/hiring-pem.pem"
SERVER_USER=${1:-"ubuntu"}  # Default to ubuntu if not specified
SERVER_HOST=${2:-"screening-hr.printo.in"}
REMOTE_DIR="/home/$SERVER_USER/hiring-automation-phase1"
APP_NAME="hiring-app"

# Check if PEM file exists
if [ ! -f "$PEM_FILE" ]; then
    echo -e "${RED}Error: PEM file not found at $PEM_FILE${NC}"
    exit 1
fi

# Set correct permissions for PEM file
chmod 400 "$PEM_FILE"

echo -e "${YELLOW}Deploying to: ${SERVER_USER}@${SERVER_HOST}${NC}"
echo ""

# Step 1: Test SSH connection
echo -e "${YELLOW}[1/6] Testing SSH connection...${NC}"
if ssh -i "$PEM_FILE" -o ConnectTimeout=10 "${SERVER_USER}@${SERVER_HOST}" "echo 'Connection successful'" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ SSH connection successful${NC}"
else
    echo -e "${RED}✗ SSH connection failed${NC}"
    echo "Please check:"
    echo "  - Server is running"
    echo "  - PEM file is correct"
    echo "  - Server address is correct"
    echo "  - Security group allows SSH"
    exit 1
fi

# Step 2: Backup current deployment
echo -e "${YELLOW}[2/6] Creating backup...${NC}"
ssh -i "$PEM_FILE" "${SERVER_USER}@${SERVER_HOST}" << 'BACKUP_EOF'
    if [ -d ~/hiring-automation-phase1 ]; then
        BACKUP_NAME="hiring-automation-backup-$(date +%Y%m%d-%H%M%S)"
        cp -r ~/hiring-automation-phase1 ~/$BACKUP_NAME
        echo "✓ Backup created: $BACKUP_NAME"
    else
        echo "✓ No existing deployment to backup"
    fi
BACKUP_EOF

# Step 3: Upload updated files
echo -e "${YELLOW}[3/6] Uploading updated files...${NC}"

# Upload requirements-web.txt
scp -i "$PEM_FILE" "requirements-web.txt" "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"
echo "  ✓ requirements-web.txt"

# Upload updated .env file
scp -i "$PEM_FILE" ".env" "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"
echo "  ✓ .env"

# Upload updated auth files
scp -i "$PEM_FILE" "src/auth_pages.py" "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/src/"
echo "  ✓ src/auth_pages.py"

# Upload updated app.py if needed
scp -i "$PEM_FILE" "app.py" "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"
echo "  ✓ app.py"

echo -e "${GREEN}✓ Files uploaded successfully${NC}"

# Step 4: Install/Update dependencies
echo -e "${YELLOW}[4/6] Installing updated dependencies...${NC}"
ssh -i "$PEM_FILE" "${SERVER_USER}@${SERVER_HOST}" << 'INSTALL_EOF'
    cd ~/hiring-automation-phase1

    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    # Upgrade pip
    pip install --upgrade pip

    # Install updated requirements
    pip install -r requirements-web.txt --upgrade

    echo "✓ Dependencies updated (Streamlit upgraded to 1.40.2)"
INSTALL_EOF

# Step 5: Stop the running application
echo -e "${YELLOW}[5/6] Stopping current application...${NC}"
ssh -i "$PEM_FILE" "${SERVER_USER}@${SERVER_HOST}" << 'STOP_EOF'
    # Stop systemd service if it exists
    if systemctl is-active --quiet hiring-app; then
        sudo systemctl stop hiring-app
        echo "✓ Systemd service stopped"
    fi

    # Kill any running Streamlit processes
    pkill -f "streamlit run app.py" || true
    sleep 2

    echo "✓ Application stopped"
STOP_EOF

# Step 6: Start the application
echo -e "${YELLOW}[6/6] Starting application...${NC}"
ssh -i "$PEM_FILE" "${SERVER_USER}@${SERVER_HOST}" << 'START_EOF'
    cd ~/hiring-automation-phase1

    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    # Start systemd service if it exists
    if systemctl list-unit-files | grep -q hiring-app.service; then
        sudo systemctl start hiring-app
        echo "✓ Systemd service started"
    else
        # Start with nohup as fallback
        nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
        echo "✓ Application started with nohup"
    fi

    sleep 3

    # Check if app is running
    if pgrep -f "streamlit run app.py" > /dev/null; then
        echo "✓ Application is running"
    else
        echo "⚠ Warning: Application may not be running. Check logs."
    fi
START_EOF

# Final status
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Application URL: https://screening-hr.printo.in"
echo ""
echo "Next steps:"
echo "  1. Test SSO login at https://screening-hr.printo.in"
echo "  2. Check application logs if needed:"
echo "     ssh -i $PEM_FILE ${SERVER_USER}@${SERVER_HOST} 'tail -f ~/hiring-automation-phase1/streamlit.log'"
echo ""
echo "Troubleshooting:"
echo "  - View logs: ssh -i $PEM_FILE ${SERVER_USER}@${SERVER_HOST} 'cd ~/hiring-automation-phase1 && tail -100 streamlit.log'"
echo "  - Restart app: ssh -i $PEM_FILE ${SERVER_USER}@${SERVER_HOST} 'sudo systemctl restart hiring-app'"
echo "  - Check status: ssh -i $PEM_FILE ${SERVER_USER}@${SERVER_HOST} 'systemctl status hiring-app'"
echo ""
