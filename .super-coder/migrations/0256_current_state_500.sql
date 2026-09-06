-- 0256 — current_state trigger 300 -> 500.
-- Guidance says "under approximately 300 characters, point at rows by id";
-- the trigger enforced exactly 300 and rejected ordinary pointer-shaped
-- states that ran a few dozen characters over. Feature #72 (spec #218,
-- decision #326): the advisory stays ~300 in boot, the hard stop moves to 500.
-- Same pointer-oriented message. Idempotent: DROP + CREATE.

BEGIN;

DROP TRIGGER IF EXISTS trg_shells_current_state_len;
CREATE TRIGGER trg_shells_current_state_len
BEFORE UPDATE OF current_state ON shells
WHEN LENGTH(COALESCE(NEW.current_state, '')) > 500
BEGIN
  SELECT RAISE(ABORT, 'current_state over 500 chars — name what is in flight and point at the row (doc/feature/flag/decision id), do not reproduce it');
END;

COMMIT;
