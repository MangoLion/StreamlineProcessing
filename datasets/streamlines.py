import argparse
import vtk
import numpy as np
import csv
from vtkmodules.util import numpy_support
PATH = 'D:/Academic/VReconstruction/datasets/bernard3D.vtk'
def generate_streamlines(file_path, num_streamlines=10, step_size=0.1, max_propagation=100):
    # Read the source file.
    reader = vtk.vtkStructuredGridReader()
    reader.SetFileName(file_path)
    reader.Update()

    # Get the structured grid from the reader
    structuredGrid = reader.GetOutput()

    # Get the bounds of the vector field
    bounds = structuredGrid.GetBounds()

    # Generate random start positions within the bounds
    start_positions = np.random.uniform(low=[bounds[0], bounds[2], bounds[4]], 
                                        high=[bounds[1], bounds[3], bounds[5]], 
                                        size=(num_streamlines, 3))

    # Initialize a list to hold the streamlines
    streamlines = []

    # For each start position, create a vtkStreamTracer object and perform the stream tracing
    for start_position in start_positions:
        streamTracer = vtk.vtkStreamTracer()
        streamTracer.SetInputData(structuredGrid)
        streamTracer.SetStartPosition(*start_position)
        streamTracer.SetMaximumPropagation(max_propagation)
        streamTracer.SetIntegrationDirectionToBoth()
        streamTracer.SetComputeVorticity(True)
        streamTracer.SetIntegrationStepUnit(vtk.vtkStreamTracer.LENGTH_UNIT)
        streamTracer.SetInitialIntegrationStep(step_size)
        
        # Perform the stream tracing
        streamTracer.Update()

        # Get the output as a vtkPolyData object containing the streamline
        polyData = streamTracer.GetOutput()
        #print(polyData)
        # Convert the vtkPolyData to a numpy array and flatten it to a 1D array
        streamline = numpy_support.vtk_to_numpy(polyData.GetPoints().GetData()).flatten()

        # Add the streamline to the list of streamlines
        streamlines.append(streamline.tolist())

    # Return the list of streamlines
    return streamlines

# Call the function with your specific parameters
streamlines = generate_streamlines(PATH, num_streamlines=10, step_size=0.1, max_propagation=100)



if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate streamlines from a VTK structured grid.')
    parser.add_argument('--file_path', help='Path to the VTK file.')
    parser.add_argument('--output_path', help='Path to the output file.')
    parser.add_argument('--num_streamlines', type=int, help='Number of streamlines to generate.')
    parser.add_argument('--step_size', type=float, help='Step size for the stream tracer.')
    parser.add_argument('--max_propagation', type=float, help='Maximum propagation distance for the stream tracer.')
    args = parser.parse_args()

    # Read the VTK file content from stdin
    #file_content = sys.stdin.buffer.read()

    # Call the function with the arguments from the command line
    streamlines = generate_streamlines(args.file_path, args.num_streamlines, args.step_size, args.max_propagation)
    
    # Print the streamlines
    streamlines_data = []
    for i, streamline in enumerate(streamlines):
        #print(f"Streamline {i+1}: {streamline}")
        streamlines_data.append(streamline)

    with open(args.output_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(streamlines_data)

    print(f"Data has been written to {args.output_path}.")