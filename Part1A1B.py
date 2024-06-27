import vtk
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkInteractionWidgets import (
    vtkSliderRepresentation2D,
    vtkSliderWidget,
    vtkTextWidget
)
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkMarchingCubes,
    vtkStripper
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter

# Function to read volume from a folder of numbered images
def read_volume(folder_path, file_prefix, start=1, end=256, dimensions=(256, 256), spacing=(1, 1, 1)):
    reader = vtk.vtkVolume16Reader()
    reader.SetFilePrefix(folder_path + "/" + file_prefix)
    reader.SetImageRange(start, end)
    reader.SetDataDimensions(*dimensions)
    reader.SetDataSpacing(*spacing)
    reader.SetDataByteOrderToLittleEndian()
    reader.Update()
    return reader

# Function to read a MetaImage volume (for the head dataset)
def read_metaimage(file_path):
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader

# Function to create an iso-surface extraction actor
def create_isosurface_actor(reader, iso_value):
    contour_filter = vtk.vtkContourFilter()
    contour_filter.SetInputConnection(reader.GetOutputPort())
    contour_filter.SetValue(0, iso_value)
    
    contour_mapper = vtk.vtkPolyDataMapper()
    contour_mapper.SetInputConnection(contour_filter.GetOutputPort())
    contour_mapper.ScalarVisibilityOff()
    
    contour_actor = vtk.vtkActor()
    contour_actor.SetMapper(contour_mapper)
    
    return contour_actor

# Function to create a volume rendering actor
def create_volume_actor(reader, color_function, opacity_function):
    volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volume_mapper.SetInputConnection(reader.GetOutputPort())

    volume_property = vtk.vtkVolumeProperty()
    volume_property.ShadeOn()
    volume_property.SetInterpolationTypeToLinear()
    volume_property.SetColor(color_function)
    volume_property.SetScalarOpacity(opacity_function)

    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    return volume

# Define color and opacity transfer functions for the datasets
def create_transfer_functions():
    color_function = vtk.vtkColorTransferFunction()
    color_function.AddRGBPoint(0, 0.0, 0.0, 0.0)
    color_function.AddRGBPoint(500, 1.0, 0.5, 0.3)
    color_function.AddRGBPoint(1000, 1.0, 1.0, 0.9)

    opacity_function = vtk.vtkPiecewiseFunction()
    opacity_function.AddPoint(0, 0.0)
    opacity_function.AddPoint(500, 0.2)
    opacity_function.AddPoint(1000, 0.4)

    return color_function, opacity_function

# Load the head model
head_file_path = "./headDataset/FullHead.mhd"
head_reader = read_metaimage(head_file_path)
head_color_function, head_opacity_function = create_transfer_functions()

# Create initial iso-surface actor
iso_value = 500  # Starting iso-value
iso_actor = create_isosurface_actor(head_reader, iso_value)

# Create volume rendering actor
volume_actor = create_volume_actor(head_reader, head_color_function, head_opacity_function)

# Create an outline
outline_filter = vtk.vtkOutlineFilter()
outline_filter.SetInputConnection(head_reader.GetOutputPort())

# Create a transform to scale the outline
transform = vtk.vtkTransform()
transform.Scale(1.2, 1.2, 1.2)  # Adjust these values to scale the outline box

transform_filter = vtk.vtkTransformFilter()
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(outline_filter.GetOutputPort())

outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(transform_filter.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.StereoCapableWindowOff()  # Disable stereo rendering
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Add actors to the scene
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(1, 1, 1)  # Background color white

# Initialize camera
camera = vtk.vtkCamera()
camera.SetViewUp(0, 0, -1)
camera.SetPosition(0, 1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.ComputeViewPlaneNormal()
renderer.SetActiveCamera(camera)
renderer.ResetCamera()
camera.Dolly(1.5)

# Reset camera clipping range
renderer.ResetCameraClippingRange()

# Volume datasets
volume_datasets = {
    "head": {"reader": head_reader, "color_function": head_color_function, "opacity_function": head_opacity_function},
    "foot": {"folder_path": "./footDataset", "file_prefix": "foot", "dimensions": (256, 256), "spacing": (1, 1, 1), "end": 256},
    "frog": {"folder_path": "./wholeFrogDataset", "file_prefix": "frog2ci", "dimensions": (256, 256), "spacing": (1, 1, 1), "end": 44},
    "aneurism": {"folder_path": "./aneurismDataset", "file_prefix": "aneurism", "dimensions": (256, 256), "spacing": (1, 1, 1), "end": 256},
    "teapot": {"folder_path": "./teapotDataset", "file_prefix": "teapot", "dimensions": (256, 256), "spacing": (1, 1, 1), "end": 178}
}

# Function to load and create actors for different volumes
def load_volume(volume_name):
    if volume_name == "head":
        reader = volume_datasets[volume_name]["reader"]
        color_function = volume_datasets[volume_name]["color_function"]
        opacity_function = volume_datasets[volume_name]["opacity_function"]
    else:
        folder_path = volume_datasets[volume_name]["folder_path"]
        file_prefix = volume_datasets[volume_name]["file_prefix"]
        dimensions = volume_datasets[volume_name]["dimensions"]
        spacing = volume_datasets[volume_name]["spacing"]
        end = volume_datasets[volume_name]["end"]
        reader = read_volume(folder_path, file_prefix, end=end, dimensions=dimensions, spacing=spacing)
        color_function, opacity_function = create_transfer_functions()
    iso_actor = create_isosurface_actor(reader, iso_value)
    volume_actor = create_volume_actor(reader, color_function, opacity_function)
    return reader, iso_actor, volume_actor

# Create a text actor to display the current iso-value
iso_value_text = vtk.vtkTextActor()
iso_value_text.SetInput(f"Iso-value: {iso_value}")
iso_value_text.GetTextProperty().SetFontSize(24)
iso_value_text.GetTextProperty().SetColor(0,0,0)
iso_value_text.SetDisplayPosition(550, 10)

renderer.AddActor2D(iso_value_text)

# Function to update the text actor with the current iso-value
def update_iso_value_text(iso_value):
    iso_value_text.SetInput(f"Iso-value: {iso_value}")

# Slider callback function to update opacity
def opacity_slider_callback(obj, event):
    opacity = obj.GetRepresentation().GetValue()
    head_opacity_function.RemoveAllPoints()
    head_opacity_function.AddPoint(0, 0.0)
    head_opacity_function.AddPoint(500, opacity)
    head_opacity_function.AddPoint(1000, 0.4)
    renderWindow.Render()

# Create an opacity slider widget
slider_rep = vtk.vtkSliderRepresentation2D()
slider_rep.SetMinimumValue(0.0)
slider_rep.SetMaximumValue(1.0)
slider_rep.SetValue(0.2)
slider_rep.SetTitleText("Opacity")
slider_rep.GetSliderProperty().SetColor(1, 0, 0)
slider_rep.GetTitleProperty().SetColor(1, 0, 0)
slider_rep.GetLabelProperty().SetColor(1, 0, 0)
slider_rep.GetSelectedProperty().SetColor(0, 1, 0)
slider_rep.GetTubeProperty().SetColor(1, 1, 0)
slider_rep.GetCapProperty().SetColor(1, 1, 0)
slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint1Coordinate().SetValue(0.1, 0.1)
slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint2Coordinate().SetValue(0.3, 0.1)

slider_widget = vtk.vtkSliderWidget()
slider_widget.SetInteractor(renderWindowInteractor)
slider_widget.SetRepresentation(slider_rep)
slider_widget.SetAnimationModeToAnimate()
slider_widget.EnabledOn()
slider_widget.AddObserver("EndInteractionEvent", opacity_slider_callback)

# Function to toggle the slider widget
def toggle_slider(obj, event):
    global slider_widget
    if slider_widget.GetEnabled():
        slider_widget.EnabledOff()
    else:
        slider_widget.EnabledOn()
    renderWindow.Render()

# Keyboard callback to switch between rendering modes and change iso-value or ray step size
def keypress_callback(obj, event):
    global iso_value, iso_actor, volume_actor, current_volume, head_reader, head_color_function, head_opacity_function
    key = obj.GetKeySym()
    if key == "i":
        iso_value += 20
        print(f"Iso-value: {iso_value}")
        renderer.RemoveActor(iso_actor)
        iso_actor = create_isosurface_actor(head_reader, iso_value)
        renderer.AddActor(iso_actor)
        update_iso_value_text(iso_value)
    elif key == "d":
        iso_value -= 10
        print(f"Iso-value: {iso_value}")
        renderer.RemoveActor(iso_actor)
        iso_actor = create_isosurface_actor(head_reader, iso_value)
        renderer.AddActor(iso_actor)
        update_iso_value_text(iso_value)
    elif key == "v":
        renderer.RemoveActor(iso_actor)
        renderer.AddVolume(volume_actor)
        print("Switched to volume rendering mode")
    elif key == "s":
        renderer.RemoveVolume(volume_actor)
        renderer.AddActor(iso_actor)
        print("Switched to iso-surface extraction mode")
    elif key == "t":
        toggle_slider(obj, event)
    elif key in ["1", "2", "3", "4", "5"]:
        volumes = ["head", "foot", "frog", "aneurism", "teapot"]
        current_volume = volumes[int(key) - 1]
        head_reader, iso_actor, volume_actor = load_volume(current_volume)
        print(f"Switched to {current_volume} dataset")
        renderer.RemoveAllViewProps()
        renderer.AddActor(outline_actor)
        renderer.AddActor(iso_actor)
        renderer.AddActor2D(iso_value_text)
        slider_widget.SetInteractor(renderWindowInteractor)  # Ensure the interactor is set before enabling
        slider_widget.EnabledOn()  # Ensure the slider widget is enabled
        slider_widget.Render()
    renderWindow.Render()

renderWindowInteractor.AddObserver("KeyPressEvent", keypress_callback)

# Render and interact
renderWindow.SetSize(800, 800)
renderWindow.SetWindowName("Iso-surface and Volume Rendering")
renderWindow.Render()
renderWindowInteractor.Start()

