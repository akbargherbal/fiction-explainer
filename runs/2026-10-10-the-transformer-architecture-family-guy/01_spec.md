# Concept spec: The transformer architecture (the family of models behind ChatGPT)

Overall confidence: HIGH · Researched: 2026-10-10 · Versions covered: "Attention Is All You Need" arXiv:1706.03762v7 (2017, last revised 2023); Hugging Face Transformers v5.19.0 generation docs (2025–26); Wikipedia "Transformer (deep learning)" and "Context window" (2026 revisions); numpy 2.1.3 / Python 3.13.16 for the scratch demos.

The mechanisms below are stable across the transformer family. Things that *do* vary by model and version are flagged in §5: the original 2017 model is an encoder–decoder with 6 layers, d_model=512, 8 heads and fixed sine/cosine positions; today's chat models are decoder-only, often use pre-layer-norm, rotary positions, far more layers, and much bigger vectors. Where the story simplifies, it must simplify in a direction that stays true to both.

## 1. Scope

**In scope — the story must teach each of these with its own cutaway:**

- C1 Tokens → embeddings (MUST)
- C2 Self-attention: query/key/value, scaled dot-product, softmax weights (MUST)
- C3 The transformer block and the stack: attention + feed-forward, residual, normalisation (MUST)
- C4 Next-token prediction and sampling (MUST)
- C5 Multi-head attention (SHOULD)
- C6 Position / why order has to be injected (SHOULD)

**Optional, include only if the outline has room:**

- The context window and the KV cache as "why the second word is faster than the first." Treated in §5, not as a numbered concept. If the outline is tight, this is the first thing to cut.

**Out of scope (do not attempt in ~2,500 words):** training (backpropagation, gradient descent, optimisers, loss), RLHF / instruction tuning, the encoder–decoder split in detail, specific vendors or model sizes, tokenizer internals beyond "text is split into sub-word pieces," long-context approximations, attention visualisation research, multimodal transformers, safety and alignment.

**What the audience already knows:** they have used ChatGPT. They have seen it talk, get things wrong, and produce different wording on repeat runs. They have no ML background: no vectors, no matrices, no calculus. The story therefore carries no equations; the equations live here so critics can check whether a scene is telling the truth.

**Reserved for the plan's decision #7:** the approved plan allows at most one SHOULD concept. If the outline is tight, keep **C5 (multi-head)** as that one and fold **C6 (position)** into C1/C2 as a short beat (name-tags added to the embeddings; attention is order-blind without them). Invariants I3 and I4 must hold either way.

## 2. Core concepts

### C1 Tokens → embeddings — priority: MUST

- **Definition:** Text is broken by a tokenizer into *tokens* — sub-word pieces, not always whole words. Each token becomes an integer id, and each id indexes one row of a learned *embedding matrix*, giving a fixed-length vector of numbers. That vector is the only thing the model ever sees.
- **Mechanism:** tokenizer (e.g. byte-pair encoding) splits the text → integer ids → the embedding table is indexed by id → a vector per token. The original paper used a shared ~37,000-token byte-pair vocabulary and vectors of length 512. There is no definition stored in a vector; "cat" and "kitten" end up near each other only because training moved them there, if it did at all.
- **Dramatizable as:** a cutaway to Peter running the family's sentence through a butcher's meat-slicer that chops words into odd chunks ("unbeliev-" / "able"), each chunk getting a numbered ticket. A bored clerk pulls a laminated number-card for each ticket. The same word always draws the same card; two similar words may draw similar cards; no card contains a meaning or a fact.
- **Misconception:** M1, M3.
- **Source:** [Attention Is All You Need, §3.4 & §5.1](https://arxiv.org/html/1706.03762v7) · HIGH; [Transformer (deep learning), Tokenization/Embedding](https://en.wikipedia.org/wiki/Transformer_(deep_learning)) · HIGH.

### C2 Self-attention: query, key, value, scaled dot-product, softmax — priority: MUST

- **Definition:** For each token the model computes a *query*, a *key* and a *value* vector from that token's current representation (three learned linear projections). Every query is compared with every key, the match scores are scaled, turned into weights by a softmax, and used to blend the values into new representations.
- **Mechanism (correct causal order):**
  1. From the current vectors X, compute Q = X·W^Q, K = X·W^K, V = X·W^V (learned projections).
  2. Scores = Q·Kᵀ: each query against all keys. (A "compatibility" measure.)
  3. Divide every score by √d_k, where d_k is the query/key length. Without this, for large d_k the dot products grow large, and softmax saturates into a region with almost no gradient.
  4. Softmax each row → weights between 0 and 1 that sum to 1.
  5. Output = weights · V. Each token's new representation is a weighted blend of the values — weighted by how well its query matched each key.
  - The weights are computed **from the current input**. Nothing is fetched from a stored fact table; the "relevance" is a fresh dot product every time.
- **Dramatizable as:** a speed-dating cutaway. Every token holds a "wanted" card (query) and an "offering" card (key). A matchmaker compares every wanted card against every offering card, stamps each score with a nerdily exact "÷√64" mark, converts the scores into a percentage split that must total 100% (softmax), and each token leaves carrying a blended cocktail (value) mixed in exactly those percentages. Running gag: change who is in the room and every percentage changes — there is no master list.
- **Misconception:** M1, M2.
- **Source:** [Attention Is All You Need, §3.2.1, eq. (1), Figure 2](https://arxiv.org/html/1706.03762v7) · HIGH; verified numerically in `scratch/attention_demo.py` §3.

### C3 The transformer block and the stack — priority: MUST

- **Definition:** A *block* is self-attention followed by a position-wise feed-forward network. Each sub-layer is wrapped as LayerNorm(x + Sublayer(x)): a residual connection adds the sub-layer's change to its own input, then normalisation rescales to keep the numbers stable. The block is stacked N times (N = 6 in the original).
- **Mechanism:** within one block: (a) multi-head self-attention mixes information *across* tokens; (b) residual add + layer-norm; (c) a feed-forward network — two linear layers with a ReLU between them (inner size 2048 vs model size 512) — is applied to *each position independently*; (d) residual add + layer-norm. Repeat N times. Depth refines the representation; it does not add a sentence store.
- **Dramatizable as:** a "pass it down the table" cutaway at a long dinner. Each family member is one block. The dish (the representation) circulates. First someone tosses every ingredient together (attention mixes tokens), then each person quietly adjusts *only their own portion* (feed-forward is per-position), and before passing it on they pour the original back in on top (residual) and smooth out the lumps (normalisation). Six tables in a row; each pass is a little more "finished"; nobody writes a recipe down.
- **Misconception:** M3, M5.
- **Source:** [Attention Is All You Need, §3.1 & §3.3, eq. (2)](https://arxiv.org/html/1706.03762v7) · HIGH.

### C4 Next-token prediction and sampling — priority: MUST

- **Definition:** The final vector at the last position is passed through a learned linear layer and a softmax, producing a probability for *every* token in the vocabulary. Generation picks one token from that distribution, appends it to the input, and repeats.
- **Mechanism:** final vector → logits (one number per vocabulary entry) → softmax → a probability distribution that sums to 1 → pick a token. *Greedy* takes the highest-probability token; *sampling* draws a token at random, weighted by the probabilities. *Temperature* T rescales the logits (logits ÷ T) before the softmax: low T sharpens the distribution toward the top token (T → 0 approaches greedy); high T flattens it, giving low-probability tokens more chance. The chosen token is appended and the whole loop runs again. There is no plan and no lookup; the distribution is recomputed from the input so far at every step.
- **Dramatizable as:** a cutaway to the world's most indecisive vending machine. It shows a bar chart of "chances" for every snack in the building and rolls weighted dice instead of "knowing" what Peter wants. It drops the choice into the tray, then asks itself again with the choice added. The temperature dial is labelled "creativity" by Peter; when he turns it up the machine starts coughing up pickled eggs, and the error light comes on. (The machine's error is Peter's belief, not the machine's function — see M4.)
- **Misconception:** M1, M4, M5.
- **Source:** [Attention Is All You Need, §3.4](https://arxiv.org/html/1706.03762v7) · HIGH; [HF Transformers, Generation strategies (sampling)](https://huggingface.co/docs/transformers/en/generation_strategies) · HIGH; [HF blog, How to generate text (temperature)](https://huggingface.co/blog/how-to-generate) · HIGH; verified in `scratch/attention_demo.py` §2 and §6.

### C5 Multi-head attention — priority: SHOULD

- **Definition:** Instead of one attention computation, the block runs *h* attention heads in parallel (h = 8 in the original), each with its own learned projections (d_k = d_v = d_model/h = 64). Each head produces its own weighted blend; the heads' outputs are concatenated and mixed once more by a projection W^O.
- **Mechanism:** all heads read the same input at the same time, each through a different learned "lens," and each computes its own Q/K/V and its own weights. The results are concatenated, not chained. No head feeds the next head.
- **Dramatizable as:** a cutaway with eight identical clones of one family member, each handed the same index cards at the same instant. Each clone wears differently coloured glasses and announces a different "who-matters" ranking simultaneously; a stern editor staples the eight lists side by side (concatenation) and merges them. The gag: Peter demands they line up single-file and "go one at a time," and the whole thing jams.
- **Misconception:** M2 (one head as "the model's single focus"), M5 (heads as steps).
- **Source:** [Attention Is All You Need, §3.2.2, Figure 2](https://arxiv.org/html/1706.03762v7) · HIGH; verified in `scratch/attention_demo.py` §5.

### C6 Position: why order has to be injected — priority: SHOULD

- **Definition:** Self-attention on its own treats the input as an unordered set: nothing in the mechanism distinguishes "dog bites man" from "man bites dog." Information about position is *added* to the embeddings before the first block (the original adds fixed sine/cosine vectors; modern models often use learned or rotary position encodings).
- **Mechanism:** the original computes a fixed positional-encoding vector PE(pos) and adds it to the token embedding at each position: PE(pos,2i) = sin(pos / 10000^(2i/d_model)), PE(pos,2i+1) = cos(pos / 10000^(2i/d_model)). Without position, permuting the tokens just permutes the outputs (the computation is *permutation-equivariant*) — order cannot change the result. With position added, the same words in a different order give different outputs.
- **Dramatizable as:** a police-lineup cutaway. Identical clones ("I", "only", "have", "eyes", "for", "you") stand in a row with no name tags; the detective swaps two of them and the verdict does not change at all (that is order-blindness). Stewie slaps coloured numbered stickers on their foreheads; now swapping two of them flips the whole meaning. Gag: one sticker falls off and the sentence becomes "eyes have only I for you."
- **Misconception:** M5 (that attention "just knows" order on its own).
- **Source:** [Attention Is All You Need, §3.5](https://arxiv.org/html/1706.03762v7) · HIGH; verified in `scratch/attention_demo.py` §4.

## 3. Invariants

I1. The attention weights for a token are computed from that token's query and the current sequence's keys; no scene may imply the model fetches anything from a stored table of facts. (C2)

I2. At every step the model's output is a probability distribution over the whole vocabulary, and the emitted token is drawn from that distribution (or taken by a rule such as argmax); the token is not chosen with intentions, and nothing is "read off." (C4)

I3. With no positional information, self-attention is order-blind: permuting the input tokens permutes the outputs and changes nothing else. Order only affects the result once position is added to the embeddings. (C6)

I4. Multiple attention heads are computed in parallel on the same input and their outputs are concatenated; no head is a step that runs after another head. (C5)

I5. A token's embedding is a learned vector of numbers, not a definition; token ids carry no meaning by themselves, and no embedding row contains a fact, a word's definition, or a stored sentence. (C1)

I6. Inside a block, the feed-forward network acts on each position separately and does not mix information between tokens; mixing across tokens happens only in attention. (C3)

I7. A residual connection makes a sub-layer *add* a change to its input rather than replace it, and normalisation rescales the values to keep training stable; neither one stores memory or retrieves anything. (C3)

I8. Temperature rescales the logits before the softmax; it changes how the next token is *picked*, never what the model has learned. Low temperature tends toward the top token; high temperature flattens the distribution. (C4)

## 4. Misconceptions

M1. **"The model looks things up / 'knows' facts."** Believed: answers come from a database of stored facts. True: the model has only learned vectors in its weights; at generation time it computes a distribution from the current input and samples a token. A story could teach this wrong by showing a character retrieve a card/file/fact that the model then "recites," or by calling the weights "the database." (Refs I1, I2, I5.)

M2. **"Attention means the model understands / focuses like a person."** Believed: attention is deliberate concentration on the important words. True: attention weights are dot products between learned vectors, computed mechanically, with no goal, intent or comprehension. A story could teach this wrong by giving the attention step a "decides what matters" voice-over or by having a character "choose" what to look at. (Refs I1, I4.)

M3. **"The model stores whole sentences and retrieves them."** Believed: training leaves a big library of sentences the model quotes back. True: only numerical weights are stored; text is regenerated token by token and can come out different each time. A story could teach this wrong by showing a filing cabinet of sentences, or the model "pulling up" a previous conversation verbatim. (Refs I2, I5, I7.)

M4. **"Temperature is a free creativity dial."** Believed: turning it up adds imagination at no cost. True: temperature only reshapes the same distribution before sampling — higher T gives lower-probability tokens more chance, which also means more incoherence and more errors; it does not add knowledge, and low T approaches a deterministic greedy pick. A story could teach this wrong by having the character turn up the dial and get *better* (rather than merely different, and usually stranger) answers. (Refs I2, I8.)

M5. **"The model plans the whole sentence before writing."** Believed: it drafts the full reply, then types it out. True: it produces one token, appends it, and recomputes from the new input; there is no sentence-level plan. A story could teach this wrong by showing the model "deciding on its answer" up front and then just emitting it. (Refs I2, I3, I6.)

## 5. Terminology

**Safe to use as-is:** token; tokenizer; embedding; vector; self-attention; query, key, value; score; weight; softmax; scaled dot-product attention; head; multi-head attention; transformer block (use "block," not "layer," to avoid the encoder/decoder ambiguity); residual connection; normalisation / layer norm; feed-forward network; logits; probability distribution; sampling; greedy; temperature; next-token prediction; context window; position / positional encoding.

**Ambiguous or version-dependent — use with care:**
- "layer" — ambiguous (a stack layer vs a sub-layer). Prefer "block" for the repeated unit.
- "position encoding" — 2017 used *fixed sine/cosine*; modern models usually use *learned* or *rotary* (RoPE). Say "position is added to the embeddings" without naming the scheme.
- "layer norm" — the original applies it *after* the residual add (post-LN); many modern models apply it *before* (pre-LN). Either is fine; don't claim a specific order as universal.
- "the transformer" — the 2017 model is an encoder–decoder for translation; ChatGPT-style models are *decoder-only* (predict the next token, no separate encoder). The story is about the family, so describing next-token prediction is safe.
- "attention" — in common speech it means human focus; in the model it is a weighted average. Do not let the word carry its everyday meaning.
- "context window" / "KV cache" — real but optional; the cache is why later tokens can be generated faster, not a memory of meaning.

**Avoid:** "knows," "thinks," "wants," "decides," "remembers," "understands," "brain," "neuron fires," "the model's memory," "looks up," "database." These anthropomorphise and map straight onto M1–M3. "Sees" and "reads" are borderline; prefer "takes as input."

## 6. Verified examples

Script: `runs/2026-10-10-the-transformer-architecture-family-guy/scratch/attention_demo.py` (numpy 2.1.3, Python 3.13.16; deterministic, `rng = default_rng(0)`). The numbers below are the exact printed output.

**Softmax and temperature** (logits `[2, 1, 0]`):
- T=0.5 → `[0.8668, 0.1173, 0.0159]` (max 0.8668)
- T=1.0 → `[0.6652, 0.2447, 0.0900]` (max 0.6652)
- T=2.0 → `[0.5065, 0.3072, 0.1863]` (max 0.5065)
- Reading: lower T sharpens (max rises toward 1); higher T flattens. Flatter is *not* "more correct."

**Scaled dot-product attention**, 3 tokens, d_k = 4, √d_k = 2:
- Raw scores Q·Kᵀ row 0 = `[2, 1, 5]`; scaled = `[1.0, 0.5, 2.5]`.
- Softmax weights row 0 = `[0.1643, 0.0996, 0.7361]`; every row sums to 1.0.
- Output = weights·V row 0 = `[1.6365, 0.8357]`; weights come only from the input Q and K.

**Order-blindness without position** (self-attention, 3 tokens):
- Original order A,B,C → outputs rows `[0.8137 0.4935 0.5065 0.1863]`, `[0.4935 0.8137 0.1863 0.5065]`, `[0.7259 0.7259 0.2741 0.2741]`.
- Permuted order C,A,B → the same three rows re-ordered; `allclose(output_permuted, P @ output) = True`.
- After adding a distinct positional vector to each slot, the same test = `False`: order now changes the result.

**Multi-head attention** (two heads, different projections):
- Head 1 weights row 0 = `[0.1643, 0.0996, 0.7361]`; head 2 weights row 0 = `[0.3837, 0.2327, 0.3837]`.
- Heads produce different weights independently; outputs concatenated: `[1.6365 0.8357 1.1510 0.6163]` (row 0).

**Next-token distribution and sampling** (candidates `["mat","floor","moon","park"]`, logits `[3, 1.5, 0.5, 0]`):
- Softmax probs = `[0.7380, 0.1647, 0.0606, 0.0367]`, sum = 1.0.
- 200 draws from the same distribution: `{mat: 137, floor: 33, moon: 19, park: 11}` — the token is drawn, not chosen.

## 7. Answer key (never shown to the cold reader)

Q1 (tokens → embeddings): the text is split into sub-word tokens; each token id indexes a row of a learned embedding matrix to produce a vector; the vector is the input to everything else; no vector holds a definition. Key: sub-word pieces, ids, table lookup, vector of numbers, no meaning stored.

Q2 (attention scores): each token makes a query, key and value from its current representation; a query is compared with every key by a dot product; the scores are divided by √d_k to stop softmax saturating; softmax turns the row into weights that sum to 1; the values are blended by those weights. Key: scores from the current input, not a lookup; scaling; softmax output is the weights.

Q3 (block and stack): a block is self-attention (mixes tokens) plus a feed-forward network applied per position (does not mix tokens); each sub-layer is wrapped in residual add + layer-norm; the block is repeated N times to refine the representation. Key: two sub-layers; residual = add the change; norm = rescale; stacking = depth, not storage.

Q4 (next token): the final vector becomes logits over the whole vocabulary; softmax turns logits into a probability distribution; a token is sampled (or argmax-chosen); it is appended to the input and the whole thing runs again. Key: distribution, sampling, append-and-repeat, no plan.

Q5 (distant word): attention lets the current query match *any* key in the current input, however far away, so an early word can raise or lower the weights that feed the next-token distribution; nothing is being looked up or retrieved — the effect is a fresh dot product over the prompt as it stands. Key: attention spans the whole input; weights recomputed from the current input.

Q6 (context cut off): anything outside the window is simply not in the input the model computes over; its keys/values are absent, so the next-token distribution no longer reflects it. Key: the model only conditions on what is inside the window.

Q7 (two samples vs temperature): with sampling on, each run draws from the distribution, so different tokens can be picked; at temperature near 0 the distribution becomes so sharp that the top token is picked nearly every time, so the runs agree. Low temperature does not make the content more true — it only makes the pick more predictable. Key: distribution → draw; low T ≈ greedy; truth unchanged.

Q8 (probe M1 — false): the model has no fact store to read from; it has only learned weights. It computes a distribution from the current input and samples a token; when the output is a correct fact it is because the weights encode a pattern that makes the right token probable — the same mechanism that produces errors. Key: no lookup; weights + distribution + sampling.

Q9 (probe M2 — false): self-attention is a weighted average. Queries and keys are learned vectors; their dot products and softmax weights are mechanical. Nothing in the operation has a goal, focuses deliberately, or understands; "attention" is just the name for weighting by similarity of learned vectors. Key: no intent; weights = dot products + softmax; not comprehension.

Q10 (boundary): the one-token-at-a-time sampling picture is the core of the architecture, but it is not the whole of a chat product. It breaks or misleads for: greedy/beam-search decoding (no random draw), instruction tuning / RLHF (which shapes the distribution toward helpful answers without changing the architecture), tool use and retrieval (which inject *external* text into the input — that is a lookup, but outside the model), reasoning/"thinking" modes that generate long internal token sequences first, and any system that re-runs the loop under constraints. Key: architecture vs product; external retrieval is added on top; the base claim "just predicts the next token" is true of the model, not of every behaviour of the app around it.

## 8. Sources

Read in full unless marked otherwise.

1. Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin. *Attention Is All You Need.* arXiv:1706.03762v7, 2017 (v7, 2 Aug 2023). https://arxiv.org/abs/1706.03762 · full text at https://arxiv.org/html/1706.03762v7 (read: §3.1 encoder/decoder stacks, §3.2.1 scaled dot-product attention eq. (1), §3.2.2 multi-head, §3.3 feed-forward, §3.4 embeddings & softmax, §3.5 positional encoding, §5.1 data/vocabulary). HIGH.
2. Hugging Face. *Generation strategies.* Transformers docs v5.19.0 (main). https://huggingface.co/docs/transformers/en/generation_strategies (read: greedy vs sampling; `do_sample`; sampling draws from the distribution). HIGH. (The v5.19.0 `attention` and `logits_process` doc pages returned 404 during research and were not used.)
3. von Platen, P. *How to generate text: using different decoding methods for language generation with Transformers.* Hugging Face blog, 1 Mar 2020 (updated Jul 2023). https://huggingface.co/blog/how-to-generate (read: sampling and temperature — "make the distribution sharper … by lowering the temperature"; temperature → 0 equals greedy decoding). HIGH.
4. Wikipedia. *Transformer (deep learning architecture).* Revision 1379435465 (2026). https://en.wikipedia.org/wiki/Transformer_(deep_learning) (read: lead; tokenization, embedding, positional encoding, scaled dot-product, multi-head, masked attention). MEDIUM–HIGH (tertiary; used only where it agrees with the paper).
5. Wikipedia. *Context window.* Revision 1379392659 (2026). https://en.wikipedia.org/wiki/Context_window (read: definition — tokens in one request; material outside is not directly available). MEDIUM. Optional concept only.
6. Scratch: `scratch/attention_demo.py` (numpy 2.1.3, Python 3.13.16) — the exact outputs quoted in §6. HIGH (directly observed).

Nothing in this spec is UNVERIFIED. The only claims not read from a primary source are the context-window "context rot" nuances, which are deliberately omitted from scope.
