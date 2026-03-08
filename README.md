# SmartStore - Streamlit E-Commerce Platform

SmartStore is a fully functional, highly interactive e-commerce storefront built entirely in Python using Streamlit. It features a public-facing product catalog, shopping cart, secure authentication, role-based dashboards, and ML-powered recommendations and demand forecasting.

---

## Features

- **Adaptive UI/UX:** Modern responsive design with sticky header, product image grids, and Light/Dark mode.
- **Public Storefront:** Guests can browse the catalog, view product images, and check stock levels.
- **Authentication System:** Single-page Login/Sign-up toggle; users must log in to add items to cart.
- **Role-Based Access Control (RBAC):**
  - Customers — Browse products, view details, manage cart.
  - Managers — Manager Dashboard: profit analytics, low-stock alerts, dynamic product addition.
  - Admins — Admin Console: user demographics, role promotion/demotion.
- **ML Features:**
  - Cosine-similarity content recommender (TF-IDF on category + description).
  - Random Forest demand forecasting trained on synthetic 30-day sales history.
- **In-Memory Database:** pandas + st.session_state — no external DB required.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend & Backend | Streamlit (Python) |
| Data | Pandas, NumPy |
| Machine Learning | scikit-learn (TF-IDF, RandomForest) |
| Containerisation | Docker |
| Cloud | Azure (Free Tier VM) |

---

## Project Structure

```
E-Comm-Site/
  app.py
  auth.py
  Dockerfile
  .dockerignore
  requirements.txt
  .streamlit/
    config.toml
  database/
    db.py
  ml/
    recommender.py
    demand_prediction.py
  pages/
    customer_store.py
    product_page.py
    login.py
    cart_utils.py
    manager_dashboard.py
    admin_panel.py
```

---

## Demo Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@test.com | admin123 |
| Manager | manager@test.com | manager123 |
| Customer | user@test.com | user123 |

---

## Run Locally (without Docker)

```bash
git clone https://github.com/YOUR_USERNAME/E-Comm-Site.git
cd E-Comm-Site

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
streamlit run app.py
# -> http://localhost:8501
```

---

## Run Locally with Docker

```bash
# Build the image
docker build -t smartstore .

# Run the container
docker run -d -p 8501:8501 --name smartstore smartstore

# Open in browser
# -> http://localhost:8501

# Stop
docker stop smartstore
```


---

## Push to Docker Hub

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A free Docker Hub account at https://hub.docker.com  (username: **debdev25**)

### One-time login

```bash
docker login
# Enter your Docker Hub username (debdev25) and password when prompted
```

### Build and push

```bash
# 1. Build the image tagged with your Docker Hub username
docker build -t debdev25/smartstore:latest .

# 2. (Optional) also tag a versioned release
docker tag debdev25/smartstore:latest debdev25/smartstore:v1.0

# 3. Push to Docker Hub
docker push debdev25/smartstore:latest
docker push debdev25/smartstore:v1.0   # optional versioned tag

# Image will be live at:
# https://hub.docker.com/r/debdev25/smartstore
```

### Pull and run from Docker Hub (on any machine / your Azure VM)

```bash
docker pull debdev25/smartstore:latest
docker run -d --name smartstore --restart always -p 80:8501 debdev25/smartstore:latest
```

### Update workflow (push a new version)

```bash
# After making code changes:
docker build -t debdev25/smartstore:latest .
docker push debdev25/smartstore:latest

# On the Azure VM — pull and redeploy:
docker pull debdev25/smartstore:latest
docker stop smartstore && docker rm smartstore
docker run -d --name smartstore --restart always -p 80:8501 debdev25/smartstore:latest
```

---

## Deploy to Azure (Manual — Free Tier)

This deploys the Docker container on a single Azure B1s VM (free for 12 months).

### Cost

| Resource | Cost |
|---|---|
| Standard_B1s VM (1 vCPU, 1 GB RAM) | FREE for 12 months (750 hr/month) |
| OS Disk 30 GB | FREE |
| Static Public IP | ~$3/month |
| Outbound data first 100 GB | FREE |

### Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed
- [Docker](https://docs.docker.com/get-docker/) installed locally
- Free Azure account at https://azure.microsoft.com/free/

### Step 1 — Log in to Azure

```bash
az login
```

### Step 2 — Create a Resource Group

```bash
az group create --name smartstore-rg --location eastus
```

### Step 3 — Create the VM

```bash
az vm create \
  --resource-group smartstore-rg \
  --name smartstore-vm \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard
```

This prints a `publicIpAddress` — save it, that is your server IP.

### Step 4 — Open Port 80

```bash
az vm open-port \
  --resource-group smartstore-rg \
  --name smartstore-vm \
  --port 80
```

### Step 5 — SSH into the VM and Install Docker

```bash
ssh azureuser@<YOUR_VM_IP>

# On the VM:
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker azureuser
newgrp docker
```

### Step 6 — Clone the Repo and Build the Image on the VM

```bash
# Still on the VM:
git clone https://github.com/YOUR_USERNAME/E-Comm-Site.git
cd E-Comm-Site

docker build -t smartstore .
```

### Step 7 — Run the Container (mapping port 80 -> 8501)

```bash
docker run -d \
  --name smartstore \
  --restart always \
  -p 80:8501 \
  smartstore
```

Open your browser: `http://<YOUR_VM_IP>` — SmartStore is live.

### Step 8 — Updating the App

When you push new code, SSH back in and run:

```bash
cd E-Comm-Site
git pull
docker build -t smartstore .
docker stop smartstore && docker rm smartstore
docker run -d --name smartstore --restart always -p 80:8501 smartstore
```

### Useful Commands on the VM

```bash
# Check running containers
docker ps

# View live app logs
docker logs -f smartstore

# Stop the app
docker stop smartstore

# Restart the app
docker restart smartstore

# Check how much disk/memory is used
docker stats smartstore
```

---

## Security Checklist

- [ ] Restrict SSH: `az vm open-port --port 22` and set a Network Security Group rule to your IP only
- [ ] Replace plain-text passwords in `database/db.py` with bcrypt-hashed values
- [ ] Set up HTTPS using Nginx + Let's Encrypt (Certbot) in front of the container
- [ ] Keep Docker and system packages updated: `sudo apt-get upgrade -y`

---

## Licence

MIT

