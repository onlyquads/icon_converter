import sys
import os
from PySide2.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog)
from PySide2.QtCore import Qt
from PIL import Image

class ImageToIcoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to ICO Converter")
        self.setGeometry(100, 100, 400, 300)

        # Initialize variables
        self.image_files = []
        self.destination_folder = ""
        self.source_image_folder = None
        
        # Set up UI elements
        self.label = QLabel(
            "Drag and drop images here to convert to .ico format"
            )
        self.label.setAlignment(Qt.AlignCenter)

        # Browse button for destination folder
        self.browse_button = QPushButton("Select Destination Folder")
        self.browse_button.clicked.connect(self.select_destination_folder)

        # Convert button to start conversion
        self.convert_button = QPushButton("Convert to ICO")
        self.convert_button.clicked.connect(self.convert_images_to_ico)
        # Disable until files are dropped
        self.convert_button.setEnabled(False)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.convert_button)
        self.setLayout(layout)

        # Enable drag-and-drop functionality
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.image_files.clear()  # Clear previous files
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
                    ):
                    self.image_files.append(file_path)
                    self.source_image_folder = os.path.dirname(file_path)
            self.label.setText(
                f"{len(self.image_files)} image(s) ready for conversion.")
            # Enable convert button when files are dropped
            self.convert_button.setEnabled(True)

    def select_destination_folder(self):
        source_folder = os.path.expanduser("~")
        if self.source_image_folder:
            source_folder = self.source_image_folder
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Destination Folder",
            source_folder
            )
        if folder:
            self.destination_folder = folder
            self.label.setText(
                f"Destination set to: {self.destination_folder}"
                )

    def convert_images_to_ico(self):
        if not self.destination_folder:
            self.label.setText("Please select a destination folder first.")
            return

        if not self.image_files:
            self.label.setText(
                "No images to convert. Please drag and drop files."
                )
            return

        # Convert each image file to ICO format with multiple sizes
        for file_path in self.image_files:
            self.convert_to_ico(file_path)

        self.label.setText("Conversion completed!")
        # Disable button after conversion
        self.convert_button.setEnabled(False)

    def convert_to_ico(self, file_path):
        try:
            img = Image.open(file_path)
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            ico_path = os.path.join(
                self.destination_folder, f"{base_name}.ico"
                )
            
            # Define the sizes commonly used for Windows icons
            sizes = [
                (16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
                ]

            # Resize the image to each of the sizes and save as an 
            # ICO file with multiple resolutions
            img.save(ico_path, format='ICO', sizes=sizes)
            print(f"Saved ICO file to: {ico_path}")
        except Exception as e:
            print(f"Failed to convert {file_path} to ICO: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageToIcoConverter()
    window.show()
    sys.exit(app.exec_())
