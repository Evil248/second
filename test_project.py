from project.project import extract_everything


def pytest_main():
    test_extract_everything()


def test_extract_everything():
    output_text = """
    Question 1: What is the capital of France?
    Choice A: Berlin
    Choice B: London
    Choice C: Paris
    Choice D: Rome
    Answer 1: C
    """

    # Вызываем вашу функцию и проверяем ожидаемый результат
    result = extract_everything(output_text)

    assert result["question"] == ["Question 1: What is the capital of France?"]
    assert result["A"] == ["Choice A: Berlin"]
    assert result["B"] == ["Choice B: London"]
    assert result["C"] == ["Choice C: Paris"]
    assert result["D"] == ["Choice D: Rome"]
    assert result["Answer"] == ["C"]


if __name__ == "__main__":
    pytest_main()pr
