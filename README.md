# Home Decor AI Chatbot

An intelligent conversational AI chatbot designed for a high-end home decor store, specializing in lamps, curtains, and curtain drivers.

## Features

- Natural language processing powered by OpenAI's GPT model
- Dynamic product catalog with SQLite database integration
- Flexible data import system supporting JSON and Excel formats
- Intelligent product search and recommendation system
- Fallback mechanisms for handling API failures gracefully

## Technology Stack

- Python 3.x
- SQLite
- OpenAI API
- pandas (for data processing)
- requests (for API communication)

## Project Structure
Lumi-chatbot/
│
├── chatbot/
│ ├── data/
│ │ ├── init.py
│ │ ├── data_processor.py
│ │ └── product_catalog.py
│ ├── init.py
│ ├── chatbot.py
│ ├── main.py
│ └── openai_wrapper.py
│
├── data/
│ ├── lamps.json
│ ├── curtains.xlsx
│ └── IKEA curtain drivers.xlsx
│
├── venv/
├── .gitignore
├── README.md
└── requirements.txt

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/home-decor-chatbot.git
   cd home-decor-chatbot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

5. Prepare your product data:
   - Place your product data files in the `data/` directory
   - Ensure the file names match those in `chatbot/main.py`

## Running the Chatbot

To start the chatbot, run:

Follow the prompts to interact with the chatbot.

## Customization

- To add new product categories, update the `import_product_data` function in `chatbot/main.py`
- Modify the chatbot's personality and knowledge base in `chatbot/openai_wrapper.py`
- Extend the `ChatBot` class in `chatbot/chatbot.py` to add new features or commands

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

