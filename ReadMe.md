# Iso-Surface and Volume Rendering Application

This application demonstrates iso-surface extraction and volume rendering using VTK. It supports multiple datasets (5 currently) and provides interactive controls for adjusting iso-values and opacity.

## Features
- Load and visualize volumetric datasets.
- Switch between **iso-surface extraction** and **volume rendering**.
- Adjust iso-values interactively using **keyboard keys**.
- Adjust opacity using a **slider widget**.
- Toggle opacity slider visibility using a keyboard key.

## Datasets
- **Head**: Uses `.mhd` and `.raw` files.
- **Foot**: Uses 256 images.
- **Frog**: Uses 44 images.
- **Aneurism**: Uses 256 images.
- **Teapot**: Uses 178 images.

## Usage

### Keyboard Controls
- **1**: Load head dataset.
- **2**: Load foot dataset.
- **3**: Load frog dataset.
- **4**: Load aneurism dataset.
- **5**: Load teapot dataset.
- **up arrow**: Increase iso-value by 20.
- **down arrow**: Decrease iso-value by 10.
- **v**: Switch to volume rendering mode.
- **s**: Switch to iso-surface extraction mode.
- **t**: Toggle opacity slider visibility.

### Slider Widget
- Adjust the opacity of the volume rendering.

## Installation and Running
1. Install VTK if not already installed:
    ```
    pip install vtk
    ```
2. Place the dataset files in the appropriate folders.
3. Run the script:
    ```
    python Part1A1B.py
    ```

## Important Surfaces
- **Head**: Skin (iso-value 500), Bone/Skull (iso-value 1150).
- **Foot** : Foot is visible (iso-value 10) Bone (Iso-value 100)
- **Frog** : Frog is seen at  iso-value 40 / frog frame at iso-value 130
- **Aneurism** : Full view of the blood vessels (iso-value 10)  Clear view of the bulge (iso value 200)
- **Teapot** : teapot is on surface (iso-value 10) / a scorpion or crawfish is seen (iso-value 130 )

## Contributors
- [Adam Azhar Bin Nor Adha A21EC8010](adamazhar@graduate.utm.my)

## Purpose
This project is done for the Data Visualisation Group Project 2023242 