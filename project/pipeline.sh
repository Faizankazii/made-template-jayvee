#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "${YELLOW}Fetching Airbnb datasets...${NC}" # Static setup. If file exists, not more need for data. No crawling. Just one-time download only.
if [ -f "airbnb_data.zip" ]; then
    echo "${YELLOW}airbnb_data.zip already exists. Skipping download.${NC}"
else
    curl -L -o airbnb_data.zip \
        https://www.kaggle.com/api/v1/datasets/download/kritikseth/us-airbnb-open-data
fi

echo "${YELLOW}Fetching US cities datasets...${NC}"
if [ -f "uscities.zip" ]; then
    echo "${YELLOW}uscities.zip already exists. Skipping download.${NC}"
else
    curl -L -o uscities.zip \
        https://simplemaps.com/static/data/us-cities/1.79/basic/simplemaps_uscities_basicv1.79.zip
fi

echo "${YELLOW}Unzipping...${NC}"
unzip -o airbnb_data.zip -d airbnb_data
unzip -o uscities.zip -d uscities
echo "${GREEN}Process Completed successfully.${NC}"

echo "${YELLOW}Starting python script.${NC}"
python fetch_process_data.py
