package com.acme.quality;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;

class OverMockingTest {
    @Test
    void constructsFourMocks() {
        Service first = mock(Service.class);
        Service second = mock(Service.class);
        Service third = mock(Service.class);
        Service fourth = mock(Service.class);
        assertEquals(4, java.util.List.of(first, second, third, fourth).size());
    }
}
