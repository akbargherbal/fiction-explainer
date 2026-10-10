# Comprehension questions — the transformer architecture

Ask these of a reader who has seen only the finished story. Questions only; the answer key is in `01_spec.md` §7.

## Mechanism

Q1. When a sentence first goes into the model, what is the text broken into, and what does each piece turn into before anything else happens? What is *not* stored in that result?

Q2. Inside self-attention, where do the numbers that decide how much one token matters to another actually come from? Walk through what happens to a query and the keys, what the softmax does with the scores, and what the weights are ultimately used for.

Q3. What are the two main things a single transformer block does? What do the residual connection and the normalisation do around each of them, and what changes when you stack many blocks?

Q4. Starting from the model's final vector for the last position, how does it arrive at the next word? Describe the order of steps, and say how the word is finally picked.

## Transfer

Q5. You give the model a long prompt in which one word near the very beginning is doing all the work of shaping the next word. There is no fact table and no stored sentence anywhere in the model. Explain how that distant word can still change the model's next-word chances.

Q6. Suppose the model's context window is smaller than your prompt, so the earliest part of the prompt is cut off. Predict how the model's next-word distribution changes, and explain why.

Q7. A user runs the same prompt twice with sampling switched on and gets two different answers. They then set the temperature very low and get the same answer both times. Explain why both results come from the same model — and say whether the low-temperature setting makes the answer any more factually correct.

## Misconception probes

Q8. True or false: when the model answers a factual question correctly, it finds the fact in a store of knowledge built during training and reads it out. Explain your answer.

Q9. True or false: self-attention means the model understands the sentence by deliberately focusing on the words that matter, the way a person concentrates. Explain your answer.

## Boundary

Q10. The story presents the model as producing one token at a time from a probability distribution. Describe a situation or behaviour where that picture would break down or give a misleading account of what a real chat model is doing.
