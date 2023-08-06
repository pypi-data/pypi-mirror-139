import novauniverse as nova

"""
player = nova.Player("THEGOLDENPRO")

print(player.is_online)
"""

license = nova.License(key=nova.KEYS.TOURNAMENT_DEMO_KEY)

print(license.owner)