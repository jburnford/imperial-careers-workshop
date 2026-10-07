#!/usr/bin/env python3
"""Run the workshop's two extraction prompts against an OpenAI-compatible vLLM server (Qwen3.8-27B-FP8 on
Plato in the saved run). Plain urllib so it runs inside the vLLM container.

This is the "saved code" for run C. Unlike runs A and B, the model here is not a coding agent: it cannot
write or run a script, so the historian's second prompt is given a one-sentence addition asking for the
records as JSON followed by a notes section. Everything else is verbatim.

    python3 02_extract.py --base-url http://127.0.0.1:8137/v1 --sources DIR --out DIR [--thinking]
"""
import argparse, json, pathlib, re, time, urllib.request

PROMPT_1 = ("Read these Tropical Agriculturist passages. Propose a small table for studying the people and "
            "activities mentioned. Show two example records before processing the rest. Preserve the printed "
            "wording and source references. Keep inferred information separate from what the text states. Use "
            "local record identifiers and do not add Wikidata identifiers yet.")
PROMPT_2 = ("Use the agreed fields to process this sample. Save the code, instructions, and output so we can "
            "inspect and rerun the work. Report failed records and uncertain readings. Do not expand a person's "
            "name unless the source provides the expansion; record any outside identification separately.")
PROMPT_2_ADDITION = ("\n\n(You cannot save files yourself. Return all the records, for both passages, as a JSON "
                     "array inside one ```json block, using your proposed fields; then a section headed "
                     "'## Notes' with failed records, uncertain readings, and anything inferred rather than read.)")
SYSTEM = ("You are assisting a historian with a small data-structuring task. Work only from the passages "
          "given in this conversation.")

def call(base, model, messages, thinking, max_tokens):
    body = {"model": model, "messages": messages, "temperature": 0, "max_tokens": max_tokens,
            "chat_template_kwargs": {"enable_thinking": bool(thinking)}}
    if not thinking:
        body["reasoning_effort"] = "none"
    req = urllib.request.Request(base.rstrip('/') + "/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=3600) as r:
        d = json.load(r)
    msg = d["choices"][0]["message"]
    return msg.get("content") or "", msg.get("reasoning_content") or msg.get("reasoning") or "", d.get("usage", {}), time.time() - t0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-url', required=True)
    ap.add_argument('--model', default='Qwen/Qwen3.8-27B-FP8')
    ap.add_argument('--sources', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--thinking', action='store_true')
    ap.add_argument('--max-tokens', type=int, default=24000)
    a = ap.parse_args()
    src = pathlib.Path(a.sources); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    passages = ("Passage S04, The Tropical Agriculturist, July 1883, p. 66 (OCR text):\n\n" + (src / 'S04_ocr.txt').read_text()
                + "\n\n----\n\nPassage S03, The Tropical Agriculturist, July 1883, p. 37 (OCR text):\n\n" + (src / 'S03_ocr.txt').read_text())
    log = {"model": a.model, "thinking": a.thinking, "temperature": 0, "turns": []}

    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": PROMPT_1 + "\n\n" + passages}]
    c1, r1, u1, t1 = call(a.base_url, a.model, messages, a.thinking, a.max_tokens)
    (out / '01_structure.md').write_text(c1 + "\n")
    if r1: (out / '01_reasoning.txt').write_text(r1)
    log["turns"].append({"prompt": "PROMPT_1 verbatim + passages", "usage": u1, "seconds": round(t1, 1)})

    messages += [{"role": "assistant", "content": c1},
                 {"role": "user", "content": PROMPT_2 + PROMPT_2_ADDITION}]
    c2, r2, u2, t2 = call(a.base_url, a.model, messages, a.thinking, a.max_tokens)
    (out / '02_response.md').write_text(c2 + "\n")
    if r2: (out / '02_reasoning.txt').write_text(r2)
    log["turns"].append({"prompt": "PROMPT_2 verbatim + PROMPT_2_ADDITION", "usage": u2, "seconds": round(t2, 1)})

    m = re.search(r"```json\s*(.*?)```", c2, re.S)
    records, parse_error = None, ""
    if m:
        try: records = json.loads(m.group(1))
        except Exception as e: parse_error = f"JSON block did not parse: {e}"
    else:
        parse_error = "no ```json block in the response"
    if records is not None:
        (out / '02_records.json').write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    notes = c2.split("## Notes", 1)[1] if "## Notes" in c2 else ""
    (out / '02_notes.md').write_text("# Notes (as returned by the model)\n" + notes + "\n")
    log["records"] = len(records) if isinstance(records, list) else None
    log["parse_error"] = parse_error
    (out / 'run.json').write_text(json.dumps(log, indent=2) + "\n")
    print(json.dumps(log, indent=2))

if __name__ == '__main__':
    main()
