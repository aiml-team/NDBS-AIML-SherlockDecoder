import base64
import os
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn


app = FastAPI()


# -------------------------------
# Model for input JSON
# -------------------------------
class FileData(BaseModel):
    filename: str    # dynamic from Get file metadata
    filecontent: str    # Base64 from Power Automate



# -------------------------------
# Endpoint: /decode-docx
# -------------------------------
@app.post("/decode-docx")
async def decode_docx(data: FileData):
    try:
        # 1. Extract Base64 content
        b64_string = data.filecontent

        # Remove prefix like: data:application/...;base64,<content>
        if "," in b64_string:
            b64_string = b64_string.split(",", 1)[1]

        # 2. Decode Base64
        file_bytes = base64.b64decode(b64_string)

        # 3. Build output file name
        base_name = os.path.splitext(data.filename)[0]
        output_filename = f"{base_name}_output.docx"

        # 4. Save file in OS temp folder (auto cleaned)
        temp_dir = tempfile.gettempdir()
        save_path = os.path.join(temp_dir, output_filename)

        with open(save_path, "wb") as f:
            f.write(file_bytes)

        print(f"Saved decoded file at: {save_path}")

        # 5. Return file to Power Automate
        return FileResponse(
            save_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=output_filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decoding file: {str(e)}")



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