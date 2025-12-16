from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import base64
from pathlib import Path
import uuid
import uvicorn

app = FastAPI()

# ----- 1. INPUT MODEL (Accept entire connector output) -----
class ConnectorPayload(BaseModel):
    # payload may contain many keys – we only need base64
    base64: str
    fileName: str | None = None   # optional filename sent from Power Automate
    folder: str | None = None     # optional grouping

# ----- 2. ENDPOINT -----
@app.post("/decode-doc")
async def decode_doc(payload: ConnectorPayload):

    # 2. Extract Base64 into a variable
    b64_string = payload.base64

    # Remove data-prefix if present (e.g., "data:application/...;base64,xxxx")
    if "," in b64_string:
        b64_string = b64_string.split(",")[1]

    # 3. Decode Base64 → Recreate file
    file_bytes = base64.b64decode(b64_string)

    # Determine output filename
    safe_name = payload.fileName or f"decoded_{uuid.uuid4()}.doc"
    output_path = Path(f"/tmp/{safe_name}")

    # Save decoded file
    output_path.write_bytes(file_bytes)

    # 4. Make the file downloadable (return it directly)
    return FileResponse(
        path=output_path,
        filename=safe_name,
    #     media_type="application/msword"
        media_type= "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

# -------------------------------
# Run locally
# -------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
