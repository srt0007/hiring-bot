#!/bin/bash
# Quick deployment script for multi-domain SSO support

set -e

PEM_FILE="$HOME/Downloads/hiring-pem.pem"
SERVER="ubuntu@13.204.233.140"
REMOTE_DIR="~/hiring-automation-phase1"

echo "========================================="
echo "Multi-Domain SSO Deployment"
echo "========================================="
echo ""

# Test connection
echo "[1/4] Testing SSH connection..."
if ssh -i "$PEM_FILE" -o ConnectTimeout=10 "$SERVER" "echo 'Connected'" > /dev/null 2>&1; then
    echo "✓ SSH connection successful"
else
    echo "✗ SSH connection failed"
    echo "Please check:"
    echo "  - Server is running"
    echo "  - PEM file is at $PEM_FILE"
    echo "  - Firewall allows SSH"
    exit 1
fi

# Upload files
echo "[2/4] Uploading files..."
scp -i "$PEM_FILE" .env "$SERVER:$REMOTE_DIR/"
echo "  ✓ .env"
scp -i "$PEM_FILE" src/auth_manager.py "$SERVER:$REMOTE_DIR/src/"
echo "  ✓ auth_manager.py"
scp -i "$PEM_FILE" src/auth_pages.py "$SERVER:$REMOTE_DIR/src/"
echo "  ✓ auth_pages.py"

# Restart application
echo "[3/4] Restarting application..."
ssh -i "$PEM_FILE" "$SERVER" << 'RESTART_EOF'
    cd ~/hiring-automation-phase1
    pkill -f "streamlit run app.py" || true
    sleep 3
    source venv/bin/activate
    nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
    sleep 3
    ps aux | grep streamlit | grep -v grep
RESTART_EOF

echo "[4/4] Verifying deployment..."
sleep 2
if ssh -i "$PEM_FILE" "$SERVER" "ps aux | grep streamlit | grep -v grep" > /dev/null 2>&1; then
    echo "✓ Application is running"
else
    echo "⚠ Application may not be running. Check logs."
fi

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Application URL: https://screening-hr.printo.in"
echo ""
echo "Test the following:"
echo "  1. Printo SSO login (@printo.in)"
echo "  2. Canvera SSO login (@canvera.com)"
echo ""
echo "View logs:"
echo "  ssh -i $PEM_FILE $SERVER 'tail -f ~/hiring-automation-phase1/streamlit.log'"
echo ""
