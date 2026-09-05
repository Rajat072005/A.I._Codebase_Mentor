import json
import random
from collections import Counter

def load_dataset():

    with open(
        "datasets/raw/intent_dataset.json",
        "r",
        encoding="utf-8"
    ) as file:

        dataset = json.load(file)

    return dataset

def dataset_size(dataset):

    return len(dataset)

def intent_distribution(dataset):

    intents = []

    for example in dataset:

        intents.append(
            example["intent"]
        )

    distribution = Counter(intents)

    return distribution

def duplicate_count(dataset):

    seen = set()

    duplicates = 0

    for example in dataset:

        key = (
            example["text"],
            example["intent"]
        )

        if key in seen:

            duplicates += 1

        else:

            seen.add(key)

    return duplicates

def question_length_statistics(dataset):

    lengths = []

    for example in dataset:

        lengths.append(
            len(example["text"])
        )

    return {

        "minimum": min(lengths),

        "maximum": max(lengths),

        "average": round(
            sum(lengths) / len(lengths),
            2
        )

    }

def random_samples(dataset, sample_count=5):

    grouped_examples = {}

    for example in dataset:

        intent = example["intent"]

        if intent not in grouped_examples:

            grouped_examples[intent] = []

        grouped_examples[intent].append(example["text"])

    for intent, questions in grouped_examples.items():

        print("\n" + "=" * 60)

        print(f"{intent.upper()}")

        print("=" * 60)

        sample_size = min(sample_count, len(questions))

        samples = random.sample(
            questions,
            sample_size
        )

        for sample in samples:

            print(f"• {sample}")

def analyze_dataset():

    dataset = load_dataset()

    print("=" * 60)

    print("DATASET ANALYSIS")

    print("=" * 60)

    print(f"\nTotal Examples : {dataset_size(dataset)}")

    print("\nIntent Distribution")

    print("---------------------")

    distribution = intent_distribution(dataset)

    for intent, count in sorted(distribution.items(),
                                key=lambda item: item[1],
                                reverse=True):
        print(f"{intent:<20} {count}")

    print(f"\nDuplicate Examples : {duplicate_count(dataset)}")

    stats = question_length_statistics(dataset)

    print("\nQuestion Length Statistics")

    print("---------------------------")

    print(f"Minimum Length : {stats['minimum']}")

    print(f"Maximum Length : {stats['maximum']}")

    print(f"Average Length : {stats['average']}")

    print("\nRandom Samples")

    random_samples(dataset)

if __name__ == "__main__":

    analyze_dataset()