from aiogram import Bot, Dispatcher, F
from database.requiests import set_star, get_reviews


async def reviews(user_id: int):
    reviews = await set_star(user_id)
    
    total_reviews = len(reviews)
    if total_reviews == 0:
        return "No reviews", 0.0, "No rating"  # Return "No reviews" and 0.0 as average rating if there are no reviews available
    
    # Define a mapping from star emojis to numeric values
    STAR_MAPPING = {
        '⭐️': 1,
        '⭐️⭐️': 2,
        '⭐️⭐️⭐️': 3,
        '⭐️⭐️⭐️⭐️': 4,
        '⭐️⭐️⭐️⭐️⭐️': 5
    }
    
    # Calculate the total rating by converting star emojis to numeric values
    total_rating = sum(STAR_MAPPING.get(review.stars, 0) for review in reviews)
    average_rating = total_rating / total_reviews
    
    # Determine the number of full stars
    full_stars = int(average_rating)
    
    # Determine if there is a half star
    half_star = (average_rating - full_stars) >= 0.5
    
    # Construct the representation with stars and a half star if applicable
    rating_representation = '⭐️' * full_stars + ('⭐️' if half_star else '')
    
    return total_reviews, average_rating, rating_representation






