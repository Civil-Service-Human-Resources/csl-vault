FROM mcr.microsoft.com/azure-cli
COPY ./.azure /root/.azure
COPY ./app /app
COPY ./.bashrc /root
WORKDIR /app
RUN pip install -r requirements.txt