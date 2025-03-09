from classes.Feeds import Feeds

# Імпортуємо та тестуємо JSONFileImporter
json_importer = Feeds.JSONFileImporter('feeds.json')
imported_feeds = json_importer.import_feeds()

# Виводимо імпортовані записи
for feed in imported_feeds:
    print(feed)