#FROM gitpod/workspace-full
                
#USER root
#RUN sudo apt-get update
#RUN sudo apt-get install -y  libgbm-dev gconf-service libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxss1 libxtst6 libappindicator1 libnss3 libasound2 libatk1.0-0 libc6 ca-certificates fonts-liberation lsb-release xdg-utils wget 

FROM gitpod/workspace-full

USER gitpod

# Copy the .python-version file into the Docker image to use it during the build
COPY .python-version /home/gitpod/.python-version

# Install the specific Python version from .python-version and upgrade pip
RUN pyenv install $(cat /home/gitpod/.python-version) && \
    pyenv global $(cat /home/gitpod/.python-version) && \
    eval "$(pyenv init -)" && \
    pip install --upgrade pip
