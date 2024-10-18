from .data.product_catalog import get_product_by_id, get_all_products, search_products, get_products_by_category
from .openai_wrapper import get_chatbot_response
import random

class ChatBot:
    def __init__(self, client):
        self.client = client

    def get_response(self, user_input):
        user_input_lower = user_input.lower()

        if user_input_lower.startswith("search "):
            return self.search_products(user_input[7:])
        elif user_input_lower.startswith("info "):
            return self.get_product_info(user_input[5:].strip().upper())
        elif "list all" in user_input_lower or "show all" in user_input_lower:
            if "drivers" in user_input_lower or "curtain drivers" in user_input_lower:
                return self.list_curtain_drivers()
            else:
                return self.list_all_products()
        else:
            response = get_chatbot_response(self.client, user_input)
            if "I apologize, but I'm having trouble accessing my knowledge base" in response:
                return self.fallback_response(user_input)
            return response

    def fallback_response(self, user_input):
        if "product" in user_input.lower() and "sell" in user_input.lower():
            return self.get_product_overview()
        elif "list" in user_input.lower() or "show" in user_input.lower():
            if "curtain" in user_input.lower() and "driver" in user_input.lower():
                return self.list_curtain_drivers()
            elif "curtain" in user_input.lower():
                return self.list_products("curtain", 5)
            elif "lamp" in user_input.lower():
                return self.list_products("lamp", 5)
            else:
                return self.list_random_products(5)
        else:
            return "I apologize, I couldn't understand your request. Could you please ask about our products, or use commands like 'search', 'info', or 'list all' followed by a product category?"

    def get_product_overview(self):
        all_products = get_all_products()
        lamp_count = len([p for p in all_products if p['id'].startswith('LAMP')])
        curtain_count = len([p for p in all_products if p['id'].startswith('CURTAIN')])
        driver_count = len([p for p in all_products if p['id'].startswith('DRIVER')])
        
        return f"We offer a wide range of home decor products. Currently, we have {lamp_count} different lamps, {curtain_count} types of curtains, and {driver_count} curtain drivers. Would you like more information about any specific category?"

    def list_products(self, category, limit=5):
        products = get_products_by_category(category)
        if products:
            response = f"Here are some of our {category} products:\n\n"
            for product in products[:limit]:
                response += f"• {product['name']} - ${product['price']:.2f}\n"
            response += f"\nWould you like more information about any of these {category}s?"
        else:
            response = f"I'm sorry, I couldn't find any {category} products. Would you like to see products from a different category?"
        return response

    def list_random_products(self, limit=5):
        all_products = get_all_products()
        if all_products:
            sample = random.sample(all_products, min(limit, len(all_products)))
            response = "Here's a random selection of our products:\n\n"
            for product in sample:
                category = 'Lamp' if product['id'].startswith('LAMP') else 'Curtain' if product['id'].startswith('CURTAIN') else 'Curtain Driver'
                response += f"• {product['name']} - ${product['price']:.2f} ({category})\n"
            response += "\nWould you like more information about any of these products or a specific category?"
        else:
            response = "I'm sorry, it seems we don't have any products available at the moment. Please check back later."
        return response

    def search_products(self, query):
        products = search_products(query)
        if products:
            response = f"Here are some products matching '{query}':\n\n"
            for product in products[:5]:  # Limit to 5 results
                response += f"• {product['name']} - ${product['price']:.2f}\n"
            response += "\nWould you like more information about any of these products?"
        else:
            response = f"I'm sorry, I couldn't find any products matching '{query}'. Can I help you find something else?"
        return response

    def get_product_info(self, product_id):
        product = get_product_by_id(product_id)
        if product:
            category = product['categories'][0].capitalize()
            response = f"Here's information about {product['name']} ({category}):\n\n"
            response += f"Price: ${product['price']:.2f}\n"
            response += f"Description: {product['description']}\n\n"
            response += f"Would you like to know more about this {category.lower()} or see similar products?"
        else:
            response = "I'm sorry, I couldn't find a product with that ID. Could you please check the ID and try again?"
        return response

    def list_all_products(self):
        products = get_all_products()
        if products:
            response = "Here's a list of all our available products:\n\n"
            for product in products:
                category = product['categories'][0].capitalize() if product['categories'] else 'Uncategorized'
                response += f"• {product['name']} - ${product['price']:.2f} ({category})\n"
            response += "\nThat's quite a selection! Is there any particular category or price range you're interested in?"
        else:
            response = "I'm sorry, it seems we don't have any products in stock at the moment. Please check back later or ask me about our upcoming inventory!"
        return response

    def list_curtain_drivers(self):
        drivers = get_products_by_category("DRIVER")
        if drivers:
            response = "Here are our available curtain drivers:\n\n"
            for driver in drivers[:5]:  # Limit to 5 results
                response += f"• {driver['name']} - ${driver['price']:.2f}\n"
            response += "\nWould you like more information about any specific driver?"
        else:
            response = "I'm sorry, we don't have any curtain drivers in stock at the moment."
        return response
