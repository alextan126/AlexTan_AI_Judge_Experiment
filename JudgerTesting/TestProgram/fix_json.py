"""Fix unescaped ASCII double quotes inside JSON string values.
Replaces Chinese-context ASCII quotes with proper Unicode quotes."""
import json
import sys
import re

target = sys.argv[1] if len(sys.argv) > 1 else r"c:\Users\60962\Desktop\Succaiss\Experiment\JudgerTesting\Report\算法_Record\1_1\Sample.md"

with open(target, "r", encoding="utf-8") as f:
    content = f.read()

try:
    json.loads(content)
    print("JSON already valid, no fix needed.")
    sys.exit(0)
except json.JSONDecodeError as e:
    print(f"JSON error: {e}")

CJK_PATTERNS = [
    ("\u201c", "\u201d"),
]

lines = content.split("\n")
fixed_lines = []
for line in lines:
    stripped = line.lstrip()
    if not stripped.startswith('"'):
        fixed_lines.append(line)
        continue

    colon_idx = line.find('": "')
    if colon_idx == -1:
        colon_idx = line.find('": [')
    if colon_idx == -1:
        colon_idx = line.find('": {')
    if colon_idx == -1:
        fixed_lines.append(line)
        continue

    val_start = line.find('"', colon_idx + 2)
    if val_start == -1:
        fixed_lines.append(line)
        continue

    key_part = line[:val_start + 1]
    rest = line[val_start + 1:]

    if rest.endswith('",') or rest.endswith('"'):
        end_trim = 2 if rest.endswith('",') else 1
        inner = rest[:-end_trim]
        suffix = rest[-end_trim:]

        has_unescaped = False
        i = 0
        while i < len(inner):
            if inner[i] == '\\' and i + 1 < len(inner):
                i += 2
                continue
            if inner[i] == '"':
                has_unescaped = True
                break
            i += 1

        if has_unescaped:
            new_inner = []
            i = 0
            quote_positions = []
            while i < len(inner):
                if inner[i] == '\\' and i + 1 < len(inner):
                    new_inner.append(inner[i:i+2])
                    i += 2
                    continue
                if inner[i] == '"':
                    quote_positions.append(len(new_inner))
                    new_inner.append(inner[i])
                    i += 1
                    continue
                new_inner.append(inner[i])
                i += 1

            for idx, pos in enumerate(quote_positions):
                if idx % 2 == 0:
                    new_inner[pos] = "\u201c"
                else:
                    new_inner[pos] = "\u201d"

            line = key_part + "".join(new_inner) + suffix

    fixed_lines.append(line)

content = "\n".join(fixed_lines)

try:
    json.loads(content)
    print("JSON validation: OK")
except json.JSONDecodeError as e:
    print(f"Still invalid: {e}")
    sys.exit(1)

with open(target, "w", encoding="utf-8") as f:
    f.write(content)
print("File saved.")
