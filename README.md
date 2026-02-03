# 3D File Layer Extractor - Streamlit App

A web application to extract material names from GLB files and layer names from 3DM files.

## Features

- ✅ Upload multiple GLB and 3DM files
- ✅ Extract material names from GLB files
- ✅ Extract layer names from 3DM files
- ✅ Beautiful, responsive UI with statistics
- ✅ Batch processing support
- ✅ Error handling for corrupted files

## Local Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the app:**
```bash
streamlit run app.py
```

3. **Open your browser:**
The app will automatically open at `http://localhost:8501`

## Deploy to Streamlit Cloud (FREE)

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Name it something like `3d-layer-extractor`
4. Make it Public
5. Click "Create repository"

### Step 2: Upload Your Files

You have two options:

**Option A: Upload via GitHub website**
1. Click "uploading an existing file"
2. Drag and drop these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. Click "Commit changes"

**Option B: Use Git command line**
```bash
git init
git add app.py requirements.txt README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/3d-layer-extractor.git
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository:** your-username/3d-layer-extractor
   - **Branch:** main
   - **Main file path:** app.py
5. Click "Deploy!"

🎉 Your app will be live in 2-3 minutes at:
`https://your-app-name.streamlit.app`

## File Structure

```
3d-layer-extractor/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Supported File Types

- `.glb` - Binary glTF files (extracts material names)
- `.3dm` - Rhino 3D files (extracts layer names)

## How It Works

### GLB Files
- Parses the binary GLB format
- Extracts JSON chunk containing material definitions
- Lists all material names (or "Unnamed_X" for unnamed materials)

### 3DM Files
- Uses the `rhino3dm` library to read Rhino files
- Iterates through all objects in the file
- Extracts unique layer names from object attributes

## Troubleshooting

**Issue:** "rhino3dm library not installed"
- **Solution:** Make sure `requirements.txt` contains `rhino3dm>=8.0.0`

**Issue:** Files not uploading
- **Solution:** Check file size limits (Streamlit Cloud has a 200MB limit per file)

**Issue:** App crashes on 3DM files
- **Solution:** Ensure the 3DM file is not corrupted and is a valid Rhino file

## Support

For issues or questions, create an issue on the GitHub repository.

## License

MIT License - Feel free to use and modify as needed!
