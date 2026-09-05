import json
import random
from itertools import product

from dataset_blueprint import INTENT_BLUEPRINT

def load_blueprint():
    return INTENT_BLUEPRINT

def generate_examples(blueprint):
    examples = []

    for intent , templates in blueprint.items():
        for template in templates:
            generated_examples = expand_template(template , intent)
            examples.extend(generated_examples)
    return examples

def expand_template(template, intent):
    generated_examples = []
    patterns = template["pattern"]
    if isinstance(patterns, str):
        patterns = [patterns]
    variables = template.get("variables")
    is_symmetric = template.get("symmetric" , False)

    for pattern in patterns:
        if not variables:
            generated_examples.append(
                {
                    "text":pattern,
                    "intent":intent
                }
            )
            continue
        
        variable_names = list(variables.keys())
        variable_values = list(variables.values())
        
        all_combinations = product(*variable_values)
        seen_comparisons = set()
        for combination in all_combinations:
            mapping = dict(
                zip(variable_names , combination)
            )
            if is_symmetric and combination[0] == combination[1]:
                continue
        
            if is_symmetric:
        
                comparison_key = tuple(sorted(combination))
        
                if comparison_key in seen_comparisons:
                    continue
        
                seen_comparisons.add(comparison_key)
        
            question = pattern.format(**mapping)
        
            generated_examples.append(
                {
                    "text":question,
                    "intent":intent
                }
            )
    return generated_examples

def remove_duplicates(dataset):

    seen = set()

    unique_examples = []

    for example in dataset:

        key = (example["text"], example["intent"])

        if key not in seen:

            seen.add(key)

            unique_examples.append(example)

    return unique_examples

def shuffle_dataset(dataset):

    random.shuffle(dataset)

    return dataset

def save_dataset(dataset):

    with open(
        "datasets/raw/intent_dataset.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=4,
            ensure_ascii=False
        )

def generate_dataset():

    blueprint = load_blueprint()

    dataset = generate_examples(blueprint)

    dataset = remove_duplicates(dataset)

    dataset = shuffle_dataset(dataset)

    save_dataset(dataset)

    print(f"Generated {len(dataset)} examples.")

if __name__ == "__main__":
    generate_dataset()