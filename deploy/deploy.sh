#!/usr/bin/env bash
#
# Deploy the Kylas CRM MCP Server to AWS Lambda as a container image, fronted
# by a public Function URL with response streaming. Idempotent: re-running
# updates the function in place.
#
# Prereqs on the machine running this:
#   - docker (running)
#   - aws cli v2, configured with credentials that can manage
#     ECR, Lambda and IAM  (aws configure / SSO / env vars)
#
# Usage:
#   ./deploy/deploy.sh
#
# Override any of the settings below via environment variables, e.g.:
#   AWS_REGION=ap-south-1 MEMORY=1024 ./deploy/deploy.sh
#
set -euo pipefail

# ----------------------------- configuration --------------------------------
AWS_REGION="${AWS_REGION:-ap-south-1}"          # region to deploy into
FUNCTION_NAME="${FUNCTION_NAME:-kylas-crm-mcp}"  # Lambda function name
ECR_REPO="${ECR_REPO:-kylas-crm-mcp}"            # ECR repository name
ARCH="${ARCH:-x86_64}"                           # x86_64 or arm64
MEMORY="${MEMORY:-1024}"                          # MB
TIMEOUT="${TIMEOUT:-120}"                         # seconds (max 900)
IMAGE_TAG="${IMAGE_TAG:-latest}"
# Public ingress: 'apigw' (API Gateway HTTP API) or 'function-url'.
# NOTE: some accounts block public Lambda Function URLs at the account/service
# layer (403 AccessDeniedException even with a correct public policy and no
# SCP/RCP). API Gateway is not affected, so it's the default here.
INGRESS="${INGRESS:-apigw}"
# Optional: bake in a single Kylas key for single-tenant use. Leave empty to
# require callers to pass their own `x-api-key` header (recommended).
KYLAS_API_KEY="${KYLAS_API_KEY:-}"
KYLAS_BASE_URL="${KYLAS_BASE_URL:-https://api.kylas.io/v1}"
# ----------------------------------------------------------------------------

if [[ "$ARCH" == "arm64" ]]; then
  DOCKER_PLATFORM="linux/arm64"
  LAMBDA_ARCH="arm64"
else
  DOCKER_PLATFORM="linux/amd64"
  LAMBDA_ARCH="x86_64"
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
REGISTRY="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_URI="${REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
ROLE_NAME="${FUNCTION_NAME}-role"

echo "==> Account ${ACCOUNT_ID} | region ${AWS_REGION} | arch ${LAMBDA_ARCH}"

# 1. ECR repository ----------------------------------------------------------
echo "==> Ensuring ECR repository '${ECR_REPO}'"
aws ecr describe-repositories --repository-names "$ECR_REPO" --region "$AWS_REGION" >/dev/null 2>&1 \
  || aws ecr create-repository --repository-name "$ECR_REPO" --region "$AWS_REGION" >/dev/null

echo "==> Logging Docker into ECR"
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$REGISTRY"

# 2. Build & push image ------------------------------------------------------
echo "==> Building image for ${DOCKER_PLATFORM}"
docker buildx build \
  --platform "$DOCKER_PLATFORM" \
  --provenance=false \
  -f Dockerfile.lambda \
  -t "$IMAGE_URI" \
  --push \
  .

# 3. Execution role ----------------------------------------------------------
echo "==> Ensuring IAM execution role '${ROLE_NAME}'"
if ! aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
  aws iam create-role --role-name "$ROLE_NAME" \
    --assume-role-policy-document '{
      "Version":"2012-10-17",
      "Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]
    }' >/dev/null
  aws iam attach-role-policy --role-name "$ROLE_NAME" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole >/dev/null
  echo "    waiting for role to propagate..."
  sleep 12
fi
ROLE_ARN="$(aws iam get-role --role-name "$ROLE_NAME" --query Role.Arn --output text)"

# 4. Environment variables for the function ----------------------------------
# API Gateway does a standard (buffered) invoke; Function URL streams. The LWA
# invoke mode must match the ingress, or the adapter mishandles the response.
if [[ "$INGRESS" == "apigw" ]]; then
  LWA_MODE="buffered"
else
  LWA_MODE="response_stream"
fi
ENV_VARS="KYLAS_BASE_URL=${KYLAS_BASE_URL},AWS_LWA_INVOKE_MODE=${LWA_MODE}"
if [[ -n "$KYLAS_API_KEY" ]]; then
  ENV_VARS="${ENV_VARS},KYLAS_API_KEY=${KYLAS_API_KEY}"
fi

# 5. Create or update the Lambda function ------------------------------------
if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$AWS_REGION" >/dev/null 2>&1; then
  echo "==> Updating function code"
  aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" --image-uri "$IMAGE_URI" \
    --region "$AWS_REGION" >/dev/null
  aws lambda wait function-updated --function-name "$FUNCTION_NAME" --region "$AWS_REGION"
  echo "==> Updating function configuration"
  aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --memory-size "$MEMORY" --timeout "$TIMEOUT" \
    --environment "Variables={${ENV_VARS}}" \
    --region "$AWS_REGION" >/dev/null
  aws lambda wait function-updated --function-name "$FUNCTION_NAME" --region "$AWS_REGION"
else
  echo "==> Creating function"
  aws lambda create-function \
    --function-name "$FUNCTION_NAME" \
    --package-type Image \
    --code ImageUri="$IMAGE_URI" \
    --role "$ROLE_ARN" \
    --architectures "$LAMBDA_ARCH" \
    --memory-size "$MEMORY" --timeout "$TIMEOUT" \
    --environment "Variables={${ENV_VARS}}" \
    --region "$AWS_REGION" >/dev/null
  aws lambda wait function-active --function-name "$FUNCTION_NAME" --region "$AWS_REGION"
fi

# 6. Public ingress ----------------------------------------------------------
if [[ "$INGRESS" == "apigw" ]]; then
  echo "==> Ensuring API Gateway HTTP API '${FUNCTION_NAME}-api'"
  FN_ARN="arn:aws:lambda:${AWS_REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}"
  API_ID="$(aws apigatewayv2 get-apis --region "$AWS_REGION" \
    --query "Items[?Name=='${FUNCTION_NAME}-api'].ApiId | [0]" --output text 2>/dev/null)"
  if [[ -z "$API_ID" || "$API_ID" == "None" ]]; then
    # quick-create wires integration + $default route + auto-deployed $default stage
    API_ID="$(aws apigatewayv2 create-api --name "${FUNCTION_NAME}-api" \
      --protocol-type HTTP --target "$FN_ARN" --region "$AWS_REGION" \
      --query ApiId --output text)"
  fi
  # permission for API Gateway to invoke the function (idempotent)
  aws lambda add-permission --function-name "$FUNCTION_NAME" --region "$AWS_REGION" \
    --statement-id apigw-invoke --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:${AWS_REGION}:${ACCOUNT_ID}:${API_ID}/*/*" \
    >/dev/null 2>&1 || true
  API_ENDPOINT="$(aws apigatewayv2 get-api --api-id "$API_ID" --region "$AWS_REGION" \
    --query ApiEndpoint --output text)"
  MCP_URL="${API_ENDPOINT%/}/mcp"
else
  echo "==> Ensuring Function URL (auth NONE, RESPONSE_STREAM)"
  echo "    (heads up: some accounts block public Function URLs — see deploy/README.md)"
  if ! aws lambda get-function-url-config --function-name "$FUNCTION_NAME" --region "$AWS_REGION" >/dev/null 2>&1; then
    aws lambda create-function-url-config \
      --function-name "$FUNCTION_NAME" \
      --auth-type NONE \
      --invoke-mode RESPONSE_STREAM \
      --region "$AWS_REGION" >/dev/null
    aws lambda add-permission \
      --function-name "$FUNCTION_NAME" \
      --statement-id FunctionURLAllowPublicAccess \
      --action lambda:InvokeFunctionUrl \
      --principal '*' \
      --function-url-auth-type NONE \
      --region "$AWS_REGION" >/dev/null 2>&1 || true
  else
    aws lambda update-function-url-config \
      --function-name "$FUNCTION_NAME" \
      --auth-type NONE \
      --invoke-mode RESPONSE_STREAM \
      --region "$AWS_REGION" >/dev/null
  fi
  FUNCTION_URL="$(aws lambda get-function-url-config --function-name "$FUNCTION_NAME" --region "$AWS_REGION" --query FunctionUrl --output text)"
  MCP_URL="${FUNCTION_URL%/}/mcp"
fi

echo ""
echo "============================================================"
echo " Deployed."
echo " MCP endpoint:  ${MCP_URL}"
echo "============================================================"
echo " Add to Claude Co-Work as a custom connector with header:"
echo "   x-api-key: <your Kylas API key>"
echo "============================================================"
