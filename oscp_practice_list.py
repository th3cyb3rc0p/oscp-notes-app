# LainKusanagi OSCP Practice List
# Source: https://docs.google.com/spreadsheets/d/18weuz_Eeynr6sXFQ87Cd5F0slOj9Z6rt/edit?gid=487240997
# Curated by LainKusanagi. Use this to track progress through ~150+ machines across HTB, HackSmarter,
# Proving Grounds Practice, VulnLab, and the free OffSec-hosted VulnHub boxes.
#
# Each entry is keyed by machine name (lower-cased for matching). The display name preserves original
# casing. "os" is "linux" or "windows" or "any". "kind" is "standalone" or "ad" for Active Directory.
#
# The app seeds these into the `checklist` table on first launch. Each row gets a checkbox,
# a status dropdown (locked / started / user / root / owned / skipped), a notes field, and a button
# to "Open as Tracker machine" that creates a per-machine entry in the Tracker tab.

PLATFORMS = [
	("HackTheBox", [
		("Linux", "standalone", [
			"Sea", "Markup", "Nibbles", "Jerry", "Solidstate", "Netmon", "Poison", "Servmon",
			"Editor", "Chatterbox", "Sunday", "Jeeves", "Keeper", "Sniper", "Pilgrimage",
			"Querier", "Cozyhosting", "Giddy", "Codify", "Bounty", "Tartarsauce", "Artic",
			"Jarvis", "Remote", "Tabby", "Buff", "Connected", "Love", "Mentor", "Secnotes",
			"Devvortex", "Access", "Irked", "Mailing", "Popcorn", "Heist", "Bashed",
			"Certified", "Broker", "Puppy", "Silentium", "Timelapse", "Networked", "Signed",
			"UpDown", "Swagshop", "Nineveh", "Dante", "Pandora", "Zephyr", "OpenAdmin",
			"Precious", "Busqueda", "Epsilon", "Monitored", "Gobox", "BoardLight", "Bucket",
			"Magic", "Facts", "Help", "Editorial", "Builder", "Linkvortex", "UnderPass",
			"Dog", "Cctv",
		]),
		("Windows", "standalone", [
			"Active", "BankSmarter", "Slayer", "ShareThePain", "Ascension", "Sysco",
			"Talisman", "StellarComms", "Verbose", "MartiniAD", "Forest", "Sauna", "Flight",
			"Exception", "Samurai", "Blackfield", "TheFrizz", "PivotSmarter",
		]),
		("Active Directory and Networks", "ad", [
			"Active", "Forest", "Sauna", "Blackfield", "Querier", "TheFrizz", "Building Magic",
			"PivotSmarter", "Administrator", "Odyssey", "BitStream", "Monteverde", "ShadowGate",
			"Escape", "Welcome", "EscapeTwo", "Anomaly", "Arasaka", "Lumon Industries",
			"NovaCart", "404 bank", "AWS", "sns_secrets", "Static",
		]),
	]),
	("HackSmarter", [
		("Linux", "standalone", [
			"Slayer", "ShareThePain", "Ascension", "Sysco", "Talisman", "StellarComms",
			"Verbose", "MartiniAD", "Exception", "Samurai", "Blackfield", "TheFrizz",
			"Building Magic", "PivotSmarter",
		]),
		("Windows", "standalone", [
			"BankSmarter", "Slayer", "Ascension", "Talisman", "StellarComms", "MartiniAD",
			"Samurai", "Blackfield", "TheFrizz", "Building Magic", "PivotSmarter",
		]),
		("Active Directory and Networks", "ad", [
			"Slayer", "ShareThePain", "Talisman", "StellarComms", "MartiniAD", "Samurai",
			"Blackfield", "TheFrizz", "Building Magic", "PivotSmarter",
		]),
	]),
	("Proving Grounds Practice", [
		("Linux", "standalone", [
			"ClamAV", "Pelican", "Payday", "Snookums", "Bratarina", "Pebbles", "Nibbles",
			"Hetemit", "ZenPhoto", "Nukem", "Cockpit", "Clue", "Extplorer", "Postfish",
			"Hawat", "Walla", "PC", "Apex", "Sorcerer", "Sybaris",
		]),
		("Windows", "standalone", [
			"Kevin", "Internal", "Algernon", "Jacko", "Craft", "Squid", "Nickel", "MedJed",
			"Billyboss", "Shenzi", "AuthBy", "Slort", "DVR4", "Mice", "Monster", "Fish",
		]),
		("Active Directory and Networks", "ad", [
			"Access", "Nagoya", "Hokkaido", "Vault", "Bamboo", "Trusted", "Hutch", "Hybrid",
			"Resourced", "Lustrous", "Heron", "Pathway",
		]),
	]),
	("VulnLab / Hackthebox", [
		("Linux", "standalone", [
			"Sync", "Data", "Build", "Forgotten", "Sendai", "SkillForge", "Reflection",
			"Resourced", "Lustrous", "Hybrid",
		]),
		("Windows", "standalone", [
			"Escape", "Job", "Job2", "Lock", "Sweep", "Baby", "Baby2", "Breach",
		]),
		("Active Directory and Networks", "ad", [
			"Baby", "Baby2", "Breach", "Sweep", "Lock", "Forgotten", "Sendai",
		]),
	]),
	("Proving Grounds Play", [
		("Standalone", "standalone", ["Sorcerer", "Sybaris"]),
	]),
	("OffSec VulnHub (free)", [
		("Linux", "standalone", [
			"Peppo", "Hunit", "Readys", "Astronaut", "Bullybox", "Marketing", "Exfiltrated",
			"Fanatastic", "QuackerJack", "Wombo", "Flu", "Roquefort", "Levram", "Mzeeav",
			"LaVita", "Xposedapi", "Zipper", "Workaholic", "Fired", "Scrutiny", "SPX",
			"Vmdak", "Mantis", "BitForge", "WallpaperHub", "Zab",
		]),
		("Windows", "standalone", [
			"Amaterasu", "Sams", "Loly", "Potato", "Stapler", "BBScute", "Gaara", "Blogger",
			"FunboxEasyEnum", "GlasgowSmile",
		]),
	]),
]


def flat_machines():
	"""Yield (platform, os, kind, name_lower, name_display)."""
	for platform, groups in PLATFORMS:
		for os_name, kind, names in groups:
			for n in names:
				yield platform, os_name, kind, n.lower(), n


def total_count() -> int:
	return sum(len(names) for _, groups in PLATFORMS for _, _, names in groups)
