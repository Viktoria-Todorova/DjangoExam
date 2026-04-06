from celery import shared_task
from django.core.cache import cache




# Calculate and cache user profile statistics asynchronously.
@shared_task
def aggregate_profile_stats(user_id):

    from users.models import User
    from circulation.models import Borrowed
    from potions.models import Potion
    from potions.choices import POTION_RECIPES
    from dragons.models import Dragon
    
    try:
        user = User.objects.get(id=user_id)
        
        borrowed = Borrowed.objects.filter(magician=user)
        
        #count rentals
        currently_rented_count = borrowed.filter(return_date__isnull=True).count()
        returned_books_count = borrowed.filter(return_date__isnull=False).count()
        
        #count potions
        potions_qs = Potion.objects.filter(magician=user)
        discovered_count = potions_qs.values('name').distinct().count()
        total_recipes = len(set(POTION_RECIPES.values()))
        
        #get dragon
        dragon = Dragon.objects.filter(rider=user).first()
        
        stats = {
            'currently_rented_count': currently_rented_count,
            'returned_books_count': returned_books_count,
            'potions_discovered': discovered_count,
            'potions_total': total_recipes,
            'potions_remaining': max(0, total_recipes - discovered_count),
            'dragon_id': dragon.id if dragon else None,
            'dragon_name': dragon.name if dragon else None,
        }
        
        #cache for 1 hour
        cache.set(f'profile_stats_{user_id}', stats, 3600)
        
        return {"status": "success", "message": "Profile stats cached", "user_id": user_id}
    
    except User.DoesNotExist:
        return {"status": "error", "message": f"User {user_id} not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}