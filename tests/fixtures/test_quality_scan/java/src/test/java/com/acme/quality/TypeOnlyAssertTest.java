package com.acme.quality;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;
import static org.assertj.core.api.Assertions.assertThat;

class TypeOnlyAssertTest {
    @org.junit.jupiter.api.Test
    void onlyChecksJunitType() {
        assertInstanceOf(String.class, value());
    }

    @org.junit.jupiter.api.Test
    void onlyChecksAssertJType() {
        assertThat(value()).isInstanceOf(String.class);
    }

    @org.junit.jupiter.api.Test
    void onlyChecksExceptionType() {
        assertThrows(IllegalStateException.class, this::run);
    }

    @org.junit.jupiter.api.Test
    void checksExceptionMessage() {
        IllegalStateException error = assertThrows(IllegalStateException.class, this::run);
        assertTrue(error.getMessage().contains("expected"));
    }

    @org.junit.Test(expected = IllegalStateException.class)
    void onlyChecksJUnit4ExceptionType() {
        run();
    }

    @org.junit.jupiter.api.Test
    void onlyChecksCaughtExceptionType() {
        try {
            run();
            fail("expected");
        } catch (IllegalStateException error) {
            assertEquals("boom", error.getClass().getSimpleName());
        }
    }
}
