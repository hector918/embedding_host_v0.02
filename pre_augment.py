### TODO: this is just a test. You need batch generating that could run for a long time and save them.

from transformers import pipeline





def gen_augmentations(
        prototype,
        generator,
        prompt,
        num_augmentations=6):
    prompt = prompt.format(prototype)

    augmenteds = []
    for _ in range(num_augmentations):
        augmented = generator(prompt, max_length=512, num_return_sequences=1)[0]['generated_text']
        augmenteds.append(augmented)
    return augmenteds


if __name__ == "__main__":
    generator = pipeline("text-generation", model="gpt-3.5-turbo")
    prompt = f"Generate an article on the same topic as the following article: {}"

    augmenteds = gen_augmentations(
            prototype=article,
            generator=generator,
            prompt=prompt,
            )

    df = pd.DataFrame(augmenteds, columns="article")
    df.to_csv("../test/test.csv")
