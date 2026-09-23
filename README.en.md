# Evidence Envelope

### A common record for financial evidence

**Version 0.2.0** · Apache-2.0

> **This repository is the LAMC programme.**
> LAMC is not a crypto system: it is a **method** for reconstructing, normalising and
> reconciling financial evidence from heterogeneous sources. **This is the first thing it
> publishes** — the format that makes the following steps possible. What comes next is at
> the end, under *The programme*.

> **This is a summary.** The authoritative document is `entregables/SPEC.md`, written in
> Spanish. If this page and the spec ever disagree, **the spec wins.** A full English
> translation is welcome — see `CONTRIBUIR.md`.

---

## The problem

Two official documents can state, on the same day, that an account holds **USD 24,817** and
**USD 0** — and both can be "correct". A system can mark the same operation **PASSED** and
**FAILED** on the same day. An audit can cite supporting artifacts **that do not exist**,
and nothing stops it.

None of that is fraud. It is a **format** problem: there is no way to write down, in a form a
computer understands, the difference between *I verified this* and *I was told this*, between
*it is zero* and *I have not looked*, between *this is current* and *this is eight months old*.

**Evidence Envelope is that format.** A record of 22 mandatory fields that forces you to
declare what you know, what you do not, and what backs the claim.

---

## The idea

Most data formats require you to fill in every field. Since you cannot fill in what you do
not know, people write a **zero**, or a reasonable guess, and **that false value travels
forever** through the rest of the system.

This contract does the opposite: **the gap is a legal value.**

```
Any of the 16 fact fields may be set to   UNKNOWN
On one condition: you must state WHY.
Without the reason, the record is invalid.
```

`UNKNOWN` **is not zero**. Zero is a measurement: *I looked and there was nothing there*.
`UNKNOWN` is the absence of measurement. Conflating the two is the most expensive error in
all of financial record-keeping, and this contract makes it impossible to write.

Each record also carries a second signed list — the fields that **were** established. The two
lists together must cover all 22 fields **exactly**: nothing missing, nothing repeated.
**Any conforming validator detects a hidden gap.**

---

## Try it in 30 seconds

No installation. Python 3, no dependencies.

```bash
git clone <this-repository>
cd evidence-envelope
python3 herramientas/validar_evidencia.py .
```

It should end with `RESULTADO: APROBADO`. The four files in `entregables/examples/` pass.

**All four are anonymised and none describes anybody.** Two are real on-chain readings of
**empty, randomly generated addresses** — they belong to no one; one describes a **synthetic**
statement published encrypted; and the fourth has its figures, date and assets **substituted**.
Each record declares this in its own `anonymization` field.

---

## What it guarantees — and what it does not

> **The record guarantees the FORM of evidence, not its FORCE.**

A record being **valid** means it **conforms to the format**. It does not mean the claim is
true, nor that its backing is any good. You can write a perfectly valid record supported by a
document nobody should accept — and a well-built record will say so, in its own confidence
field.

**The contract forces you to DECLARE. It does not force you to be RIGHT.** A format cannot
replace judgement; it can only stop judgement from being made on falsified data.

This is deliberate. A standard promising more than that would be lying.

---

## Status: this is the first step

**Version 0.2.0.** The contract is finished, tested and verified. **Nothing is built on top
of it.** No data reader, no calculation engine, no institution comparison, no risk score.

> **Can a third party who has never spoken to the author fill in a conforming record using
> only the manual and the schema?**

Tested five times with agents given zero prior context. All five found real defects. On the
fifth, **no invented values**.

**No institution is using it yet.** If you are reading this and it is relevant to you, that is
exactly the missing conversation.

### Known limitations, declared

- **22 fields across 12 domains** risks becoming unmanageable — and the number has already
  changed three times, the last time because **a field was genuinely missing**.
- **The contract declares validity periods; whether a system honours them is a different
  matter**, and that is not built.
- **A record expresses an amount at a date — it does not distinguish a balance from a flow.**
- **On-chain examples expire by design.** Past their validity they remain true *for that
  block*, but no longer describe the present.

Full list in `entregables/SPEC.md`, section *Limitaciones conocidas de v0.2.0*.

---

## What is here

| File | What it is |
|---|---|
| `entregables/SPEC.md` | **The manual.** What each of the 22 fields means, and how to fill it |
| `entregables/evidence-envelope.schema.json` | The contract, in machine-checkable form |
| `PORQUE.md` | The market problem behind it, with figures and sources |
| `entregables/examples/` | Four records, each from a different authority — **all of them anonymised** |
| `entregables/adjuntos/02-extracto-ejemplo.pdf.enc` | The **synthetic, encrypted** document example 02 refers to. Published so its hash can be verified; the password is not |
| `herramientas/validar_evidencia.py` | The validator. No dependencies |
| `SELLOS.txt` | SHA-256 of every published file. Check with `sha256sum -c SELLOS.txt` |
| `CHANGELOG.md` · `CONTRIBUIR.md` | Change history · how to contribute |

**Example 02 is the most useful of the four.** The statement is **encrypted** — it cannot be
opened without a password, so the amount could not be read. The record **declares the gap with
its reason** instead of filling in a zero. It shows what the contract does when it does not yet
know the amount — which is the normal case, not the exception.

**And the container is published.** You can verify that its SHA-256 is what the record claims,
and check for yourself that it will not open without the password. **There is no data about
anybody inside:** it is a document made for the example.

---

## Four confusions this contract prevents

**1. Not knowing becoming zero.** A declared gap can be chased down. A false zero cannot.

**2. The where being mistaken for the what.** The bank is not the peso. The wallet is not the
ether. Two separate mandatory fields — which sounds trivial until someone adds "what I hold at
the bank" to "what I hold in the currency" and counts the money twice.

**3. When we looked being mistaken for when it applies.** A statement I read today may be about
last month. A contract signed today may apply from January.

**4. A stale value still deciding.** A June measurement does not describe September. The number
is not erased — it is history — but **it loses its force: an expired value cannot support a
conclusion.**

And a one-line rule that prevents an enormous problem:

> **You can never write "this does not exist".** The contract has no way to say it. At most it
> permits "we have not established it". Failing to find something **is not proof** that it does
> not exist.

---

## The programme

**LAMC** came out of a concrete problem: one person with assets spread across banks, public
chains and documents, who needed to know what they actually knew and what they were assuming.
It is published because the problem is not one person's.

> **The asset is not the portfolio. It is the method.**

**Published today:** the 0.2.0 contract — this repository. The format. It is the step that
makes the others possible: **without a common record there is nothing to aggregate, nothing to
compare, nothing to audit.**

### What comes next, and in what order

Built **from simple to complex**. Every step has **a test a third party can fail**, and the
next step is not started until it passes.

| # | Step | Test to move on |
|---|---|---|
| **1** | **The contract** ✅ — this repository | Can a third party with no context fill in a valid record? **Tested five times** |
| **2** | **Reconstruct** — read real data and emit records for a whole portfolio | Does it reproduce a known total **without inventing a single value**? |
| **3** | **Operational controls** — a standard for what happens **off-chain**, which is where the breaches are | Can a third party verify a control's state **without asking the author**? |
| **4** | **Control data** — which control each protocol has, and which it does not | Can two institutions be compared with each other? |

**Why this order.** There is nothing to aggregate today because **the format for what we want
to aggregate does not exist**. Building the engine before the unit of measure is precisely how
you end up with two systems that cannot be compared — the problem described in `PORQUE.md`.

### What will NOT be built

- An investment dashboard, signals, or buy recommendations
- Key custody, or transaction signing
- Risk scores **before** the data that would support them exists
- Anything that advises: **the system declares. It does not recommend.**

---

*Apache-2.0. Use it, copy it, modify it, sell it. If you improve it, tell us how.*
