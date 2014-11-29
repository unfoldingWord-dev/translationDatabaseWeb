Seed Data
=========

    import bs4
    import csv
    import requests

    from .models import *

    data = requests.get("https://dir.yahoo.com/society_and_culture/religion_and_spirituality/faiths_and_practices/christianity/denominations_and_sects/")
    soup = bs4.BeautifulSoup(data.content)
    soup.select("div.cat li > a > b")
    for d in rows:
        Denomination.objects.create(name=d.text)


    bible_content = [
        "Full Bible",
        "Full NT",
        "Genesis",
        "Exodus",
        "Leviticus",
        "Numbers",
        "Deuteronomy",
        "Joshua",
        "Judges",
        "Ruth",
        "1 Samuel",
        "2 Samuel",
        "1 Kings",
        "2 Kings",
        "1 Chronicles",
        "2 Chronicles",
        "Ezra",
        "Nehemiah",
        "Esther",
        "Job",
        "Psalms",
        "Proverbs",
        "Ecclesiastes",
        "Solomon",
        "Isaiah",
        "Jeremiah",
        "Lamentations",
        "Ezekiel",
        "Daniel",
        "Hosea",
        "Joel",
        "Amos",
        "Obadiah",
        "Jonah",
        "Micah",
        "Nahum",
        "Habakkuk",
        "Zephaniah",
        "Haggai",
        "Zechariah",
        "Malachi",
        "Matthew",
        "Mark",
        "Luke",
        "John",
        "Acts",
        "Romans",
        "1 Corinthians",
        "2 Corinthians",
        "Galatians",
        "Ephesians",
        "Philippians",
        "Colossians",
        "1 Thessalonians",
        "2 Thessalonians",
        "1 Timothy",
        "2 Timothy",
        "Titus",
        "Philemon",
        "Hebrews",
        "James",
        "1 Peter",
        "2 Peter",
        "1 John",
        "2 John",
        "3 John",
        "Jude",
        "Revelation"
    ]

    for b in bible_content:
        BibleContent.objects.create(name=b)


    for c in EthnologueCountryCode.objects.all():
        Country.objects.create(country=c)


    reader = csv.reader(open("../population.csv", "rb"))
    for row in reader:
        try:
            country = Country.objects.get(country__name__iexact=row[0])
            country.population = int(row[1].replace(" ", ""))
            country.save()
        except Country.DoesNotExist:
            print "Could not find:", row
