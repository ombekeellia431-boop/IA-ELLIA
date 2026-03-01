
#!/bin/bash
# Ce script modifie la politique de sécurité d'ImageMagick pour autoriser MoviePy
sudo sed -i 's/domain="coder" rights="none" pattern="PDF"/domain="coder" rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml
