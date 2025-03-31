# Llama Chat Application

A modern chat application built with React and Flask that uses the Mistral-7B-Instruct-v0.2 model through the Together API for generating responses.

## Features

- Real-time chat interface
- Integration with Mistral-7B-Instruct-v0.2 model
- Modern React frontend with styled components
- Flask backend with REST API
- Message formatting and styling

## Project Structure

```
.
├── frontend/           # React frontend application
│   ├── src/           # Source files
│   ├── public/        # Public assets
│   └── package.json   # Dependencies
├── backend/           # Flask backend application
│   ├── app.py        # Main application file
│   └── requirements.txt # Python dependencies
└── README.md         # This file
```

## Setup

1. Clone the repository
2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the backend directory
   - Add your Together API key: `TOGETHER_API_KEY=your_api_key_here`

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python app.py
   ```
2. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```
3. Open http://localhost:3000 in your browser

## API Endpoints

- `POST /api/chat`: Send a message to the chatbot
- `GET /api/health`: Check API health status

## Technologies Used

- Frontend:
  - React
  - JavaScript
  - CSS
  - HTML
- Backend:
  - Python
  - Flask
  - Together API
  - Mistral-7B-Instruct-v0.2 model

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 