package com.acme.quality;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.fail;

class BroadRaisesTest {
    @org.junit.jupiter.api.Test
    void catchesException() {
        assertThrows(Exception.class, this::run);
    }

    @org.junit.Test(expected = RuntimeException.class)
    void catchesJUnit4RuntimeException() {
        run();
    }

    @org.junit.jupiter.api.Test
    void catchesThrowableInTryFail() {
        try {
            run();
            fail("expected");
        } catch (Throwable error) {
            assertThrows(IllegalStateException.class, () -> error.getClass());
        }
    }
}
