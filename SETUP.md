# K3s CI/CD Setup Guide

## Prerequisites
- VPS with k3s installed (IP: 37.60.228.133)
- GitHub repository
- SSH access to your VPS

---

## Step 1: Get your kubeconfig from VPS

SSH into your VPS and run:

```bash
# Get the kubeconfig content
sudo cat /etc/rancher/k3s/k3s.yaml
```

**Important:** In the output, replace `127.0.0.1` with your VPS IP `37.60.228.133`:

```yaml
server: https://37.60.228.133:6443   # <-- Change this line
```

---

## Step 2: Base64 encode the kubeconfig

On your VPS, run:

```bash
# Create a modified kubeconfig with your external IP
sudo cat /etc/rancher/k3s/k3s.yaml | sed 's/127.0.0.1/37.60.228.133/g' | base64 -w 0
```

Copy the entire base64 output.

---

## Step 3: Add GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `KUBECONFIG` | The base64 encoded kubeconfig from Step 2 |

---

## Step 4: Open firewall port on VPS

The Kubernetes API needs to be accessible. On your VPS:

```bash
# If using ufw
sudo ufw allow 6443/tcp

# If using firewalld
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --reload

# If using iptables
sudo iptables -A INPUT -p tcp --dport 6443 -j ACCEPT
```

---

## Step 5: Create GitHub repository and push

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit: K3s demo app with CI/CD"

# Add your GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/k3s-demo.git
git branch -M main
git push -u origin main
```

---

## Step 6: Verify deployment

After pushing, GitHub Actions will:
1. Build the Docker image
2. Push to GitHub Container Registry (ghcr.io)
3. Deploy to your K3s cluster

Check your VPS:
```bash
kubectl get pods
kubectl get svc
kubectl get ingress
```

Visit: **http://37.60.228.133**

---

## File Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yaml      # GitHub Actions CI/CD pipeline
├── app/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── k8s/
│   ├── deployment.yaml      # Kubernetes Deployment
│   ├── service.yaml         # Kubernetes Service
│   └── ingress.yaml         # Traefik Ingress
├── Dockerfile               # Container build instructions
└── SETUP.md                 # This file
```

---

## Troubleshooting

### Can't connect to K3s API from GitHub Actions
- Ensure port 6443 is open on your VPS firewall
- Verify the kubeconfig has the correct external IP
- Check that the base64 encoding is correct (no line breaks)

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Image pull errors
- Ensure GitHub Container Registry is accessible
- Check if the image name matches in deployment.yaml

---

## Manual Deployment (Optional)

If you want to deploy manually without CI/CD:

```bash
# On your VPS
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

