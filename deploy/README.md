# Deploying the Kylas CRM MCP Server to AWS Lambda

This runs the **existing** FastMCP `streamable-http` app on AWS Lambda behind a
public **Function URL**, so you can connect to it from **Claude Co-Work in the
cloud** — no localhost, no long-running server to babysit.

## How it works

- The app is packaged as a container image ([`../Dockerfile.lambda`](../Dockerfile.lambda)).
- The [**AWS Lambda Web Adapter**](https://github.com/awslabs/aws-lambda-web-adapter)
  runs inside the image as a Lambda extension. It bridges Lambda invocations to
  the normal uvicorn web server your app already starts — **zero code changes**.
- A **Function URL** with `RESPONSE_STREAM` gives a public HTTPS endpoint that
  supports the SSE frames MCP streamable-http uses.
- `main.py` already sets `stateless_http=True` (required — Lambda has no session
  affinity) and already resolves the Kylas key **per request** from the
  `x-api-key` header, falling back to the `KYLAS_API_KEY` env var.

## Auth model (public URL + per-user key)

The Function URL has **no AWS auth** (`AUTH_TYPE=NONE`), but every request must
carry a valid Kylas key in an `x-api-key` header. The URL is useless without a
real key, and each user brings their own — so it's effectively multi-tenant and
nothing sensitive is baked into the deployment.

> If you'd rather run single-tenant with one baked-in key, set `KYLAS_API_KEY`
> when deploying (see below). Then treat the URL itself as a secret.

## Prerequisites

On the machine you deploy from:

- **Docker** running (Docker Desktop, colima, etc.)
- **AWS CLI v2**, configured with credentials that can manage ECR, Lambda and IAM
  ```bash
  # macOS
  brew install awscli        # or: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
  aws configure              # or aws sso login / env-var credentials
  ```

## Deploy

```bash
# from the repo root
AWS_REGION=ap-south-1 ./deploy/deploy.sh
```

The script is **idempotent** — re-run it to ship a new build. It will:

1. create/reuse an ECR repo,
2. build & push the image,
3. create/reuse an IAM execution role,
4. create/update the Lambda function,
5. create/update a public Function URL with response streaming,
6. print your MCP endpoint: `https://<id>.lambda-url.<region>.on.aws/mcp`

### Configuration knobs (env vars)

| Var              | Default                     | Notes                                        |
|------------------|-----------------------------|----------------------------------------------|
| `AWS_REGION`     | `ap-south-1`                | Region to deploy into                        |
| `FUNCTION_NAME`  | `kylas-crm-mcp`             | Lambda function name                         |
| `ECR_REPO`       | `kylas-crm-mcp`             | ECR repository name                          |
| `ARCH`           | `x86_64`                    | `x86_64` or `arm64` (arm64 = cheaper Graviton) |
| `MEMORY`         | `1024`                      | MB                                           |
| `TIMEOUT`        | `120`                       | Seconds (max 900)                            |
| `KYLAS_API_KEY`  | *(empty)*                   | Set only for single-tenant (baked-in key)    |
| `KYLAS_BASE_URL` | `https://api.kylas.io/v1`   | Override for non-default Kylas envs          |

## Connect from Claude Co-Work

Add a **custom connector** pointing at the printed `/mcp` URL, and set a request
header:

```
x-api-key: <your Kylas API key>
```

## Verify

```bash
curl -i -X POST "https://<id>.lambda-url.<region>.on.aws/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-api-key: <your Kylas API key>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}'
```

A `200` with `content-type: text/event-stream` and an `initialize` result means
you're live.

## Notes & gotchas

- **Cold starts**: first hit after idle takes a few seconds (container + Python
  import). Bump `MEMORY` or add provisioned concurrency if that matters.
- **Background label refresh**: `main.py` runs a 30-min entity-label refresh
  loop. On Lambda the sandbox freezes between invocations, so that loop only
  ticks while warm — harmless, because labels also load lazily on the first
  request via middleware.
- **Timeout**: long multi-page CRM operations must finish within `TIMEOUT`
  (≤ 900 s). 120 s is plenty for normal tool calls.
- **Logs**: `aws logs tail /aws/lambda/kylas-crm-mcp --follow --region <region>`
