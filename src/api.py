from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from helper import save_file
from Algorithm import main, data_path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/", response_class=FileResponse)
async def process_image(
        points: str = Form(...),
        iterations: str = Form(...),
        k: str = Form(...),
        file: UploadFile = File(...),
):
    file_name = file.filename
    save_file(file, data_path)
    points, iterations, k = int(points), int(iterations), int(k)

    main(file_name, points, iterations, k)

    return data_path + f'output-{file_name}'
