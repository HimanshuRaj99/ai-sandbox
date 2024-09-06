import logging

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO)

def select_age(grade):
    """
    Retrieve the age of a student based on their grade level.

    Args:
        grade (int): The grade level of the student.

    Returns:
        str: The age corresponding to the specified grade level, or a message if the grade is not found.
    """
    # Mapped the age of the student according to their grade level.
    logging.info(f'Retrieving age for Grade {grade}')
    
    # Dictionary mapping grades to ages
    age = {
        3: '8 years',
        4: '9 years',
        5: '10 years'
    }

    try:
        # Get the value corresponding to the specified grade level
        selected_age = age[grade]
        logging.info(f'Age retrieved: {selected_age}')
    except KeyError:
        # Handle the case where the grade is not found in the dictionary
        selected_age = f'Grade {grade} is not recognized. Please provide a valid grade (3, 4, or 5).'
        logging.error(selected_age)
    
    return selected_age
