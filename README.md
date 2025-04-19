# Shopology

Shopology is an online marketplace and eCommerce platform similar to Amazon or eBay. Users can create a free account, build a personal dashboard, list items for sale, purchase goods, and interact with other users in a social and commercial environment.

## Features

- User registration and authentication
- Personalized user dashboard
- Item listing and browsing
- Secure buying and selling
- User-to-user messaging
- Search and filtering options

## Getting Started

Follow these steps to get Shopology running locally on your machine.

### Prerequisites

- Python 3.8+
- Git (optional, for cloning the repo)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/shopology.git
   cd shopology
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

## Project Structure

```
shopology/
├── accounts/           # User authentication and profiles
├── marketplace/        # Buying, selling, item listings
├── messages/           # User messaging system
├── templates/          # HTML templates
├── static/             # CSS, JavaScript, images
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Contributing

Feel free to fork the repository and submit pull requests. Issues and feature requests are welcome!

## License

This project is licensed under the MIT License.

---

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

