import streamlit as st
import io
import struct
import json
from collections import defaultdict

# Page configuration
st.set_page_config(
    page_title="3D File Layer Extractor",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: white;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    .file-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .error-card {
        border-left-color: #ef4444;
        background: #fef2f2;
    }
    .layer-item {
        background: #f9fafb;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #667eea;
    }
    .file-type-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def parse_glb(file_bytes, filename):
    """Parse GLB file and extract material names"""
    try:
        # Read GLB header
        magic = struct.unpack('<I', file_bytes[0:4])[0]
        if magic != 0x46546C67:  # "glTF" in ASCII
            return None, "Not a valid GLB file"
        
        version = struct.unpack('<I', file_bytes[4:8])[0]
        length = struct.unpack('<I', file_bytes[8:12])[0]
        
        # Find JSON chunk
        offset = 12
        json_data = None
        
        while offset < len(file_bytes):
            chunk_length = struct.unpack('<I', file_bytes[offset:offset+4])[0]
            chunk_type = struct.unpack('<I', file_bytes[offset+4:offset+8])[0]
            
            if chunk_type == 0x4E4F534A:  # "JSON" in ASCII
                json_bytes = file_bytes[offset+8:offset+8+chunk_length]
                json_data = json.loads(json_bytes.decode('utf-8'))
                break
            
            offset += 8 + chunk_length
        
        if not json_data:
            return None, "No JSON chunk found in GLB file"
        
        # Extract material names
        materials = json_data.get('materials', [])
        material_names = []
        
        for idx, material in enumerate(materials):
            name = material.get('name', f'Unnamed_{idx}')
            material_names.append(name)
        
        return material_names, None
        
    except Exception as e:
        return None, str(e)

def parse_3dm(file_bytes, filename):
    """Parse 3DM file and extract layer names"""
    try:
        # Try importing rhino3dm
        try:
            import rhino3dm
        except ImportError:
            return None, "rhino3dm library not installed. Install with: pip install rhino3dm"
        
        # Read the 3DM file
        model = rhino3dm.File3dm.FromByteArray(file_bytes)
        
        if not model:
            return None, "Failed to parse 3DM file"
        
        # Extract unique layer names
        layer_names = set()
        
        for obj in model.Objects:
            layer_index = obj.Attributes.LayerIndex
            if layer_index < len(model.Layers):
                layer = model.Layers[layer_index]
                layer_names.add(layer.Name)
        
        return sorted(list(layer_names)), None
        
    except Exception as e:
        return None, str(e)

def main():
    # Header
    st.markdown("<h1>🎨 3D File Layer Extractor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Extract material and layer names from GLB and 3DM files</p>", unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload your 3D files (.glb or .3dm)",
        type=['glb', '3dm'],
        accept_multiple_files=True,
        help="You can upload multiple files at once"
    )
    
    if uploaded_files:
        # Process files
        results = []
        
        with st.spinner('Processing files...'):
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension == 'glb':
                    layers, error = parse_glb(file_bytes, uploaded_file.name)
                    file_type = 'GLB'
                elif file_extension == '3dm':
                    layers, error = parse_3dm(file_bytes, uploaded_file.name)
                    file_type = '3DM'
                else:
                    layers = None
                    error = "Unsupported file type"
                    file_type = 'UNKNOWN'
                
                results.append({
                    'filename': uploaded_file.name,
                    'file_type': file_type,
                    'layers': layers if layers else [],
                    'error': error
                })
        
        # Statistics
        total_files = len(results)
        total_layers = sum(len(r['layers']) for r in results)
        successful_files = sum(1 for r in results if not r['error'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display stats in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-value'>{total_files}</div>
                    <div class='stat-label'>Files Processed</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-value'>{total_layers}</div>
                    <div class='stat-label'>Total Layers Found</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-value'>{successful_files}</div>
                    <div class='stat-label'>Successful Extractions</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display results
        st.markdown("### 📊 Results")
        
        for result in results:
            card_class = 'error-card' if result['error'] else 'file-card'
            
            with st.container():
                st.markdown(f"""
                    <div class='{card_class}'>
                        <h4>{result['filename']} <span class='file-type-badge'>{result['file_type']}</span></h4>
                    </div>
                """, unsafe_allow_html=True)
                
                if result['error']:
                    st.error(f"❌ Error: {result['error']}")
                elif not result['layers']:
                    st.info("ℹ️ No layers or materials found")
                else:
                    for layer in result['layers']:
                        st.markdown(f"""
                            <div class='layer-item'>
                                🔹 {layer}
                            </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Clear button
        if st.button("🗑️ Clear All", type="secondary", use_container_width=True):
            st.rerun()
    
    else:
        # Instructions when no files uploaded
        st.info("""
        👆 **How to use:**
        1. Click the upload button above
        2. Select one or more .glb or .3dm files
        3. View the extracted layer/material names instantly
        
        **Supported formats:**
        - `.glb` - Extracts material names
        - `.3dm` - Extracts layer names (requires rhino3dm library)
        """)

if __name__ == "__main__":
    main()
