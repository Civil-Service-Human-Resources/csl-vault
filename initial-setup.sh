if [ -d "./.azure" ] 
then
    :
else
    if [ -d "$HOME/.azure" ] 
    then
        cp -r ~/.azure .
    else
        docker run -it --rm -v $PWD/.azure:/root/.azure mcr.microsoft.com/azure-cli az login
    fi
fi

echo "Logged in to Azure. Setting up container..."
docker build -t csl-vault --no-cache .
echo "Done."