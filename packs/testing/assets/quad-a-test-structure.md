# Quad-A test structure: skeleton and review checklist

The language-neutral skeleton of a Quad-A test, and a short checklist to review one. The `quadruple-a-test-format` styleguide in the testing pack explains each phase and carries language examples.

## Skeleton

```text
test <behaviour, in domain words>:
    # Arrange: put the system in the state the behaviour needs
    <build the subject and its collaborators; seed realistic state>

    # Assumption check: prove the arranged state is the one the test claims
    <assert the precondition; a wrong fixture fails here, loudly>

    # Act: trigger the one behaviour under test
    <exactly one action>

    # Assert: check the observable effect
    <returned value, persisted state, emitted event or raised error>
```

When the action's effect is an error, Act and Assert may fuse into one expect-raises block. When the default state already is the precondition, the assumption check may come first.

## Review checklist

- [ ] The name states the behaviour, and the body asserts exactly what the name promises.
- [ ] There is exactly one Act. Two actions, or two unrelated groups of assertions, mean two tests.
- [ ] An assumption check guards any precondition a fixture change could silently break.
- [ ] The Assert phase targets an observable outcome, not the call graph of owned collaborators.
- [ ] The phases are visible (labelled or separated) so a reader finds precondition, trigger and effect at a glance.
