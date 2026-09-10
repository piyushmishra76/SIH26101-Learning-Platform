import re


def clean_text(text: str) -> str:
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace 3 or more consecutive newlines with 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces at the beginning/end of each line
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    # Remove unnecessary blank lines at the beginning/end
    text = text.strip()

    return text
if __name__ == "__main__":
    sample_text = """
        Statistical     Methods


        Sampling     is a method of selecting
        units from a population.


        """

    print(clean_text(sample_text))