from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Librarian group: full CRUD on all main models
    librarian, _ = Group.objects.get_or_create(name='Librarian')

    librarian_codenames = [
        # Catalog (books)
        'add_catalog', 'change_catalog', 'delete_catalog', 'view_catalog',
        # Grimoire
        'add_grimoire', 'change_grimoire', 'delete_grimoire', 'view_grimoire',
        # Circulation (borrowing)
        'add_borrowed', 'change_borrowed', 'delete_borrowed', 'view_borrowed',
        # Dragons
        'add_dragon', 'change_dragon', 'delete_dragon', 'view_dragon',
        # Potions
        'add_potion', 'change_potion', 'delete_potion', 'view_potion',
        # Users
        'view_user',
    ]

    librarian_perms = Permission.objects.filter(codename__in=librarian_codenames)
    librarian.permissions.set(librarian_perms)

    # Visitor group: read-only on all main models
    visitor, _ = Group.objects.get_or_create(name='Visitor')

    visitor_codenames = [
        'view_catalog',
        'view_grimoire',
        'view_borrowed',
        'view_dragon',
        'view_potion',
    ]

    visitor_perms = Permission.objects.filter(codename__in=visitor_codenames)
    visitor.permissions.set(visitor_perms)


def delete_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Librarian', 'Visitor']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email_alter_user_phone_number'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_code=delete_groups),
    ]
