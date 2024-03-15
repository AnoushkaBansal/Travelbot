# TravelBot

TravelBot is a conversational agent designed to assist users in planning their travel by providing information on accommodations, local transport, points of interest, and general travel queries. Built with Flask, MySQL, BERT for intent recognition, and OpenAI for generating SQL queries and handling general inquiries, TravelBot aims to simplify travel planning with AI-powered insights.

## Features

- **Accommodation Information**: Find hotels and accommodations based on location, amenities, and price range.
- **Local Transport Options**: Get details on subway lines, buses, taxis, and bike rental services.
- **Points of Interest**: Discover landmarks, parks, museums, and other attractions.
- **General Travel Inquiries**: Ask any travel-related questions outside the database's scope, handled by OpenAI's GPT model.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- MySQL
- Flask
- OpenAI API key

### Installation

1. Clone the repository:
2. Navigate to the project directory:
3. Install the required Python packages:
4. Create a `.env` file in the root directory and add your OpenAI API key:
5. Set up your MySQL database and update the database configuration in `app.py` or through environment variables.
6. The BERT model requires training with specific data to generate label encoders and tensors suitable for intent classification. Due to GitHub's file size limitations, the fully trained model file, which is approximately 6GB, cannot be uploaded directly to the repository. Instructions for training the model are provided in the documentation. The code is present in train_model to achieve the same.

### Running the Application

1. Start the Flask server:
2. Open your web browser and navigate to `http://127.0.0.1:5000/` to interact with TravelBot.

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [MySQL](https://www.mysql.com/) - Database
- [BERT](https://huggingface.co/transformers/model_doc/bert.html) - Intent recognition
- [OpenAI](https://openai.com/) - SQL query generation and handling general inquiries

## Authors

- **Anoushka Bansal** - *Initial work* - [AnoushkaBansal](https://github.com/AnoushkaBansal)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc

