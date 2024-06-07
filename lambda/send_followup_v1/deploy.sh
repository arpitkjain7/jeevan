#!/bin/bash

# Variables
ACTION=$1
FUNCTION_NAME="send_followups_v1"
ROLE_ARN="arn:aws:iam::022262065730:role/send-data-pilot"
LAYER_NAME="cliniq360_layer1"
ZIP_FILE="follow_up_v1.zip"
LAYER_ZIP="cliniq360_layer1.zip"
PACKAGE_DIR="package"
ENV_FILE="environment.json"
ENV="env"
SERVICE_USER=$2
SERVICE_PASSWORD=$3
API_KEY=$4
SECRET=$5
# Remove existing zip files and package directory
rm -f $ZIP_FILE $LAYER_ZIP
rm -rf $PACKAGE_DIR

# Create a package directory for dependencies
mkdir -p $PACKAGE_DIR/python

# Install dependencies into the package directory
pip install -r requirements.txt --target ./$PACKAGE_DIR/python

# Create a zip file for the layer
cd $PACKAGE_DIR
zip -r9 ../$LAYER_ZIP .
cd ..

# Publish a new layer version
LAYER_VERSION_ARN=$(aws lambda publish-layer-version --layer-name $LAYER_NAME --zip-file fileb://$LAYER_ZIP --compatible-runtimes python3.8 --query 'LayerVersionArn' --output text)

# Create a zip file for the Lambda function code
zip -r $ZIP_FILE *.py

if [ "$ACTION" == "update" ]; then
    # Update the Lambda function code
    aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$ZIP_FILE

    # Check if the function code was updated successfully
    if [ $? -ne 0 ]; then
        echo "Error: Failed to update function code."
        exit 1
    fi

    # Update the Lambda function configuration to use the new layer version
    deployment=$(aws lambda update-function-configuration --function-name $FUNCTION_NAME --environment "Variables={callback_base_url=https://engine.doc.cliniq360.com, gupshup_base_url=https://api.gupshup.io, gupshup_followup_notification_template=f09f3217-dd92-4bdd-a0ab-be4653a6ed3f, algorithm=HS256, service_user=$SERVICE_USER, service_password=$SERVICE_PASSWORD, gupshup_api_key=$API_KEY, secret=$SECRET}" --layers $LAYER_VERSION_ARN)

    # Check if the function configuration was updated successfully
    if [ $? -ne 0 ]; then
        echo "Error: Failed to update function configuration."
        exit 1
    fi

elif [ "$ACTION" == "create" ]; then
    # Create the Lambda function
    deployment=$(aws lambda create-function --function-name $FUNCTION_NAME --runtime python3.9 --role $ROLE_ARN --handler main.send_followup_notifications --zip-file fileb://$ZIP_FILE --timeout 30 --memory-size 128 --environment "Variables={callback_base_url=https://engine.doc.cliniq360.com, gupshup_base_url=https://api.gupshup.io, gupshup_followup_notification_template=f09f3217-dd92-4bdd-a0ab-be4653a6ed3f, algorithm=HS256, service_user=$SERVICE_USER, service_password=$SERVICE_PASSWORD, gupshup_api_key=$API_KEY, secret=$SECRET}" --layers $LAYER_VERSION_ARN)

    # Check if the function was created successfully
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create function."
        exit 1
    fi

else
    echo "Error: Invalid ACTION parameter. Use 'create' or 'update'."
    exit 1
fi

echo "Deployment successful!"