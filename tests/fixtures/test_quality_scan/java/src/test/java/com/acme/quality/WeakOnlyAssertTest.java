package com.acme.quality;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.assertj.core.api.Assertions.assertThat;

class WeakOnlyAssertTest {
    @Test
    void onlyChecksTrue() {
        assertTrue(true);
    }

    @Test
    void onlyChecksNonNull() {
        assertNotNull(value());
    }

    @Test
    void onlyChecksAssertJNonNull() {
        assertThat(value()).isNotNull();
    }
}
