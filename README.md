# EcoNom-y

# Setup

### Clone the Repository

```bash
git clone https://github.com/digitalyoshixi/EcoNom-y
cd EcoNom-y
```

### Install Dependencies

```bash
py -m pip install -r requirements.txt  # Windows
python3 -m pip install -r requirements.txt  # Unix (MacOS or Linux)
```

### Set Environment Variables

```bash
cp .env.example .env  # Copy .env.example to .env
vim .env  # Add a Gemini API key to .env
```

See the [docs](https://ai.google.dev/gemini-api/docs/api-key) for information on how to create an API key.

### Run the Server

```bash
python3 main.py
```
