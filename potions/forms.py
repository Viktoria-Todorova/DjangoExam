from django import forms

from users.models import User


class CreatePotionForm(forms.Form):
    HERB_CHOICES = [
        ("mint", "Mint"),
        ("lavender", "Lavender"),
        ("mushroom", "Glow Mushroom"),
        ("nettle", "Nettle"),
        ("sage", "Silver Sage"),
        ("chamomile", "Golden Chamomile"),
        ("aloe", "Aloe Vera"),
        ("nightshade", "Nightshade"),
        ("sunflower", "Sunfire Petal"),
        ("lotus", "Blue Lotus"),
        ("ginger_root", "Fire Ginger Root"),
        ("blue_orchid", "Blue Orchid"),
        ("thorn_leaf", "Thorn Leaf"),
        ("moonflower", "Moonflower"),
        ("black_rose", "Black Rose"),
        ("ghost_mushroom", "Ghost Mushroom"),
        ("mandrake", "Mandrake Root"),
        ("void_root", "Void Root"),
        ("blood_lily", "Blood Lily"),
    ]

    LIQUID_CHOICES = [
        ("water", "Spring Water"),
        ("milk", "Moon Milk"),
        ("honey", "Honey Syrup"),
        ("ink", "Octopus Ink"),
        ("oil", "Herbal Oil"),
        ("alcohol", "Dwarven Alcohol"),
        ("blood", "Beast Blood"),
        ("ice_water", "Glacial Water"),
        ("fire_water", "Fire Water"),
        ("dew", "Morning Dew"),
        ("fog", "Captured Fog"),
        ("holy_water", "Holy Water"),
        ("elixir", "Ancient Elixir"),
        ("tar", "Black Tar"),
        ("lava", "Liquid Lava"),
        ("mercury", "Mercury"),
        ("liquid_light", "Liquid Light"),
    ]

    ITEM_CHOICES = [
        ("feather", "Phoenix Feather"),
        ("scale", "Dragon Scale"),
        ("bone", "Fairy Bone"),
        ("stone", "Moon Stone"),
        ("crystal", "Magic Crystal"),
        ("pearl", "Pearl"),
        ("dust", "Fairy Dust"),
        ("shadow_dust", "Shadow Dust"),
        ("gold_flake", "Gold Flake"),
        ("ash", "Sacred Ash"),
        ("butterfly_wing", "Butterfly Wing"),
        ("iron", "Iron Shard"),
        ("silver", "Silver Fragment"),
        ("spider_silk", "Spider Silk"),
        ("stardust", "Stardust"),
        ("crow_feather", "Crow Feather"),
        ("spirit_essence", "Spirit Essence"),
        ("opal", "Opal Gem"),
        ("ancient_coin", "Ancient Coin"),
        ("obsidian", "Obsidian"),
        ("heart_fragment", "Heart Fragment"),
        ("ruby", "Ruby"),
        ("clock_gear", "Clock Gear"),
        ("halo_fragment", "Halo Fragment"),
    ]
    magician = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter Username..."}),
    )
    herb = forms.ChoiceField(choices=HERB_CHOICES)
    liquid = forms.ChoiceField(choices=LIQUID_CHOICES)
    item = forms.ChoiceField(choices=ITEM_CHOICES)

    def clean_magician(self):
        username = self.cleaned_data["magician"]

        try:
            magician = User.objects.get(username=username)
            return magician
        except User.DoesNotExist:
            raise forms.ValidationError('No magician with this username exists!')

