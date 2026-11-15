# Model evaluation

Candidates: existing Turbo, https://huggingface.co/givia/whisper-large-v3-turbo-persian and https://huggingface.co/Nimruz/Nava-ct2. Preserve Givia attribution/license on distribution. Nava requires <=30-second pause-based chunks and a validated separate alignment stage. No local benchmark results yet.

Compare identical Persian clips: clean conversation, names/technical vocabulary, background music, noisy speech, long speech and silence. Record normalized WER/CER, colloquial fidelity, boundary drift, duplicate/missing words, runtime and memory. Do not select a specialist default until recognition and timing both pass. Published model-card scores are not local verification.
