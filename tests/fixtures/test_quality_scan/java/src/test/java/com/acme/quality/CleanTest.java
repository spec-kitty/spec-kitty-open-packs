package com.acme.quality;

import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CleanTest {
    @Test
    void comparesTheResult() {
        assertEquals("expected", value());
    }

    @ParameterizedTest
    @ValueSource(strings = "expected")
    void comparesEachParameterizedResult(String value) {
        assertEquals("expected", value);
    }

    @RepeatedTest(2)
    void comparesEachRepeatedResult() {
        assertEquals("expected", value());
    }

    @TestFactory
    DynamicTest comparesADynamicResult() {
        return DynamicTest.dynamicTest("result", () -> assertEquals("expected", value()));
    }

    @org.junit.Test
    void comparesAJUnit4Result() {
        assertEquals("expected", value());
    }

    @org.junit.jupiter.api.TestTemplate
    void comparesATemplatedResult() {
        assertEquals("expected", value());
    }

    @Test
    void delegatesToAnAssertingHelper() {
        assertPayload(value());
    }

    @Test
    void aDomainNowHelperIsNotAClockCall() {
        assertEquals("expected", now());
    }

    private String now() {
        return value();
    }

    private void assertPayload(String payload) {
        assertEquals("expected", payload);
    }
}
