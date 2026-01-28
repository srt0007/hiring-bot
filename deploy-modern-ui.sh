#!/bin/bash
# Deploy modern SaaS UI for login/registration pages

PEM_FILE="$HOME/Downloads/hiring-pem.pem"
SERVER="ubuntu@13.204.233.140"
REMOTE_DIR="~/hiring-automation-phase1"

echo "========================================="
echo "Deploying Modern SaaS UI"
echo "========================================="
echo ""

# Upload file
echo "[1/2] Uploading auth_pages.py..."
scp -i "$PEM_FILE" src/auth_pages.py "$SERVER:$REMOTE_DIR/src/"
echo "✓ Upload complete"

# Restart application
echo "[2/2] Restarting application..."
ssh -i "$PEM_FILE" "$SERVER" << 'RESTART_EOF'
    cd ~/hiring-automation-phase1
    pkill -f "streamlit run app.py" || true
    sleep 3
    source venv/bin/activate
    nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
    sleep 3
    echo "✓ Application restarted"
RESTART_EOF

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Visit: https://screening-hr.printo.in"
echo "The login page now has modern SaaS UI!"
