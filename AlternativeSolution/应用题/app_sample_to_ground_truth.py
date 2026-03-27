import os
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "JudgerTesting" / "NewSample" / "全栈工程师" / "应用题"
OUTPUT_FILE = BASE_DIR / "AlternativeSolution" / "应用题" / "app_ground_truth.json"

def parse_markdown_file(filepath: Path) -> list[dict]:
    content = filepath.read_text(encoding="utf-8")
    
    # Extract correct answer
    correct_answer_match = re.search(r"正确答案：(.*)", content)
    correct_answer = correct_answer_match.group(1).strip() if correct_answer_match else ""

    # Extract question
    question_match = re.search(r"题目：\n(.*?)(?=\n\n样本测试序号|\Z)", content, re.S)
    question = question_match.group(1).strip() if question_match else ""
    
    # Split by separator or sample start
    samples = []
    
    # Find all sample blocks
    sample_blocks = re.split(r"————————", content)
    
    for block in sample_blocks:
        block = block.strip()
        if not block:
            continue
            
        case_id_match = re.search(r"样本测试序号\s+([A-Za-z0-9\-]+)", block)
        if not case_id_match:
            continue
            
        case_id = case_id_match.group(1).strip()
        
        level_score_match = re.search(r"STARE_level:\s*(.*?)\s*/\s*score:\s*(\d+)", block)
        stare_level = level_score_match.group(1).strip() if level_score_match else ""
        score = int(level_score_match.group(2).strip()) if level_score_match else 0
        
        answer_match = re.search(r"模拟候选人回答：\n(.*?)(?=\n\n备注：|\Z)", block, re.S)
        answer = answer_match.group(1).strip() if answer_match else ""
        
        notes_match = re.search(r"备注：\n(.*?)(?=\Z)", block, re.S)
        notes = notes_match.group(1).strip() if notes_match else ""
        
        samples.append({
            "file_name": filepath.name,
            "question": question,
            "correct_answer": correct_answer,
            "case_id": case_id,
            "stare_level": stare_level,
            "score": score,
            "simulated_answer": answer,
            "notes": notes
        })
        
    return samples

def main():
    all_samples = []
    
    if not INPUT_DIR.exists():
        print(f"Directory not found: {INPUT_DIR}")
        return
        
    for filepath in sorted(INPUT_DIR.glob("*.md")):
        print(f"Parsing {filepath.name}...")
        samples = parse_markdown_file(filepath)
        all_samples.extend(samples)
        
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_samples, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully wrote {len(all_samples)} samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
