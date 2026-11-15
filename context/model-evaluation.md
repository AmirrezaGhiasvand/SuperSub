# Model evaluation

Candidates: existing Whisper Large V3 Turbo; https://huggingface.co/givia/whisper-large-v3-turbo-persian (colloquial Persian candidate; preserve attribution/license on redistribution); https://huggingface.co/Nimruz/Nava-ct2 (disabled pending validated forced alignment).

Local Turbo passed isolated silence and an eight-second speech sample yielding 11 timed words. These verify pipeline operation, not quality. No comparable three-model WER/CER benchmark exists.

Compare identical clean/noisy/technical/mixed-language/long clips, including silence, music and speech crossing chunk boundaries. Measure WER/CER with stated Persian normalization, colloquial fidelity, duplicate/missing words, timing drift, runtime and memory. Evaluate the shipped INT8/greedy/chunked pipeline, not model-card scores. Recommend a specialist default only after recognition and timing validation.
