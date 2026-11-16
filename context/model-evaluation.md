# Model selection and evaluation

Repository listings checked 2026-11-16. See [README comparison](../README.md#model-choices), [exact downloads](../README.md#manual-download-exact-files) and [Persian conversion](../README.md#persian-specialist-source-files-and-conversion).

| Candidate | Approximate weight download, not runtime RAM | Status and exact runtime filenames |
| --- | --- | --- |
| [Small](https://huggingface.co/Systran/faster-whisper-small/tree/main) | 484 MB | Multilingual CTranslate2; smaller-footprint candidate. model.bin, config.json, tokenizer.json, vocabulary.txt. Not locally benchmarked. |
| [Medium](https://huggingface.co/Systran/faster-whisper-medium/tree/main) | 1.53 GB | Multilingual CTranslate2; same four filenames, from Medium only. Not locally benchmarked. |
| [Large V3 Turbo](https://huggingface.co/dropbox-dash/faster-whisper-large-v3-turbo/tree/main) | 1.62 GB | Current local operational baseline. model.bin, config.json, tokenizer.json, vocabulary.json, preprocessor_config.json. Old mobiuslabsgmbh URL redirects here. |
| [Large V3](https://huggingface.co/Systran/faster-whisper-large-v3/tree/main) | 3.09 GB | Larger multilingual candidate; same filenames as Turbo, from its own repository. Not locally benchmarked. |
| [Givia Persian Turbo](https://huggingface.co/givia/whisper-large-v3-turbo-persian/tree/main) | 3.24 GB source weights | Transformers source requires conversion to CTranslate2. Exact 12-file source list and conversion command in README. GGML unsupported; Persian profile required; CC-BY-4.0 attribution applies. |
| [Nava CT2](https://huggingface.co/Nimruz/Nava-ct2) | 1.62 GB | Generation disabled pending validated separate alignment. Not a working SRT recommendation. |

Keep model/config/tokenizer/vocabulary from one repository/revision. Small/Medium supply vocabulary.txt and no preprocessor_config.json; do not copy or rename files from other models. File-list verification does not prove universal runtime compatibility.

Only existing Turbo has operational smoke checks: silence and eight-second speech producing 11 timed words. No local WER/CER comparison is complete. No perfect Persian accuracy or speed claims are justified.

Evaluate identical clean/noisy/technical/mixed-language clips, silence/music and long speech across chunk boundaries. Measure normalized WER/CER, colloquial fidelity, missing/duplicate words, timing drift, memory and runtime with the shipped INT8/greedy/chunked pipeline. Recommend a specialist only after recognition and timing pass.
