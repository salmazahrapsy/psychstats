import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Any

class MoodleQuestionGenerator:
    """
    Transforms psychological, statistical, and clinical concepts from 
    PsychStats Wiki into validated Moodle XML and Aiken format question banks 
    mapped across Bloom's Revised Taxonomy.
    """

    def __init__(self, output_dir: str = "data/assessments"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_canonical_assessment_items(self) -> List[Dict[str, Any]]:
        """
        Returns verified assessment items mapped across Bloom's Taxonomy,
        aligned with PsychStats Wiki, APA Division 12, and Kemenkes RI guidelines.
        """
        return [
            {
                "id": "PSY-GAD-001",
                "category": "$course$/Psychology/Clinical_Psychopathology",
                "name": "GAD Diagnostic Duration and Autonomic Symptoms",
                "bloom_level": "Remembering",
                "difficulty": "Easy",
                "source_url": "https://psychstats.miraheze.org/wiki/Psychology/Generalized_Anxiety_Disorder",
                "question_text": "According to DSM-5-TR and WHO ICD-11 diagnostic criteria, what is the minimum duration of excessive, uncontrollable worry required to establish a diagnosis of Generalized Anxiety Disorder (GAD)?",
                "choices": [
                    {"label": "A", "text": "At least 6 months, occurring more days than not", "fraction": 100, "feedback": "Correct. DSM-5-TR and ICD-11 mandate persistent worry for at least 6 months accompanied by minimum 3 autonomic/motor symptoms."},
                    {"label": "B", "text": "At least 2 weeks, accompanied by depressed mood", "fraction": 0, "feedback": "Incorrect. A 2-week threshold characterizes a Major Depressive Episode, not GAD."},
                    {"label": "C", "text": "At least 1 month following an identifiable acute stressor", "fraction": 0, "feedback": "Incorrect. This timeline describes Acute Stress Disorder or Adjustment Disorder."},
                    {"label": "D", "text": "At least 12 months with intermittent panic attacks", "fraction": 0, "feedback": "Incorrect. 12 months is not required for primary GAD diagnostic threshold."}
                ],
                "general_feedback": "Diagnostic validity for GAD requires excessive anxiety occurring more days than not for at least 6 months about multiple life domains (Source: PsychStats Wiki / DSM-5-TR)."
            },
            {
                "id": "PSY-CBT-002",
                "category": "$course$/Psychology/Psychotherapy_Interventions",
                "name": "CBT Graded Exposure Mechanism in Panic Disorder",
                "bloom_level": "Understanding",
                "difficulty": "Medium",
                "source_url": "https://psychstats.miraheze.org/wiki/Psychotherapy/Cognitive_Behavioral_Therapy",
                "question_text": "In first-line Cognitive Behavioral Therapy (CBT) protocols for panic disorder, what is the primary neurobehavioral mechanism underlying interoceptive exposure?",
                "choices": [
                    {"label": "A", "text": "Extinction of catastrophic misinterpretations via systematic habituation to somatic sensations", "fraction": 100, "feedback": "Correct. Interoceptive exposure induces benign somatic sensations (hyperventilation, tachycardia) to facilitate inhibitory learning and cognitive re-appraisal."},
                    {"label": "B", "text": "Immediate suppression of autonomic arousal through deep diaphragmatic avoidance", "fraction": 0, "feedback": "Incorrect. Somatic suppression acts as a safety behavior that maintains panic vulnerability."},
                    {"label": "C", "text": "Desensitization of unconscious psychodynamic defense mechanisms", "fraction": 0, "feedback": "Incorrect. This reflects psychoanalytic models, not empirical CBT learning theory."},
                    {"label": "D", "text": "Pharmacodynamic downregulation of postsynaptic serotonin receptors", "fraction": 0, "feedback": "Incorrect. Pharmacodynamics relates to SSRI pharmacotherapy, not behavioral exposure."}
                ],
                "general_feedback": "Interoceptive exposure targets conditioned fear of somatic sensations, facilitating cognitive restructuring across 12-16 weekly clinical sessions (Source: PsychStats Wiki)."
            },
            {
                "id": "STAT-ZSCORE-003",
                "category": "$course$/Statistics/Psychometrics",
                "name": "Z-Score Standardization & Normative Interpretation",
                "bloom_level": "Applying",
                "difficulty": "Medium",
                "source_url": "https://psychstats.miraheze.org/wiki/Statistics/Descriptive_Statistics",
                "question_text": "A patient completes a standardized Depression Scale where the normative mean is 50 with a standard deviation of 10. The patient obtains a raw score of 72. What is their standardized Z-score, and how is it interpreted clinically?",
                "choices": [
                    {"label": "A", "text": "Z = +2.20; indicates severe symptomatology exceeding 98% of the normative population", "fraction": 100, "feedback": "Correct. Z = (72 - 50) / 10 = 2.20. In standard Gaussian distributions, Z >= 2.0 indicates clinical elevation exceeding the 97.7th percentile."},
                    {"label": "B", "text": "Z = +1.20; indicates mild distress within the average range", "fraction": 0, "feedback": "Incorrect. Calculation error. (72 - 50) / 10 is 2.20, not 1.20."},
                    {"label": "C", "text": "Z = -2.20; indicates unusually low depressive affect", "fraction": 0, "feedback": "Incorrect. Sign error; a raw score of 72 is above the mean, yielding a positive Z-score."},
                    {"label": "D", "text": "Z = +22.0; indicates statistical invalidity of the assessment instrument", "fraction": 0, "feedback": "Incorrect. Division by standard deviation was omitted in this calculation."}
                ],
                "general_feedback": "Standard score transformation Z = (X - μ) / σ maps patient metrics onto the standard Gaussian curve for clinical normative benchmarking (Source: PsychStats Wiki / Layer 3 Normalization)."
            },
            {
                "id": "CLIN-ETHICS-004",
                "category": "$course$/Clinical_Governance/JPAIS_Standards",
                "name": "Clinical AI SaMD Liability & Legal Oversight",
                "bloom_level": "Evaluating",
                "difficulty": "Hard",
                "source_url": "https://github.com/salmazahrapsy/psychstats/blob/main/policies/JPAIS_MED_REF/PHYSICIAN_OVERSIGHT_STANDARDS.md",
                "question_text": "Under Indonesian Health Law (UU RI No. 17 Tahun 2023) and the JPAIS-MED-REF Clinical Oversight Standards, who holds legal diagnostic responsibility when a clinician uses an AI Clinical Decision Support (CDS) recommendation?",
                "choices": [
                    {"label": "A", "text": "The licensed human clinician (DPJP / Psikolog Klinis) retains sole medical responsibility", "fraction": 100, "feedback": "Correct. Under UU No. 17/2023 and JPAIS-MED-REF, AI CDS tools are advisory instruments; legal diagnostic responsibility cannot be transferred to algorithms."},
                    {"label": "B", "text": "The cloud software vendor hosting the LLM API endpoint", "fraction": 0, "feedback": "Incorrect. Cloud software vendors provide technical infrastructure, not licensed medical diagnosis."},
                    {"label": "C", "text": "Joint statutory liability shared equally between the AI model and the hospital IT department", "fraction": 0, "feedback": "Incorrect. Clinical liability under Indonesian law rests strictly with licensed professionals."},
                    {"label": "D", "text": "The Ministry of Health (Kemenkes RI) through automatic state indemnity", "fraction": 0, "feedback": "Incorrect. Kemenkes regulates clinical practice guidelines but does not assume individual practitioner liability."}
                ],
                "general_feedback": "The Physician-in-the-Loop (PITL) mandate enforces that AI CDS operates strictly as an advisory instrument, preserving human clinician accountability (Source: JPAIS-MED-REF / UU No. 17/2023)."
            }
        ]

    def export_aiken(self, questions: List[Dict[str, Any]], filename: str = "psychstats_question_bank.aiken.txt") -> str:
        """Exports questions into Moodle Aiken format (.txt)."""
        filepath = os.path.join(self.output_dir, filename)
        lines = []

        for q in questions:
            lines.append(q["question_text"])
            correct_label = "A"
            for c in q["choices"]:
                lines.append(f"{c['label']}. {c['text']}")
                if c["fraction"] == 100:
                    correct_label = c["label"]
            lines.append(f"ANSWER: {correct_label}")
            lines.append("")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return filepath

    def export_moodle_xml(self, questions: List[Dict[str, Any]], filename: str = "psychstats_question_bank.xml") -> str:
        """Exports questions into Moodle XML format (.xml) with categories, tags, and feedback."""
        filepath = os.path.join(self.output_dir, filename)
        root = ET.Element("quiz")

        current_category = None
        for q in questions:
            if q["category"] != current_category:
                current_category = q["category"]
                cat_q = ET.SubElement(root, "question", type="category")
                cat_tag = ET.SubElement(cat_q, "category")
                cat_text = ET.SubElement(cat_tag, "text")
                cat_text.text = current_category

            question_el = ET.SubElement(root, "question", type="multichoice")
            
            name_el = ET.SubElement(question_el, "name")
            name_text = ET.SubElement(name_el, "text")
            name_text.text = f"[{q['id']}] {q['name']}"

            qtext_el = ET.SubElement(question_el, "questiontext", format="html")
            qtext_body = ET.SubElement(qtext_el, "text")
            qtext_body.text = f"<p>{q['question_text']}</p><p><small><em>Source: <a href='{q['source_url']}'>PsychStats Knowledge Base</a></em></small></p>"

            gen_fb_el = ET.SubElement(question_el, "generalfeedback", format="html")
            gen_fb_text = ET.SubElement(gen_fb_el, "text")
            gen_fb_text.text = f"<p>{q['general_feedback']}</p>"

            def_grade = ET.SubElement(question_el, "defaultgrade")
            def_grade.text = "1.0"
            penalty = ET.SubElement(question_el, "penalty")
            penalty.text = "0.3333333"
            hidden = ET.SubElement(question_el, "hidden")
            hidden.text = "0"
            single = ET.SubElement(question_el, "single")
            single.text = "true"
            shuffle = ET.SubElement(question_el, "shuffleanswers")
            shuffle.text = "true"
            answernumbering = ET.SubElement(question_el, "answernumbering")
            answernumbering.text = "abc"

            for c in q["choices"]:
                ans_el = ET.SubElement(question_el, "answer", fraction=str(c["fraction"]), format="html")
                ans_text = ET.SubElement(ans_el, "text")
                ans_text.text = f"<p>{c['text']}</p>"
                fb_el = ET.SubElement(ans_el, "feedback", format="html")
                fb_text = ET.SubElement(fb_el, "text")
                fb_text.text = f"<p>{c['feedback']}</p>"

            tags_el = ET.SubElement(question_el, "tags")
            tags_to_add = [
                f"bloom:{q['bloom_level'].lower()}",
                f"difficulty:{q['difficulty'].lower()}",
                f"source:{q['id']}"
            ]
            for tag_str in tags_to_add:
                tag_el = ET.SubElement(tags_el, "tag")
                tag_text = ET.SubElement(tag_el, "text")
                tag_text.text = tag_str

        xml_bytes = ET.tostring(root, encoding="utf-8")
        pretty_xml = minidom.parseString(xml_bytes).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(pretty_xml)
        return filepath

    def build_all(self):
        print("=== Generating Moodle Assessment Artifacts ===")
        items = self.get_canonical_assessment_items()
        print(f"Loaded {len(items)} canonical psychometric & clinical items.")

        aiken_path = self.export_aiken(items)
        print(f"✓ Exported Aiken Question Bank: {aiken_path}")

        xml_path = self.export_moodle_xml(items)
        print(f"✓ Exported Moodle XML Question Bank:   {xml_path}")

        print("\nBloom's Revised Taxonomy Coverage:")
        for it in items:
            print(f"  • [{it['id']}] {it['bloom_level']:<14} | {it['name']}")
        print(f"\nReady for import into Moodle LMS (https://salmazahra.moodiy.org/my/).")

if __name__ == "__main__":
    generator = MoodleQuestionGenerator()
    generator.build_all()
