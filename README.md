# Llama OCR - Image Text Extraction App

<a href="https://groq.com" target="_blank" rel="noopener noreferrer">
  <img
    src="https://groq.com/wp-content/uploads/2024/03/PBG-mark1-color.svg"
    alt="Powered by Groq for fast inference."
  />
</a>



A Chainlit-based web application that uses Groq's Llama Vision model to extract and analyze text from images. The app provides a user-friendly interface for uploading images and getting structured text output.

## Features

- 📷 Image upload support (JPEG, PNG, JPG)
- 👀 Image preview functionality
- 📝 Text extraction using Groq's Llama Vision model
- 🔍 Structured Markdown output
- 🚀 Real-time processing status updates
- ⚡ Simple and intuitive user interface

## Prerequisites

Before running the application, make sure you have:

- Python 3.8 or higher installed
- A Groq API key (get it from [Groq's platform](https://console.groq.com))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/QsingularityAi/CustomLLamaOCR.git
cd CustomLLamaOCR
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
chainlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8000`

3. Use the application:
   - Click "Upload Image" to select and upload an image
   - Review the preview of your uploaded image
   - Click "Extract Text" to process the image
   - View the extracted text in structured Markdown format

## Project Structure

```
llama-ocr/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # Project documentation
```

## Requirements

Create a `requirements.txt` file with the following dependencies:

```
chainlit
groq
Pillow
python-dotenv
```

## Environment Variables

The application requires the following environment variables:

- `GROQ_API_KEY`: Your Groq API key for accessing the Llama Vision model

## Features in Detail

### Image Upload
- Supports JPEG, PNG, and JPG formats
- Maximum file size: 5MB
- Displays preview of uploaded image

### Text Extraction
- Uses Groq's Llama-3.2-90b-vision-preview model
- Processes image content and extracts readable text
- Outputs structured text in Markdown format
- Provides real-time status updates during processing

### User Interface
- Clean and intuitive interface
- Clear success/error messages
- Progress indicators for processing status
- Action buttons for upload and extraction

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File size limitations
- API connection issues
- Processing errors

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Acknowledgments

- [Chainlit](https://github.com/chainlit/chainlit) for the chat interface
- [Groq](https://groq.com) for the Llama Vision model
- All contributors and users of this project

## Support

For support, please:
1. Check the existing issues or create a new one
2. Contact the project maintainers
3. Read the [Chainlit documentation](https://docs.chainlit.io)
