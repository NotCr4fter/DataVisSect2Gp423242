# Iso-Surface and Volume Rendering Application

This application demonstrates iso-surface extraction and volume rendering using VTK. It supports multiple datasets and provides interactive controls for adjusting iso-values and opacity.

## Features
- Load and visualize volumetric datasets.
- Switch between iso-surface extraction and volume rendering.
- Adjust iso-values interactively using keyboard keys.
- Adjust opacity using a slider widget.
- Toggle opacity slider visibility using a keyboard key.

## Datasets
- **Head**: Uses `.mhd` and `.raw` files.
- **Foot**: Uses 256 images.
- **Frog**: Uses 44 images.
- **Aneurism**: Uses 256 images.
- **Teapot**: Uses 256 images.

## Usage

### Keyboard Controls
- **1**: Load head dataset.
- **2**: Load foot dataset.
- **3**: Load frog dataset.
- **4**: Load aneurism dataset.
- **5**: Load teapot dataset.
- **i**: Increase iso-value by 20.
- **d**: Decrease iso-value by 10.
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
    python PartAB.py
    ```

## Important Surfaces
- **Head**: Skin (iso-value 500), Bone (iso-value 1150).
- **Foot, Frog, Aneurism, Teapot**: Adjust iso-values interactively to locate interesting surfaces.

## Customization
You can customize the color and opacity transfer functions for different datasets in the script. Modify the `create_transfer_functions` function to set the desired values.

## Contributors
- [Your Name](mailto:your.email@example.com)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
