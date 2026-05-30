Try each. The hint columns are intentionally light — peek only if stuck.

| # | Task | Hint |
|---|---|---|
| 1 | Modify `01_first_message.py` to also print whether `usage.output_tokens > 30`. | `resp.usage.output_tokens` |
| 2 | Make `02_multi_turn.py` save the entire chat history to `chat.json` on exit. | `json.dump(history, open("chat.json","w"))` |
| 3 | Add a 4th persona to `03_system_prompt.py`: "Sarcastic but technically correct DBA". Compare outputs. | none |
| 4 | Change `04_streaming.py` to also count tokens-per-second. | `time.perf_counter()` before / after |
| 5 | In `05_structured_output.py` pattern B, add a new field `confidence` (number 0–1) to the tool schema. Re-run. | extend `properties` and `required` |
| 6 | Feed `06_vision.py` an image of your own (screenshot a sample dashboard) and ask for accessibility issues. | base64 path in the file |
| 7 | In `07_stop_reasons_and_errors.py` force a `max_tokens` truncation (set `chunk_tokens=20`) and confirm the loop continues. | inspect the prints |

## Mini quiz answers (from README)

1. `system`, `user`, `assistant`.
2. Because the API expects the next turn to be the assistant — the model — so the last input must be from the user.
3. `max_tokens`.
4. `tool_use`.
5. **Prefilling** the assistant turn with `{`, and **tool-use-as-formatter** with `tool_choice={"type":"tool","name":...}`.
