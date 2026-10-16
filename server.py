import hashlib
import os
from mcp.server.fastmcp import FastMCP, Context
from starlette.requests import Request
from starlette.responses import PlainTextResponse

EMAIL = "23f2005623@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP(
    "exam-server",
    host="0.0.0.0",                          # listen to the outside world
    port=int(os.environ.get("PORT", 9002)),  # hosting sites tell us the port
    stateless_http=True,                     # no sessions: every call stands alone
    json_response=True,                      # plain JSON replies (simpler)
)

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request):
    return PlainTextResponse("ok")

@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the first 16 hex chars of SHA-256('<challenge>:<email>')."""
    request = ctx.request_context.request            # the raw HTTP request
    challenge = request.headers.get("x-exam-challenge", "")  # read the header
    digest = hashlib.sha256(f"{challenge}:{EMAIL}".encode()).hexdigest()
    return digest[:16]

if __name__ == "__main__":
    mcp.run(transport="streamable-http")