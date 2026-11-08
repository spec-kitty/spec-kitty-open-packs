package com.acme.quality;

import java.time.Instant;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NonDeterminismTest {
    @Test
    void sleeps() throws InterruptedException {
        Thread.sleep(1);
        assertEquals(1, 1);
    }

    @Test
    void readsCurrentTime() {
        assertTrue(Instant.now().isAfter(Instant.EPOCH));
    }
}
