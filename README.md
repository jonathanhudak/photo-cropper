# PhotoCropper

PhotoCropper is an application that automatically generates optimal crops for images using saliency detection and composition rules.

## Setup Instructions

Follow these steps to set up the PhotoCropper virtual environment and run the application.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- virtualenv

### Setting up the Virtual Environment

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/PhotoCropper.git
   cd PhotoCropper
   ```

2. Create a virtual environment:

   ```
   python3 -m venv photocroppervenv
   ```

3. Activate the virtual environment:

   - On macOS and Linux:
     ```
     source photocroppervenv/bin/activate
     ```
   - On Windows:
     ```
     photocroppervenv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Installing OpenCV

PhotoCropper uses OpenCV for image processing. To install OpenCV:

1. Ensure you're in the activated virtual environment.

2. Install OpenCV:

   ```
   pip install opencv-python
   ```

3. If you need additional OpenCV modules, you can install them with:
   ```
   pip install opencv-contrib-python
   ```

### Running the Application

1. Ensure you're in the activated virtual environment.

2. Run the main script:
   ```
   python main.py
   ```

### Deactivating the Virtual Environment

When you're done using PhotoCropper, you can deactivate the virtual environment:

```
deactivate
```

## Troubleshooting

If you encounter any issues with OpenCV or other dependencies, ensure that:

- You're using the correct Python version
- Your virtual environment is activated
- All required packages are installed correctly

For OpenCV-specific issues, you might need to install additional system libraries. Refer to the OpenCV documentation for your operating system.

## Contributing

[Include instructions for how others can contribute to your project]

## License

[Include your license information here]
