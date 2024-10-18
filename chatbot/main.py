import os
from .chatbot import ChatBot
from .openai_wrapper import create_openai_client
from .data.data_processor import import_product_data
from .data.product_catalog import get_all_products

def run_chatbot():
    # Define the paths to your data files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lamps_file_path = os.path.join(current_dir, '..', 'data', 'lamps.json')
    curtains_file_path = os.path.join(current_dir, '..', 'data', 'curtains.xlsx')
    ikea_curtains_file_path = os.path.join(current_dir, '..', 'data', 'IKEA curtain drivers.xlsx')

    # Import product data
    import_product_data(lamps_file_path, 'lamp')
    import_product_data(curtains_file_path, 'curtain')
    
    if os.path.exists(ikea_curtains_file_path):
        import_product_data(ikea_curtains_file_path, 'curtain_driver')
    else:
        print(f"Warning: IKEA Curtain driver file not found at {ikea_curtains_file_path}")

    # After importing data
    all_products = get_all_products()
    print(f"Imported a total of {len(all_products)} products into the database.")

    client = create_openai_client()
    chatbot = ChatBot(client)
    print("Welcome to our home decor chatbot! How can I assist you today?")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = chatbot.get_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    run_chatbot()
