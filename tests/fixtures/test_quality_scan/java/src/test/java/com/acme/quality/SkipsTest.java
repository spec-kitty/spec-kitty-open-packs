package com.acme.quality;

import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SkipsTest {
    @Disabled("fixture")
    @Test
    void disabledJUnit5Test() {
        assertEquals(1, 1);
    }

    @org.junit.Ignore("fixture")
    @org.junit.Test
    void ignoredJUnit4Test() {
        assertEquals(1, 1);
    }

    @Test
    void assumedTest() {
        Assumptions.assumeTrue(false);
        assertEquals(1, 1);
    }
}
