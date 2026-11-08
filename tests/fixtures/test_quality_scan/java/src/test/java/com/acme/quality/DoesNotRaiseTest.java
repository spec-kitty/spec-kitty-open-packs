package com.acme.quality;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.fail;

class DoesNotRaiseTest {
    @Test
    void completesWithoutAnException() {
        try {
            run();
        } catch (Exception error) {
            fail("unexpected exception", error);
        }
    }
}
