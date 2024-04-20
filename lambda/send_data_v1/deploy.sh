project_id=$1
ecr_repo=$2
function_name=$3
region=$4
build_version=$5
img_uri=$project_id.dkr.ecr.$region.amazonaws.com/$ecr_repo:$function_name-$build_version
docker build -t $img_uri .
docker push $img_uri
# deployment=$(aws lambda update-function-code --function-name $function_name --environment 'Variables={base_url=https://f195-2401-4900-52fd-3b77-4083-b14f-d858-195a.ngrok-free.app,ack_endpoint=/v1/data_transfer_ack}' --image-uri $img_uri)
config_update=$(aws lambda update-function-configuration --function-name $function_name --timeout 300 --memory-size 1024 --environment "Variables={callback_base_url=https://8c8b-2402-e280-3e33-1da-812b-5b-2f14-de6.ngrok-free.app}")
deployment=$(aws lambda update-function-code --function-name $function_name --image-uri $img_uri)
while true; do
    echo "---------Checking deployment status----------"
    deployment_status=$(aws lambda get-function --function-name $function_name --output json --query Configuration.LastUpdateStatus | tr -d '"')
    echo "Deployment Status: ${deployment_status}"
    if [ "$deployment_status" = "Successful" ]; then
        echo "Deployment successful"
        break
    elif [ "$deployment_status" = "Failed" ]; then
        echo "Deployment failed"
        break
    fi
    echo "Sleeping for 5 seconds"
    sleep 5
done