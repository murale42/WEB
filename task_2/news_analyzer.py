import csv
import sys
import random
from datetime import datetime, timedelta
from collections import defaultdict
from statistics import mean

PURPLE = "\033[95m"
LIGHT_PURPLE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Генерация CSV
categories_list = ["Technology", "Economy", "Politics", "Health", "Sports",
                   "Culture", "Science", "World", "Business"]

titles_list = [
    "New AI Breakthrough",
    "Global Markets Rally",
    "Elections Bring Surprises",
    "Health Experts Warn of New Virus",
    "Sports Team Wins Championship",
    "Cultural Festival Draws Thousands",
    "Scientists Discover New Element",
    "World Leaders Meet for Summit",
    "Business Giants Merge in Historic Deal",
    "Tech Company Releases Innovative Gadget"
]

NUM_RECORDS = 104

def random_date():
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2025, 10, 1)
    delta = end_date - start_date
    return (start_date + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

def generate_csv(file_path):
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "title", "category", "views", "publication_date"])

        for i in range(1, NUM_RECORDS + 1):
            writer.writerow([
                i,
                random.choice(titles_list),
                random.choice(categories_list),
                random.randint(100, 50000),
                random_date()
            ])

    print(f"{LIGHT_PURPLE}Файл '{file_path}' был создан автоматически.{RESET}")


# Чтение и анализ
def read_csv(file_path):
    news_list = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["views"] = int(row["views"])
                news_list.append(row)
    except FileNotFoundError:
        print(f"{PURPLE}Файл не найден! Генерирую новый...{RESET}")
        generate_csv(file_path)
        return read_csv(file_path)

    return news_list

def analyze_news(news_list):
    total_news = len(news_list)
    most_viewed = max(news_list, key=lambda x: x["views"])
    avg_views = mean([n["views"] for n in news_list])

    categories = defaultdict(int)
    for n in news_list:
        categories[n["category"]] += 1
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

    return total_news, most_viewed, sorted_categories, avg_views

def print_report(total, top, categories, avg):
    print(f"\n{BOLD}{PURPLE} АНАЛИЗ ФАЙЛА С НОВОСТЯМИ{RESET}")
    print(f"{LIGHT_PURPLE}─────────────────────────────────────────────{RESET}")
    print(f"{BOLD}Общее количество новостей:{RESET} {total}")
    print(f"{BOLD}Самая популярная новость:{RESET} '{top['title']}' ({top['views']} просмотров)")
    print(f"{BOLD}Среднее количество просмотров:{RESET} {avg:.2f}\n")

    print(f"{BOLD}{PURPLE}Количество новостей по категориям:{RESET}")
    for cat, count in categories:
        print(f"  {LIGHT_PURPLE}{cat:<20}{RESET} — {count} новостей")
    print()

def main():
    if len(sys.argv) < 2:
        print(f"{PURPLE}Использование: python news_analyzer.py news_data.csv{RESET}")
        sys.exit(1)

    file_path = sys.argv[1]
    news_list = read_csv(file_path)
    total, top, categories, avg = analyze_news(news_list)
    print_report(total, top, categories, avg)

if __name__ == "__main__":
    main()
