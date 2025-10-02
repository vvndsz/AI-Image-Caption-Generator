# 🧠 AI-Powered Image Caption Generator 🤖

Generate intelligent and personalized image captions with tones like **casual**, **formal**, **humorous**, **poetic**, and more — using OpenAI’s BLIP model.

**Features:**
- 📤 Upload images directly from your device.
- 🎨 Choose a tone (casual, poetic, humorous, etc.).
- 📝 Generate automatic captions using **real computer vision AI**.
- 💬 Tone-adapted caption outputs.
- ⚡ Fast startup with optional **mock AI mode** (no ML backend required).
- 📱 Ready for integration with social media APIs.

**Home Page**
![upload](\Upload.png)
**Setting the tone**
![tone](\Tone.png)
**Generation of Caption**
![caption](\Caption.png)

---

## Technologies Used

- **Frontend:** React.js, TailwindCSS
- **Backend:** FastAPI 
- **Model:** Salesforce BLIP 
- **AI Library:** Transformers 
- **Others:** Axios, React-Dropzone, Redis

---

## Project Structure

```
ai-img-captioner/
│
├── backend/
│   ├── app/
│   │   ├── main_full.py          ← Full AI model (real captions)
│   │   └── ... (config, processors, utils)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   └── public/
│       └── index.html, favicon.ico
│
└── README.md
```

---

##  Backend Setup (FastAPI + BLIP)

### AI-Powered Captions using BLIP

```bash
cd backend
pip install torch torchvision transformers pillow fastapi uvicorn python-multipart
python app/main_full.py
```

>  First-time use will **download BLIP model (~900 MB)**.

>  Each image will generate **contextually unique, AI-generated** captions!

---

##  Frontend Setup (React App)

```bash
cd frontend
npm install
npm start
```

The app will open at:  
➡️ `http://localhost:3000`

You can upload an image and select a tone to generate custom captions.

---

##  Full Stack Running Together

Ensure both backend and frontend are running in different terminal windows:

| Terminal 1 (Backend) | Terminal 2 (Frontend)    |
|----------------------|--------------------------|
| `python main_full.py`| `cd frontend && npm start` |

---

##  Docker Setup (optional)

**Coming Soon...** *(You can implement using Dockerfiles already in `backend/` and `frontend/`)*
```bash
docker-compose up --build
```

---

##  Available Caption Tones

| Tone         | Description                |
|--------------|----------------------------|
| `formal`     | Professional and descriptive |
| `casual`     | Friendly, conversational     |
| `humorous`   | Funny and witty              |
| `poetic`     | Lyrical and evocative        |
| `technical`  | Analytical and detailed      |
| `marketing`  | Persuasive and engaging      |
| `storytelling` | Narrative, imaginative    |

---

##  Endpoints - API (FastAPI Docs)

Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

| Endpoint                 | Method | Description                              |
|--------------------------|--------|------------------------------------------|
| `/api/v1/caption`       | POST   | Upload image and get caption (with tone) |
| `/api/v1/tones`         | GET    | List available tones                     |
| `/api/v1/health`        | GET    | Server health check                      |
| `/api/v1/test`          | GET    | Simple test endpoint                     |
| `/api/v1/model/status`  | GET    | (Optional) Check model status            |
| `/api/v1/model/reload`  | POST   | (Optional) Reload the model              |

---

##  Tips

-  If you get **"Could not find index.html"**, ensure `frontend/public/index.html` exists.
-  If `uvicorn` reloads are giving warnings:
  - Use CLI: `uvicorn app.main_full:app --reload`
-  On slow machines or internet? Use `main_light.py` for instant testing.
-  Want more tones? Add templates in `adapt_caption_to_tone()`.

---

## Ideas for Future

- [ ]  DB support to store captions
- [ ]  Translation into other languages
- [ ]  Support for mobile camera capture
- [ ]  Add OpenAI/GPT API to rewrite tones

---

##  Credits

- [Salesforce BLIP](https://github.com/salesforce/BLIP)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [FastAPI](https://fastapi.tiangolo.com)
- [React + Tailwind](https://tailwindcss.com)

---