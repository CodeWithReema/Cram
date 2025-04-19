# Cram

Cram is a Django-based study platform designed for students to enhance their learning through AI-generated resources. With free account registration, students can upload study material and receive personalized flashcards, quizzes, and other memory tools powered by the GeminiAI API.

## Features

- Free student account registration
- AI-generated flashcards, tests, and study aids
- Integration with GeminiAI for intelligent content processing
- Profiles for each user
- Browse and share public study materials
- Uses memory retention techniques based on popular learning methods

## Getting Started

Follow these instructions to get the Cram application running on your local machine.

### Prerequisites

- Python 3.8+
- Git (optional, for cloning the repo)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/cram.git
   cd cram
   ```

2. **Create and activate a virtual environment**

   - **Mac/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

6. **Open in browser**
   Visit `http://127.0.0.1:8000/` in your web browser.

## Contributing

We welcome contributions! Fork the project and submit a pull request, or open an issue for suggestions and bug reports.

## License

This project is licensed under the MIT License.

