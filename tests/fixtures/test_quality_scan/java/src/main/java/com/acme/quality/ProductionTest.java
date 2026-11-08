package com.acme.quality;

class ProductionTest {
    @org.junit.jupiter.api.Test
    void notDiscoveredBecauseThisIsNotATestSourceRoot() {
        service.run();
    }
}
