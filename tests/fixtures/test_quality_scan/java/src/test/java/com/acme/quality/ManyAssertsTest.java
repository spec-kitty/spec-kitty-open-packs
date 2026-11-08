package com.acme.quality;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ManyAssertsTest {
    @Test
    void checksFifteenValues() {
        assertEquals(1, 1);
        assertEquals(2, 2);
        assertEquals(3, 3);
        assertEquals(4, 4);
        assertEquals(5, 5);
        assertEquals(6, 6);
        assertEquals(7, 7);
        assertEquals(8, 8);
        assertEquals(9, 9);
        assertEquals(10, 10);
        assertEquals(11, 11);
        assertEquals(12, 12);
        assertEquals(13, 13);
        assertEquals(14, 14);
        assertEquals(15, 15);
    }
}
