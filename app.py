#!/usr/bin/env python3
import streamlit as st
import platform
import os
import time

# Set page config
st.set_page_config(
    page_title="Stress & Strain Analyzer",
    page_icon="🏗️",
    layout="wide"
)

# Materials database
materials = {
    'steel': {
        'name': 'Mild Steel',
        'density': 7850,  # Corrected density (kg/m3)
        'young': 210000,  # MPa (210 GPa in MPa)
        'poisson': 0.3,
        'color': '#b3cde0'
    },
    'aluminum': {
        'name': 'Aluminum Alloys',
        'density': 2700,
        'young': 69000,
        'poisson': 0.33,
        'color': '#d9d9d9'
    },
    'timber': {
        'name': 'Timber',
        'density': 600,  # Typical softwood
        'young': 11000,
        'poisson': 0.3,
        'color': '#c2b280'
    }
}

# Section database with ASCII art
sections = {
    'I-beam': '''
  <-- b -->   
t  XXXXXXXX  |
      XX     | 
e---->XX     h
      XX     |
   XXXXXXXX  |''',
    'T-beam': '''
   <-- b -->   
t  XXXXXXXX  |
      XX     | 
e---->XX     h
      XX     |
      XX     |''',
    'Rectangle': '''
  <-- b -->   
  XXXXXXXX  |
  XXXXXXXX  |
  XXXXXXXX  h
  XXXXXXXX  |
  XXXXXXXX  |''',
    'Hollow Rectangle': '''
   <-- b -->   
t-->XXXXXXXX  |
    XX    XX  |
e-->XX    XX  h
    XX    XX  |
    XXXXXXXX  |''',
    'Circle': '''
       |-r-->   
     xxxx             
  xXXXXXXXXx       
 xXXXXXXXXXXx      
 xXXXXXXXXXXx      
  xXXXXXXXXx        
     xXXx     ''',
    'Hollow Circle': '''
       |-r-->   
     x  x             
  x        x            
 x          x <-- e     
 x          x      
  x        x        
     x  x     '''
}

# --- Streamlit UI ---
st.title("🏗️ Structural Stress & Strain Analyzer")
st.markdown("""
An interactive tool for basic structural engineering calculations.
""")

# Sidebar controls
with st.sidebar:
    st.header("Material Properties")
    material_choice = st.selectbox(
        "Select Material",
        list(materials.keys()),
        format_func=lambda x: materials[x]['name']
    )
    
    st.header("Cross Section")
    section_choice = st.selectbox(
        "Select Section Type",
        list(sections.keys())
    )

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Material Properties")
    mat = materials[material_choice]
    
    st.metric("Name", mat['name'])
    st.metric("Young's Modulus", f"{mat['young']:,} MPa")
    st.metric("Poisson's Ratio", mat['poisson'])
    st.metric("Density", f"{mat['density']} kg/m³")
    
    # Stress-Strain visualization placeholder
    st.subheader("Stress-Strain Curve")
    st.line_chart({
        'Strain': [0, 0.001, 0.002, 0.003, 0.004],
        'Stress (MPa)': [0, mat['young']*0.001, mat['young']*0.002, mat['young']*0.003, mat['young']*0.004]
    })

with col2:
    st.subheader("Cross Section")
    st.code(sections[section_choice], language='text')
    
    # Section dimensions input
    with st.expander("Section Dimensions"):
        if 'beam' in section_choice.lower():
            b = st.number_input("Width (b) [mm]", 50, 1000, 200)
            h = st.number_input("Height (h) [mm]", 50, 1000, 400)
            t = st.number_input("Flange Thickness (t) [mm]", 5, 50, 10)
            e = st.number_input("Web Thickness (e) [mm]", 5, 50, 8)
        else:
            r = st.number_input("Radius (r) [mm]", 10, 500, 100)
            e = st.number_input("Wall Thickness (e) [mm]", 2, 50, 5)
    
    # Basic calculations
    with st.expander("Basic Calculations"):
        force = st.number_input("Applied Force (N)", 1000, 1000000, 50000)
        area = b * h if 'beam' in section_choice.lower() else 3.14 * r**2
        stress = force / (area * 1e-6)  # Convert mm² to m²
        strain = stress / mat['young']
        
        st.metric("Stress", f"{stress:,.2f} MPa")
        st.metric("Strain", f"{strain:.6f}")

# Footer
st.markdown("---")
st.caption("""
Developed with Python & Streamlit | [GitHub Repository](#)
""")