# Prompt: Content from a call or transcript

The single best content source in the business. Real questions from real couples.

## Inputs needed
- The transcript, notes, or recording summary
- Who was on the call, by role not by name
- Whether anything said is confidential

## The prompt

```
Pull content out of this call.

Transcript:
[paste, or give the file path]

Give me:
1. Every question the couple asked, in their own words
2. Anything they were visibly relieved to hear
3. Anything that surprised them
4. Anything they had wrong about how it works
5. For each, whether it is worth a story frame, a reel, or a carousel

Rank by how likely another couple has the same question.

Then write the top three as posts.

Rules:
- Never publish anything a client said without permission. Use the pattern, not the
  person. "Couples often ask" is fine, "one of our couples said" is not
- A wrong assumption becomes a "do not" post, which is the strongest shape we have

Read sop/calls-to-faq-content.md and playbooks/education.md first.
```

## Output format
The four lists, ranked, plus three finished posts.

## Quality standard
Real questions in real words. Not tidied into marketing language.

## Brand rules
No client is named or quoted without permission. No confidential detail: budgets,
family situations, vendor disputes. The pattern is the asset, not the person.

## CTA rules
Education posts still convert. Match the ask to the lesson.
