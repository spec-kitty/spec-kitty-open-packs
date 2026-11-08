package com.acme.quality;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class StrongOracleAssertionsTest {
    @org.junit.jupiter.api.Test
    void typeCheckHasAnotherStrongAssertion() {
        assertInstanceOf(String.class, value());
        assertEquals("expected", value());
    }

    @org.junit.jupiter.api.Test
    void typeCheckHasAMessage() {
        assertThatThrownBy(this::run)
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("boom");
    }

    @org.junit.jupiter.api.Test
    void typeCheckHasMessageContents() {
        assertThatThrownBy(this::run)
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("boom");
    }

    @org.junit.jupiter.api.Test
    void typeCheckHasACause() {
        assertThatThrownBy(this::run)
                .isInstanceOf(IllegalStateException.class)
                .hasCauseInstanceOf(IllegalArgumentException.class);
    }

    @org.junit.jupiter.api.Test
    void typeCheckHasARootCause() {
        assertThatThrownBy(this::run)
                .isInstanceOf(IllegalStateException.class)
                .hasRootCauseInstanceOf(IllegalArgumentException.class);
    }

    @org.junit.jupiter.api.Test
    void typeCheckSatisfiesAValueAssertion() {
        assertThat(value())
                .isInstanceOf(String.class)
                .satisfies(text -> assertEquals("expected", text));
    }

    @org.junit.jupiter.api.Test
    void typeCheckExtractsAValue() {
        assertThat(error())
                .isInstanceOf(IllegalStateException.class)
                .extracting(Throwable::getMessage)
                .isEqualTo("boom");
    }

    @org.junit.jupiter.api.Test
    void instanceOfSatisfyingChecksTheExceptionValue() {
        assertThatThrownBy(this::run)
                .isInstanceOfSatisfying(IllegalStateException.class,
                        error -> assertEquals("boom", error.getMessage()));
    }

    @org.junit.jupiter.api.Test
    void assertThrowsResultIsAsserted() {
        IllegalStateException error = assertThrows(IllegalStateException.class, this::run);
        assertEquals("boom", error.getMessage());
    }

    @org.junit.jupiter.api.Test
    void tryFailCatchChecksTheExceptionMessage() {
        try {
            run();
            fail("expected");
        } catch (IllegalStateException error) {
            assertTrue(error.getMessage().contains("boom"));
        }
    }
}
