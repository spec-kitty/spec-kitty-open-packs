package com.acme.quality;

import org.junit.jupiter.api.Test;
import org.mockito.Mock;

import static org.junit.jupiter.api.Assertions.assertEquals;

class OverMockingFieldsTest {
    @Mock Service first;
    @Mock Service second;
    @Mock Service third;
    @Mock Service fourth;

    @Test
    void usesAMockCollaborator() {
        first.run();
        assertEquals(1, 1);
    }
}
