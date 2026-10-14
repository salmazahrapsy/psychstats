import os
import xml.etree.ElementTree as ET
import pytest
from pipelines.moodle_generator import MoodleQuestionGenerator

@pytest.fixture
def generator(tmp_path):
    return MoodleQuestionGenerator(output_dir=str(tmp_path))

def test_question_items_structure(generator):
    items = generator.get_canonical_assessment_items()
    assert len(items) >= 4

    bloom_levels = {item["bloom_level"] for item in items}
    assert "Remembering" in bloom_levels
    assert "Understanding" in bloom_levels
    assert "Applying" in bloom_levels
    assert "Evaluating" in bloom_levels

    for item in items:
        assert item["id"].startswith(("PSY-", "STAT-", "CLIN-"))
        assert len(item["choices"]) == 4
        fractions = [c["fraction"] for c in item["choices"]]
        assert fractions.count(100) == 1
        assert fractions.count(0) == 3

def test_aiken_export_syntax(generator):
    items = generator.get_canonical_assessment_items()
    aiken_path = generator.export_aiken(items, filename="test.aiken.txt")
    
    assert os.path.exists(aiken_path)
    with open(aiken_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "ANSWER: A" in content
    assert "A. " in content

def test_moodle_xml_validity(generator):
    items = generator.get_canonical_assessment_items()
    xml_path = generator.export_moodle_xml(items, filename="test.xml")

    assert os.path.exists(xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    assert root.tag == "quiz"

    questions = root.findall("./question[@type='multichoice']")
    assert len(questions) == len(items)

    for q in questions:
        assert q.find("name/text") is not None
        assert q.find("questiontext/text") is not None
        assert q.find("generalfeedback/text") is not None
        answers = q.findall("answer")
        assert len(answers) == 4
        tags = [t.text for t in q.findall("tags/tag/text")]
        assert any(t.startswith("bloom:") for t in tags)
