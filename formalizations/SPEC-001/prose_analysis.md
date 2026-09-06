# Prose Analysis Report: SPEC-001
**Schema Version:** 1.0.0

## 1. Extracted Semantic Clauses & Claims
### Clause `CLS-001`
> The emergency brake system shall initiate deceleration when time-to-collision is below 1.5 seconds.

**Functional Claims:**
- **[CLM-001-1]** (`postcondition`): The emergency brake system shall initiate deceleration when time-to-collision is below 1.5 seconds.
  - *Arg:* Mandated by imperative phrasing ('must'/'shall').

### Clause `CLS-002`
> If sensor confidence drops below 80 percent, the controller must degrade gracefully to manual override.

**Functional Claims:**
- **[CLM-002-1]** (`postcondition`): If sensor confidence drops below 80 percent, the controller must degrade gracefully to manual override.
  - *Arg:* Mandated by imperative phrasing ('must'/'shall').

### Clause `CLS-003`
> The target deceleration rate must not exceed 9.8 m/s^2 under dry pavement conditions.

**Functional Claims:**
- **[CLM-003-1]** (`postcondition`): The target deceleration rate must not exceed 9.8 m/s^2 under dry pavement conditions.
  - *Arg:* Mandated by imperative phrasing ('must'/'shall').

## 2. Uncertainty Record (Ambiguities & Under-specifications)
- **Clause `CLS-002`** [underspecification]:
  - *Source text:* "If sensor confidence drops below 80 percent, the controller must degrade gracefully to manual override."
  - *Assumptions made:*
    - Under-specified adjective detected; concrete threshold needed in formal model.