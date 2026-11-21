# Test desiderata checklist

Kent Beck's twelve test desiderata (https://testdesiderata.com/), one line each, as a review checklist. They are properties to trade off deliberately, not to maximise all at once: decide which ones a given test optimises. When two of them seem to conflict, look for a design change (a clearer boundary, a pure function, composition) before accepting a brittle test.

- [ ] **Isolated**: the test returns the same result whatever order the tests run in; no shared mutable state, no order dependence. Isolated means independent of other tests. It does not mean isolating the unit from its collaborators with mocks.
- [ ] **Composable**: dimensions of variability can be tested separately and combined, so coverage grows without combinatorial test counts.
- [ ] **Deterministic**: if nothing changes, the result does not change; no reliance on clocks, randomness, network or ambient filesystem state.
- [ ] **Fast**: the test runs quickly enough to run after every small change.
- [ ] **Writable**: the test is cheap to write relative to the code it covers; expensive setup is a signal that the boundary is wrong.
- [ ] **Readable**: the test communicates its motivation and scenario to a future reader without spelunking the production code.
- [ ] **Behavioral**: the test is sensitive to changes in the behavior of the code under test.
- [ ] **Structure-insensitive**: the test does not change its result when internal structure is refactored without a behavior change.
- [ ] **Automated**: the test runs without human intervention.
- [ ] **Specific**: when the test fails, the cause is obvious from the failure alone.
- [ ] **Predictive**: when all tests pass, the code is fit for production.
- [ ] **Inspiring**: passing the suite inspires the confidence to ship.

A Behavioral test is shown, not assumed, to be Behavioral: break the behavior once and watch it go red.

Beck's desiderata never mention mocks or test doubles. Reading Predictive, Specific, Behavioral and Structure-insensitive as a reason to substitute only at the responsibility boundary is an application of the properties, not a quotation.
