# Industrial Defect Detection & Quality-Control Assistant

A Phase 1 prototype for PS5: Real-time Industrial Defect Detection & Quality-Control Assistant.

## What this prototype does

- Accepts a known-good reference product image.
- Accepts an image of a product to inspect.
- Compares the two images using OpenCV.
- Highlights regions that differ from the reference.
- Reports the number and approximate size of difference regions.
- Allows the annotated result to be downloaded.

## Important limitation

This is a classical computer-vision proof of concept, not a trained AI defect-detection model.
It does not reliably identify defect categories such as crack, scratch, dent, or corrosion.
Lighting, camera angle, object position, and scale can create false detections. Use controlled
images and manually verify results. Do not use it for safety-critical or production decisions.

The challenge's Llama and ExecuTorch requirements are not implemented in this starter version.
They must be integrated and tested separately if required by the official PS5 rules.

## Run on Windows

1. Install Python 3.10 or newer.
2. Open Command Prompt in this project folder.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate it:

   ```bash
   .venv\\Scripts\\activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the app:

   ```bash
   streamlit run app.py
   ```

7. Your browser should open the local dashboard.

## GitHub upload

Create a new empty GitHub repository, then run these commands in the project folder:

```bash
git init
git add .
git commit -m "Add industrial defect inspection prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your own repository URL.
