package com.acme.quality;

import org.junit.jupiter.api.Test;

class NonArchUnitCheckTest {
    @Test
    void delegatesValidationWithoutAnAssertion() {
        validator.check(value());
    }
}
