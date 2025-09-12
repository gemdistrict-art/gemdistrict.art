# 1. Go to home workspace
cd ~

# 2. Clone the full GemDistrict project
git clone https://github.com/kimi-gemdistrict/gemdistrict-art.git

# 3. Copy everything into your existing repo
cp -r gemdistrict-art/* ~/workspaces/Old-and-new/

# 4. Move into your repo
cd ~/workspaces/Old-and-new

# 5. Stage, commit, push
git add .
git commit -m "feat: add AI gem ID, Web3 wallet, 3D/AR viewer"
git push origin main
git commit -m "feat: AI gem ID, Web3 wallet, 3D/AR viewer"
git push origin main
