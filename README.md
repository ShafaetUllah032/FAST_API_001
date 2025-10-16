# FAST_API Project

This project is built using [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance) web framework for building APIs with Python 3.7+.

## Features

- High performance API endpoints
- Automatic interactive API documentation (Swagger UI & ReDoc)
- Easy integration with databases
- Asynchronous request handling

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/FAST_API.git
    cd FAST_API
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

2. Access the API documentation:
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
    - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
FAST_API/
├── main.py
├── requirements.txt
├── README.md
└── ...
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.