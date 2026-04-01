from celery import shared_task
from django.utils import timezone
from django.db import transaction
from datetime import timedelta


@shared_task
def process_book_rental(user_id, book_id):
    """
    Process book rental asynchronously.
    - Creates Borrowed record
    - Decrements book quantity
    - Returns status for logging/monitoring
    """
    from circulation.models import Borrowed
    from catalog.models import Catalog
    from users.models import User
    
    try:
        user = User.objects.get(id=user_id)
        
        with transaction.atomic():
            book = Catalog.objects.select_for_update().get(id=book_id)
            
            # Check if book is available
            if book.quantity <= 0:
                return {
                    "status": "error",
                    "message": f"Book '{book.title}' is out of stock",
                    "book_id": book_id
                }
            
            # Create rental record
            borrowed = Borrowed.objects.create(
                magician=user,
                book=book,
                due_date=timezone.now() + timedelta(days=25)
            )
            
            # Update book quantity
            book.quantity -= 1
            book.save()
        
        return {
            "status": "success",
            "message": f"Book '{book.title}' rented successfully",
            "book_id": book_id,
            "borrowed_id": borrowed.id,
            "due_date": borrowed.due_date.isoformat()
        }
    
    except Catalog.DoesNotExist:
        return {
            "status": "error",
            "message": f"Book {book_id} not found",
            "book_id": book_id
        }
    except User.DoesNotExist:
        return {
            "status": "error",
            "message": f"User {user_id} not found",
            "user_id": user_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Rental processing failed: {str(e)}",
            "book_id": book_id,
            "user_id": user_id
        }


@shared_task
def process_book_return(borrowed_id):
    """
    Process book return asynchronously.
    - Updates Borrowed return_date
    - Increments book quantity
    - Returns status for logging/monitoring
    """
    from circulation.models import Borrowed
    
    try:
        with transaction.atomic():
            borrowed = Borrowed.objects.select_for_update().get(id=borrowed_id)
            
            # Mark as returned
            borrowed.return_date = timezone.now()
            borrowed.save()
            
            # Increment book quantity
            borrowed.book.quantity += 1
            borrowed.book.save()
        
        return {
            "status": "success",
            "message": f"Book '{borrowed.book.title}' returned successfully",
            "borrowed_id": borrowed_id,
            "book_id": borrowed.book.id,
            "return_date": borrowed.return_date.isoformat()
        }
    
    except Borrowed.DoesNotExist:
        return {
            "status": "error",
            "message": f"Rental record {borrowed_id} not found",
            "borrowed_id": borrowed_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Return processing failed: {str(e)}",
            "borrowed_id": borrowed_id
        }
