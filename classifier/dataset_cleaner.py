import json
import random
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RAW_DATASET = BASE_DIR / "datasets" / "raw" / "intent_dataset.json"

PROCESSED_DIR = BASE_DIR / "datasets" / "processed"

MAX_PER_INTENT = 800

TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10

RANDOM_SEED = 42

def load_dataset():
    with open(RAW_DATASET , "r" , encoding="utf-8")as f:
        dataset = json.load(f)
    return dataset

def group_by_intent(dataset):

    grouped = defaultdict(list)

    for example in dataset:

        intent = example["intent"]

        grouped[intent].append(example)

    return grouped

def balance_dataset(grouped_datset):
    random.seed(RANDOM_SEED)

    balanced_dataset = []

    for intent , examples in grouped_datset.items():                 
        if(len(examples) > MAX_PER_INTENT):
            selected_examples = random.sample(examples , MAX_PER_INTENT)
        else:
            selected_examples = examples

        balanced_dataset.extend(selected_examples)

    return balanced_dataset

def shuffle_datset(dataset):
    random.seed(RANDOM_SEED)
    random.shuffle(dataset)

    return dataset

def split_dataset(dataset):
    total_examples = len(dataset)
    train_end = int(total_examples * TRAIN_RATIO)
    validation_end  = train_end + int(total_examples * VAL_RATIO)

    train_dataset = dataset[:train_end]
    validation_datset = dataset[train_end : validation_end]
    test_dataset = dataset[validation_end:]

    return train_dataset , validation_datset , test_dataset

def save_dataset(train_dataset, validation_dataset, test_dataset):

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    datasets = {
        "train.json": train_dataset,
        "validation.json": validation_dataset,
        "test.json": test_dataset
    }

    for filename, dataset in datasets.items():

        filepath = PROCESSED_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:

            json.dump(dataset, f, indent=4)

    print("\nProcessed datasets saved successfully!")

def clean_dataset():

    dataset = load_dataset()
    print(f"Raw Dataset Size       : {len(dataset)}")

    grouped_dataset = group_by_intent(dataset)
    print(f"Number of Intents      : {len(grouped_dataset)}")

    balanced_dataset = balance_dataset(grouped_dataset)
    print(f"Balanced Dataset Size  : {len(balanced_dataset)}")

    shuffled_dataset = shuffle_datset(balanced_dataset)
    print(f"Shuffled Dataset Size  : {len(shuffled_dataset)}")

    train_dataset, validation_dataset, test_dataset = split_dataset(
        shuffled_dataset
    )
    print(f"Train Size             : {len(train_dataset)}")
    print(f"Validation Size        : {len(validation_dataset)}")
    print(f"Test Size              : {len(test_dataset)}")

    save_dataset(
        train_dataset,
        validation_dataset,
        test_dataset
    )

    print("\nDataset Cleaning Completed Successfully!")

if __name__ == "__main__":

    clean_dataset()