"""
XML Parser - Chely Kelvin Sheja

Reads the XML file and converts it to Python dictionaries.
Using ElementTree because it's built into Python.
"""

import xml.etree.ElementTree as ET
import json
import os


def parse_xml_to_json(xml_file_path):
    """
    Parse the XML file and return a list of transaction dicts
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        transactions = []
        
        # Iterate through each transaction element
        for transaction_elem in root.findall('transaction'):
            # Extract the id attribute
            transaction_id = transaction_elem.get('id')
            
            # Build dictionary from child elements
            transaction = {
                'id': int(transaction_id) if transaction_id else None,
                'type': transaction_elem.find('type').text if transaction_elem.find('type') is not None else '',
                'amount': float(transaction_elem.find('amount').text) if transaction_elem.find('amount') is not None else 0.0,
                'sender': transaction_elem.find('sender').text if transaction_elem.find('sender') is not None else '',
                'receiver': transaction_elem.find('receiver').text if transaction_elem.find('receiver') is not None else '',
                'timestamp': transaction_elem.find('timestamp').text if transaction_elem.find('timestamp') is not None else '',
                'status': transaction_elem.find('status').text if transaction_elem.find('status') is not None else 'pending'
            }
            
            transactions.append(transaction)
        
        return transactions
    
    except FileNotFoundError:
        print(f"Error: File '{xml_file_path}' not found.")
        return []
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def create_transaction_dictionary(transactions_list):
    """
    Convert list of transactions to dictionary with id as key for fast lookup.
    
    Args:
        transactions_list (list): List of transaction dictionaries
        
    Returns:
        dict: Dictionary with transaction id as key
    """
    return {transaction['id']: transaction for transaction in transactions_list}


def save_json_file(data, output_path):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save (list or dict)
        output_path (str): Path to output JSON file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"JSON file saved to: {output_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Get the path to the XML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    xml_path = os.path.join(os.path.dirname(current_dir), 'data', 'modified_sms_v2.xml')
    
    print("=" * 60)
    print("XML to JSON Parser - Testing")
    print("=" * 60)
    
    # Parse XML to list of dictionaries
    transactions = parse_xml_to_json(xml_path)
    
    print(f"\nTotal transactions parsed: {len(transactions)}")
    
    # Display first 3 transactions as example
    if transactions:
        print("\nFirst 3 transactions:")
        print(json.dumps(transactions[:3], indent=2))
        
        # Create dictionary version for fast lookup
        transaction_dict = create_transaction_dictionary(transactions)
        print(f"\nDictionary created with {len(transaction_dict)} entries")
        
        # Test dictionary lookup
        test_id = 5
        if test_id in transaction_dict:
            print(f"\nLookup test - Transaction ID {test_id}:")
            print(json.dumps(transaction_dict[test_id], indent=2))
        
        # Optionally save to JSON file
        output_path = os.path.join(os.path.dirname(current_dir), 'data', 'transactions.json')
        save_json_file(transactions, output_path)
    
    print("\n" + "=" * 60)
